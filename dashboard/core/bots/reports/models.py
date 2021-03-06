import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _

from dashboard.core.bots.models import Bot
from dashboard.core.browsers.models import Browser
from dashboard.core.tests.models import Test
from dashboard.core.metric_units.models import MetricUnit




AGGREGATION_CHOICES = (
    ('None', 'None'),
    ('Total', 'Total'),
    ('Arithmetic', 'Arithmetic'),
    ('Geometric', 'Geometric'),
)


class BotReportDataManger(models.Manager):
    def create_report(self, bot, browser, browser_version, root_test,
                      test_path, test_version, aggregation, metric_unit,
                      metric_unit_prefixed, mean_value, stddev, delta,
                      is_improvement,prev_result,timestamp=None):
        bot_report_data = self.create(
            bot=bot, browser=browser, browser_version=browser_version,
            root_test=root_test, test_path=test_path,
            test_version=test_version, aggregation=aggregation,
            metric_unit=metric_unit, metric_unit_prefixed=metric_unit_prefixed,
            mean_value=mean_value, stddev=stddev, delta=delta,
            is_improvement=is_improvement, prev_result=prev_result,
            timestamp=timestamp
        )
        return bot_report_data


class BotReportData(models.Model):
    id = models.AutoField(primary_key=True)
    bot = models.ForeignKey(
        Bot, blank=False, null=False, related_name='bot_relation',
        related_query_name='bot_relation'
    )
    browser = models.ForeignKey(Browser, blank=False, null=False)
    browser_version = models.CharField(
        _('Browser Version'), max_length=500, blank=True, unique=False
    )
    root_test = models.ForeignKey(
        Test, blank=False, null=False, related_name='root_test'
    )
    test_path = models.CharField(
        _('Test Path'), max_length=500, blank=True, unique=False
    )
    test_version = models.CharField(
        _('Test Version'), max_length=500, blank=True, unique=False
    )
    aggregation = models.CharField(
        _('Aggregation'), max_length=50, choices=AGGREGATION_CHOICES,
        default='na'
    )
    metric_unit = models.ForeignKey(
        MetricUnit, blank=False, null=False
    )
    metric_unit_prefixed = models.CharField(
        _('Metric Unit Prefixed'), max_length=70, blank=True, unique=False
    )
    mean_value = models.FloatField(_('Mean Value'),null=True, blank=True)
    stddev = models.FloatField(_('Standard Deviation'),null=True, blank=True)
    delta = models.FloatField(
        _('Delta Field'), null=True, blank=True, default=0.00
    )
    timestamp = models.DateTimeField()
    is_improvement = models.BooleanField(default=False)
    prev_result = models.ForeignKey(
        'self', blank=True, null=True, related_name='prev_results'
    )

    objects = BotReportDataManger()

    def save(self, *args, **kwargs):
        if self.timestamp is None:
            self.timestamp = datetime.datetime.utcnow()
        super(BotReportData, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.bot.name + ":" + str(self.browser) \
               + ":" + self.test_version + ":" +\
               self.test_path + ":" + str(self.mean_value)

    class Meta:
        unique_together = (
            'bot', 'browser', 'browser_version', 'root_test', 'test_path',
            'test_version', 'metric_unit', 'aggregation',
        )