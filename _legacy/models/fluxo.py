# -*- coding: utf-8 -*-
import datetime
import decimal
import logging
import math
import numpy
from google.appengine.ext import ndb
from models.indices import Selic


# class FluxoDeCaixa(object):

#     logger = logging.getLogger("FluxoDeCaixa")

#     def __init__(self):

#         self.fluxos = list()

#     def append(self, fluxo):
#         self.fluxos.append(fluxo)

#     def capitaliza(self, juros=None, inflacao=None):
#         for fluxo in self.fluxos:
#             fluxo.capitaliza(juros=juros, inflacao=inflacao)

#     '''
#     ###
#     Retorna o VPL agregado desta serie de fluxos de caixa
#     ###
#     '''
#     def npv(self):

#         r = 0.00

#         for fluxo in self.fluxos:
#             r += fluxo.npv

#         return "{:.2f}".format(r)

#     def roi(self):
#         raise NotImplementedError("ROI não implementado")

#     '''
#     ###
#     Retorna a TIR desta serie de fluxos de caixa
#     ###
#     '''
    def irr(self):
        self.logger.info([fluxo.npv for fluxo in self.fluxos])
        r = numpy.irr([fluxo.npv for fluxo in self.fluxos])
        self.logger.info("Calculando TIR: {}".format(r))

        if math.isnan(r):
            return 0

        return round(r*100, 2)

    '''
    ###
    Retorna o tamanho do fluxo de caixa
    ###
    '''
    def size(self):
        return len(self.fluxos)

    '''
    ###
    Retorna uma versão serializável via JSON desta serie de fluxos de caixa
    ###
    '''
    def json(self):

        r = list()

        for f in self.fluxos:
            r.append(f.jsondict())

        return r

    '''
    ###
    Retorna os dados da plotagem do NPV na forma de um dict
    ###
    '''
    def npvplot(self):

        reply = dict()
        balance = 0
        reply["cashflow"] = list()

        # Acumula o NPV total e a lista de pares ordenados (date, valor)
        for tr in self.fluxos:
            balance += tr.npv
            reply["cashflow"].append(
                {
                    "date": tr.date.strftime("%Y%m%d"),
                    "ammount": "{:.2f}".format(tr.npv),
                    "balance": "{:.2f}".format(balance)
                }
            )

        # Define o range do grafico como o valor absoluto maximo do balanço
        reply["yrange"] = round(max(math.fabs(x.npv) for x in self.fluxos), 0)
        return reply

    '''
    ###
    Retorna o juro para o período total
    ###
    '''
    def selic(self):
        lastflow = self.fluxos[-1]
        prazo = (lastflow.date - datetime.datetime.today()).days
        j = Selic.juroDiario(prazo)
        self.logger.info("Juro no periodo: {}".format(j))
        return j


class Fluxo(ndb.Model):

    descricao = ndb.StringProperty()
    valor = ndb.FloatProperty()
    npv = ndb.FloatProperty()
    date = ndb.DateProperty()

    logger = logging.getLogger("Fluxo")

    def jsondict(self):

        if self.npv is None:
            self.capitali

        r = dict()

        r['descricao'] = self.descricao
        r['valor'] = "{:.2f}".format(self.valor)
        r['npv'] = "{:.2f}".format(self.npv)
        r['date'] = self.date.strftime("%d/%m/%Y")
        return r

    '''
    Capitaliza/Descapitaliza uma transacao de fluxo de caixa para o valor presente a fim de
    permitir calculos e comparacoes
    '''

    def capitaliza(self, juros=None, inflacao=None):

        decimal.getcontext().prec = 3

        if juros is None:
            juros = "selic"

        if inflacao is None:
            inflacao = "igpm"

        # NOT IMPLEMENTED INFLACAO
        inflacao = None

        self.logger.info("Capitalizando fluxo {}".format(self))

        prazo = (self.date - datetime.datetime.today()).days

        if prazo == 0:
            self.npv = self.valor

        else:

            if juros is "selic" and inflacao is None:
                #dec = decimal.Decimal(self.valor) * decimal.Decimal(math.pow(1+Selic.juroDiario(prazo), prazo))
                dec = self.valor * math.pow(1+Selic.juroDiario(prazo), prazo)
                self.npv = float(dec)
            else:
                raise NotImplementedError("Capitalização por inflação não implementada")

        return self
