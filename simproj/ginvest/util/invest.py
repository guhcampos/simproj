class Investimento(object):

    def rentabilidade(valor, datainicial, datafinal, step=30):
        raise NotImplementedError("Method must be implemented on subclass")


class Poupanca(Investimento):
    
    def __init__(self, aniversario=01):

        self.aniversario = aniversario

    def rentabilidade(valor, datainicial, datafinal, step=30):
        pass



class TesouroDireto(Investimento):

    def __init__(self, maturity=None):

        if maturity is None:
            raise ValueError("You must pass a maturity")

class LTN(TesouroDireto):
    pass

class NTNf(TesouroDireto):
    pass

class LFT(TesouroDireto):
    pass

class NTNc(TesouroDireto):
    pass

class NTNb(TesouroDireto):
    pass

class NTNbPrincipal(TesouroDireto):
    pass


