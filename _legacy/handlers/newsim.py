# -*- coding: utf-8 -*-
import datetime
import json
import logging
from handlers.default import SimProjHandler
from models.fluxo import Fluxo, FluxoDeCaixa


class NewSimHandler(SimProjHandler):

    logger = logging.getLogger("NewSimHandler")

    def get(self):
        self.render_response('newsim.html', **self.context)


class FluxoProcessorHandler(SimProjHandler):

    logger = logging.getLogger("FluxoProcessorHandler")

    def post(self):

        self.response.headers['Content-Type'] = 'application/json'

        fluxos = FluxoDeCaixa()
        resposta = dict()
        
        #
        # CONFIGURACOES
        #
        juros = "selic"
        inflacao = None

        # Pegamos os dados importados do CSV e transformamos numa
        # lista de objetos Fluxo, que representam fluxos de caixa
        for item in json.loads(self.request.POST.items()[0][0]):

            try:
                fluxo = Fluxo(
                    descricao=item[0],
                    valor=float(item[2]),
                    date=datetime.datetime.strptime(item[1], "%Y-%m-%d")
                ).capitaliza(juros=juros, inflacao=inflacao)

                fluxos.append(fluxo)

                self.logger.info("Adicionado fluxo {}".format(fluxo.jsondict()))

            # Se nao conseguimos parsear, ignoramos a linha
            except:
                raise

            # Se o resultado vier vazio houve um erro
            if fluxos.size == 0:
                resposta['erro'] = True
                resposta['errormsg'] = "Ocorreu um erro ao processar os dados"
                self.response.write(json.dumps(resposta))

        resposta['erro'] = False
        resposta['errormsg'] = None
        resposta['fluxos'] = fluxos.json()
        resposta['npv'] = fluxos.npv()
        resposta['irr'] = fluxos.irr()
        resposta['selic_periodo'] = fluxos.selic()
        resposta['npvplot'] = fluxos.npvplot()

        self.response.out.write(json.dumps(resposta))