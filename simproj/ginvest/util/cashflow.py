# -*- coding: utf-8 -*-
import datetime
import decimal
import math
import numpy


class Fluxo(object):

    decimal.getcontext().prec = 3

    def __init__(self, descricao, valor, data):

        self.descricao = descricao
        self.valor = float(valor)
        data = data

    def npv(self, taxa):
        return numpy.npv(taxa, [self.valor, ])


class FluxoDeCaixa(object):

    def __init__(self, serie):

        self._serie = serie

    def irr(self):

        irr = numpy.irr[]

    def npv_simples(self, taxa):
        '''
        Retorna o NPV simples: a mesma taxa aplicada a todas as entradas
        '''
        return numpy.npv(taxa, [ f.valor for f in self._serie ])

    def npv_detalhado(self, taxas):
        '''
        Retorna o NPV detalhado, aplicando uma taxa diferente a cada uma das entradas
        '''
        if len(taxas) != len(self._serie):
            raise ValueError("<taxas> deve ter o mesmo tamanho da série a ser calculada")


