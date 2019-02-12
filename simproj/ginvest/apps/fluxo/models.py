# -*- coding: utf-8 -*-
import datetime
import decimal
import math
import numpy
import time

from django.db import models
from django.conf import settings
from ginvest.apps.indicadores.models import SELIC
from ginvest.apps.indicadores.models import IPCA
from ginvest.apps.indicadores.models import IGPM


class CashFlowSeries(models.Model):

    DEBUGPRE = "## DEBUG CashFlowSeries"

    project = models.CharField(
        help_text="Which project this series belong to",
        verbose_name="Project",
        blank=False,
        default="Projeto Sem Nome",
        max_length=64,
        unique=True,
    )

    description = models.CharField(
        help_text="Description of this series",
        verbose_name="Description",
        blank=True,
        max_length=255
    )

    discounted = models.DateField(
        help_text="Last time this was discounted",
        verbose_name="Discounted Date",
        blank=True,
        null=True
    )

    use_selic = models.BooleanField(
        help_text="Whether this series should be discounted with SELIC index",
        verbose_name="Use Selic?",
        blank=False,
        null=False
    )

    use_ipca = models.BooleanField(
        help_text="Whether this series should be discounted with IPCA index",
        verbose_name="Use IPCA?",
        blank=False,
        null=False
    )

    use_igpm = models.BooleanField(
        help_text="Whether this series should be discounted with IGP-M index",
        verbose_name="Use IGP-M?",
        blank=False,
        null=False
    )

    class Meta:

        app_label = "fluxo"
        verbose_name = "Cash Flow Series"
        verbose_name_plural = "Cash Flows Series"

    def __unicode__(self):
        return "Projeto: {nome} -  IPCA: {ipca}, IGP-M: {igpm}, SELIC: {selic}".format(
            nome=self.project,
            ipca=self.use_ipca, igpm=self.use_igpm, selic=self.use_selic)

    def discount(self):

        for flow in self.cashflows():
            flow.discount(self.selic, self.ipca, self.igpm)

        self.discounted = datetime.datetime.today()

        return self

    def npv(self):
        """
        Returns the accumulated NPV of this cash flow series
        """
        if self.discounted is None:
            raise AttributeError("Cannot calculate NPV of series before discounting")

        decimal.getcontext().prec = 3

        # returns the sum of the lists of npvs
        return numpy.sum([flow.npv for flow in self.cashflows.all()])

    def irr(self):
        """
        Returns the Internal Return Rate of this series of cash flows
        """

        if self.discounted is None:
            raise AttributeError("Cannot calculate IRR of series before discounting")

        irr = numpy.irr([flow.npv for flow in self.cashflows.all()])

        if math.isnan(irr):
            return 0

        else:
            return round(irr * 100, 2)

    def size(self):
        return len(self.cashflows.all())

    def json(self):

        r = list()

        for f in self.cashflows.all():
            r.append(f.json())

        return r

    def compare_plot(self):

        ret =  [
            [time.mktime(flow.date.timetuple()), "{:.2f}".format(flow.npv)]
            for flow
            in self.cashflows.all()

        ]

        ret[0][1] = "{:.2f}".format(math.fabs(self.cashflows.all()[0].npv))

        return ret

    def npvplot(self):

        reply = dict()
        balance = 0
        reply["cashflow"] = list()

        for tr in self.cashflows.all():

            balance += tr.npv
            reply["cashflow"].append(
                {
                    "date": tr.date.strftime("%Y%m%d"),
                    "ammount": "{:.2f}".format(tr.npv),
                    "balance": "{:.2f}".format(balance)
                }
            )

        reply["yrange"] = round(max(math.fabs(x.npv) for x in self.cashflows.all()), 0)

        return reply


class CashFlow(models.Model):

    DEBUGPRE = "## DEBUG CashFlow"

    series = models.ForeignKey(
        CashFlowSeries,
        help_text="A series of cashflows to which this one belongs",
        verbose_name="Series",
        related_name="cashflows"
    )

    description = models.CharField(
        help_text="Description of this transaction",
        verbose_name="Description",
        blank=False,
        max_length=255
    )

    value = models.DecimalField(
        help_text="The money ammount of this transaction",
        verbose_name="Value",
        blank=False,
        null=False,
        decimal_places=2,
        max_digits=24
    )

    date = models.DateField(
        help_text="The date when the transaction ocurred",
        verbose_name="Date",
        blank=False,
        null=False
    )

    npv = models.DecimalField(
        help_text="The latest Net Present Value calculated for this transaction",
        verbose_name="NPV",
        blank=True,
        null=True,
        decimal_places=2,
        max_digits=24
    )

    npv_date = models.DateField(
        help_text="The date for which the calculated NPV was valid",
        verbose_name="NPV Updated on",
        blank=True,
        null=True
    )

    class Meta:

        app_label = "fluxo"
        verbose_name = "Cash Flow"
        verbose_name_plural = "Cash Flows"
        ordering = ["date", ]

    def discount(self, use_selic=False, use_ipca=False, use_igpm=False):

        decimal.getcontext().prec = 3

        maturity = (self.date - datetime.datetime.today()).days

        if settings.DEBUG:
            print(self.DEBUGPRE)
            print(self.DEBUGPRE + " Selic {} - IPCA - {} - IGP-M {}".format(use_selic, use_ipca, use_igpm))
            print(self.DEBUGPRE + " ###### Discounting... ######")
            print(self.DEBUGPRE + " Maturity {}".format(maturity))
            print(self.DEBUGPRE + " Value {:6.2f}".format(self.value))

        # Shortcut for present cash flows
        if maturity == 0:
            self.npv = self.value

        ### INTEREST
        if not use_selic:
            # short cut for no selic
            interest_multiplier = 1

        else:
            # We get the daily interest rate for SELIC and pow() it to the number of days
            interest_multiplier = float(SELIC.objects.total_rate_for(maturity))

        if settings.DEBUG:
            print(self.DEBUGPRE + " Interest {:6.3f}".format(interest_multiplier))

        ### INFLATION
        ipca = 1.0
        igpm = 1.0

        if use_ipca:
            ipca = 1.0 + float(IPCA.objects.period_rate(maturity))

        if use_igpm:
            igpm = 1.0 + float(IGPM.objects.period_rate(maturity))

        if not use_ipca and not use_igpm:
            # shortcut for no inflation
            inflation_multiplier = 1.0

        if use_ipca or use_igpm:
            # ((igpm+ipca)/2)^maturity
            inflation_multiplier = ipca * igpm

        if settings.DEBUG:
            print(self.DEBUGPRE + " IPCA  {:6.3f}".format(ipca))
            print(self.DEBUGPRE + " IGP-M {:6.3f}".format(igpm))
            print(self.DEBUGPRE + " INFL MULTI {:6.3f}".format(inflation_multiplier))

        self.npv = self.value * interest_multiplier * inflation_multiplier

        if settings.DEBUG:
            print(self.DEBUGPRE + " NPV: {:6.2f}".format(self.npv))

        self.updated = datetime.datetime.today()

        return self.npv

    def __unicode__(self):
        return "Projeto: '{name}', Fluxo do Dia: {date}. Valor: R$ {value:6.2f}, NPV: R$ {npv:6.2f}".format(
            name=self.series.project, date=self.date, value=self.value, npv=self.npv
        )

    def json(self):

        r = dict()

        r["desc"] = self.description
        r["val"] = "{:8.2f}".format(self.value)
        r["npv"] = "{:8.2f}".format(self.npv)
        r["date"] = self.date.strftime("%d/%m/%Y")

        return r
