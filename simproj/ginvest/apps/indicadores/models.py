# -*- coding: utf-8 -*-

#import logging
import math
from django.db import models
from django.conf import settings


class DailyRateManager(models.Manager):

    DEBUGPRE = "## DEBUG DailyRateManager"

    def daily_rate_for(self, maturity):

        """
        Calculates the daily rate for a given maturity by finding the nearest upper maturity
        available in the database

        """

        # get all maturities greater than query, order lowest first and get first element
        accumulated = super(DailyRateManager, self).get_query_set().filter(
            maturity__gte=maturity
        ).order_by("maturity")[0]

        # [(1+n)^(1/360)]-1
        daily_rate = math.pow(1.0 + float(accumulated.rate / 100.0), float(1.0 / 360.0)) - 1.0

        # if settings.DEBUG:
        #     print(self.DEBUGPRE+" accumulated: {}".format(accumulated))
        #     print(self.DEBUGPRE+" maturity {}, daily_rate {}".format(maturity, daily_rate))

        return daily_rate

    def monthly_rate_for(self, maturity):
        """
        Calculates the daily rate for a given maturity by finding the nearest upper maturity
        available in the database

        """

        # get all maturities greater than query, order lowest first and get first element
        accumulated = super(DailyRateManager, self).get_query_set().filter(
            maturity__gte=maturity
        ).order_by("maturity")[0]

        # [(1+n)^(1/360)]-1
        monthly_rate = math.pow(1.0 + float(accumulated.rate / 100.0), float(1.0 / 12.0)) - 1.0

        # if settings.DEBUG:
        #     print(self.DEBUGPRE+" accumulated: {}".format(accumulated))
        #     print(self.DEBUGPRE+" maturity {}, daily_rate {}".format(maturity, daily_rate))

        return monthly_rate

    def yearly_rate_for(self, maturity):
        """
        Calculates the daily rate for a given maturity by finding the nearest upper maturity
        available in the database

        """

        # get all maturities greater than query, order lowest first and get first element
        accumulated = super(DailyRateManager, self).get_query_set().filter(
            maturity__gte=maturity
        ).order_by("maturity")[0]

        return accumulated

    def total_rate_for(self, maturity):
        """
        Calculates the stacked rate for a given maturity
        """

        total_rate = math.pow(1.0 + self.daily_rate_for(maturity), maturity)

        if settings.DEBUG:
            print(self.DEBUGPRE + " maturity {}, total_rate {}".format(maturity, total_rate))

        return total_rate


class DailyRateManagerInflacao(models.Manager):

    DEBUGPRE = "## DEBUG DailyRateManagerInflacao"

    def period_rate(self, maturity):

        """
        Calculates the daily rate for a given maturity by finding the nearest upper maturity
        available in the database

        """

        # get all maturities greater than query, order lowest first and get first element
        final = super(DailyRateManagerInflacao, self).get_query_set().filter(
            maturity__gte=maturity
        ).order_by("maturity")[0]

        initial = super(DailyRateManagerInflacao, self).get_query_set().order_by("maturity")[0]

        # (final - initial) / initial
        period_rate = (final.rate - initial.rate) / initial.rate

        # if settings.DEBUG:
        #     print(self.DEBUGPRE+" final points: {}".format(final))
        #     print(self.DEBUGPRE+" initial points: {}".format(initial))
        #     print(self.DEBUGPRE+" maturity {}, period_rate {}".format(maturity, period_rate))

        return period_rate


class IndicadorFinanceiro(models.Model):

    maturity = models.IntegerField(
        help_text="The maturity for this entry",
        verbose_name="Maturity",
        blank=False,
        null=False,
    )

    rate = models.FloatField(
        help_text="The accumulated rate for this maturity",
        verbose_name="Rate",
        blank=False,
        null=False,
    )

    updated = models.DateField(
        help_text="Last time this was updated",
        verbose_name="Updated",
        blank=False,
        null=False,
    )

    class Meta:

        abstract = True
        app_label = "indicadores"

    def __unicode__(self):

        return "{} >> Prazo: {} dias, Taxa: {:6.2f} pontos".format(
            self.__class__._meta.verbose_name, self.maturity, self.rate
        )


class SELIC(IndicadorFinanceiro):

    objects = DailyRateManager()

    class Meta:

        app_label = "indicadores"
        verbose_name = "SELIC"
        verbose_name_plural = "SELIC"
        ordering = ["maturity", ]


class IGPM(IndicadorFinanceiro):

    objects = DailyRateManagerInflacao()

    class Meta:

        app_label = "indicadores"
        verbose_name = "IGP-M"
        verbose_name_plural = "IGP-M"
        ordering = ["maturity", ]


class IPCA(IndicadorFinanceiro):

    objects = DailyRateManagerInflacao()

    class Meta:

        app_label = "indicadores"
        verbose_name = "IPCA"
        verbose_name_plural = "IPCA"
        ordering = ["maturity", ]
