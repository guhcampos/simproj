# -*- coding: utf-8 -*-
import datetime
import time
import ginvest.util.interest as interest

from django.db import models


class TesouroDireto(models.Model):

    _profitability = None

    DEBUGPRE = "## DEBUG TesouroDireto"

    NOINDEX = 0
    INDEX_SELIC = 1
    INDEX_IPCA = 2
    INDEX_IGPM = 3

    INDEX_CHOICES = (
        (NOINDEX, "Nao Indexado"),
        (INDEX_SELIC, "SELIC"),
        (INDEX_IPCA, "IPCA"),
        (INDEX_IGPM, "IGP-M"),
        )

    name = models.CharField(
        help_text="The name of this paper",
        verbose_name="Name",
        blank=False,
        max_length=6,
        )

    description = models.CharField(
        help_text="Description of this paper",
        verbose_name="Description",
        blank=False,
        max_length=255,
        )

    maturity = models.DateField(
        help_text="The maturity of this bond",
        verbose_name="Maturity",
        blank=False,
        null=False,
        )

    rate = models.FloatField(
        help_text="The annual rate of this bond",
        verbose_name="Monthly Rate",
        blank=False,
        null=False,
        )

    indexedby = models.IntegerField(
        help_text="Is this bond posfixed by some index?",
        verbose_name="Index",
        blank=False,
        null=False,
        choices=INDEX_CHOICES,
        )

    updated = models.DateField(
        help_text="When this information was last updated",
        verbose_name="Updated in",
        blank=False,
        null=False,
        )

    class Meta:

        app_label = "simproj"
        ordering = ["name", "maturity", ]
        verbose_name = "Título do Tesouro Nacional"
        verbose_name_plural = "Títulos do Tesouro Nacional"
        unique_together = ["name", "maturity", ]


    def __unicode__(self):
        return "TD: {} due to {}, rate {} indexed by {}".format(
                    self.name, self.maturity, self.rate, self.get_indexedby_display()
                )

    def _gen_profitability(self, value, startdate, enddate):

        fixedrate = self.rate

        current_date = startdate
        monthly_rate = 1.0 + interest.year_to_month(fixedrate)

        result = list()

        while current_date < enddate:
            float_rate = 1.0

            newvalue = value * monthly_rate * float_rate
            thisdate = current_date

            value = newvalue
            current_date += datetime.timedelta(days=30)

            result.append((thisdate, value))

        return result

    def profitability(self, value, startdate, enddate):
        self._profitability = self._gen_profitability(value, startdate, enddate)
        return self._profitability

    def profitability_chart(self):

        if self._profitability is None:
            raise AttributeError("Profitability is not calculated")

        return [ 
                    (time.mktime(date.timetuple()), "{:.2f}".format(value))
                    for (date, value)
                    in self._profitability
                ]
