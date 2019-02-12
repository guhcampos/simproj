# -*- coding: utf-8 -*-
import logging
import math
from google.appengine.ext import ndb


class Selic(ndb.Model):

    prazo = ndb.IntegerProperty(required=True)
    taxa = ndb.FloatProperty(required=True)
    updated = ndb.DateProperty(required=True)

    logger = logging.getLogger("Selic")

    '''
    Dado o prazo de uma transação, juroDiario retorna o valor diário
    do juro composto para o prazo mais próximo existente no banco de dados.

    Exemplo: se no banco de dados temos o valor do juro anual para aplicações
    com 10 e 15 dias de prazo, ao se pedir uma aplicação com 12 dias,
    será retornado o valor do juro diário com prazo de 15 dias.
    '''
    @classmethod
    def juroDiario(cls, prazo=None):

        Selic.logger.info("Calculando Juro para prazo: {}".format(prazo))

        if len(Selic.query().fetch()) == 0:
            raise SystemError("Não existem entradas para SELIC no banco de dados")

        if prazo is None:
            raise ValueError("Prazo não informado")

        # comecamos com um indice vazio
        indice = None

        # buscamos pelo prazo mais próximo superiormente
        while indice is None:        

            Selic.logger.info("Trying for: {}".format(prazo))

            indice = Selic.query(Selic.prazo == prazo).get()
            prazo += 1

        # [(1+n)^(1/360)]-1
        return math.pow(float(1.0+indice.taxa/100.0), float(1.0/360.0)) - 1.0


class IGPM(ndb.Model):

    prazo = ndb.IntegerProperty(required=True)
    taxa = ndb.FloatProperty(required=True)
    updated = ndb.DateProperty(required=True)
