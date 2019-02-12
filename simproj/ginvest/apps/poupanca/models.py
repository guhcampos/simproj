import datetime
import time
#from django.conf import settings
from ginvest.apps.indicadores.models import SELIC


LIMIAR_POUPANCA = 8.5
PORCENTAGEM_POUPANCA = 0.7
CONSTANTE_POUPANCA = 0.5

#
# TODO
#
# Obter a TR de forma correta
#
TR_CONSTANTE = 0.1


class Poupanca(object):

    def rendimentos(self, data_inicial, data_final, valor_inicial):
        """
        Rendimentos da poupcanca:

        0.5% + TR se SELIC Anual > 8.5%
        0.7 * Selic Mensal + TR se SELIC Anual <= 8.5%

        """

        rendimentos = []

        #prazo = datetime.datetime.today() + datetime.timedelta(days=dias)

        #
        # TODO
        #
        # Calcular corretamente a quantidade de meses nesse periodo de dias
        # lembrando que meses incompletos nao contam para o rendimento da poupanca
        #
        # P.S.: assumimos que a poupanca aniversaria no dia primeiro de cada mes
        #
        meses = (data_final - data_inicial).days / 30

        for i in range(1, meses):

            selic = SELIC.objects.monthly_rate_for(i * 30)
            selic_ano = SELIC.objects.yearly_rate_for(i * 30)

            # if settings.DEBUG:
            #     print("Prazo = {} meses".format(i))
            #     print("Selic Anual = {}".format(selic_ano))
            #     print("Selic Mensal = {}".format(selic))

            if selic_ano <= LIMIAR_POUPANCA:
                rendimentos.append(
                    1.0 + (((PORCENTAGEM_POUPANCA * selic) + TR_CONSTANTE) / 100)
                )
            else:
                rendimentos.append(
                    1.0 + ((CONSTANTE_POUPANCA + TR_CONSTANTE) / 100)
                )

        valor_intermediario = valor_inicial
        current_date = data_inicial

        yield(time.mktime(current_date.timetuple()), "{:.2f}".format(valor_inicial))

        for taxa in rendimentos:
            current_date = current_date + datetime.timedelta(days=30)
            valor_intermediario = float(valor_intermediario) * (1.0 + taxa / 100)
            yield (time.mktime(current_date.timetuple()), "{:.2f}".format(valor_intermediario))
