import numpy as np

class Celeste:
    C = 10000
    corpos_celestes = []
    def __init__(self):
        x , y = np.random.randint(300, 600), np.random.randint(300, 600)
        self.x = x
        self.y = y
        self.posicao = np.array([x, y])
        Celeste.corpos_celestes.append(self)
    
    def aceleracao_gravitacional(self,s):
        direcao_aceleracao = self.posicao  - s
        direcao_aceleracao = direcao_aceleracao / np.linalg.norm(direcao_aceleracao)
        magnitude_aceleracao = Celeste.C / np.linalg.norm(self.posicao - s)**2
        aceleracao = magnitude_aceleracao * direcao_aceleracao
        return aceleracao
    
    @classmethod
    def gera_corpos(cls, nivel):
        if nivel > 4:
            nivel = 4
        for i in range(nivel):
            Celeste()

    @classmethod
    def limpa_corpos(cls):
        cls.corpos_celestes = []

class Nave:
    def __init__(self):
        self.s0 = np.array([50,200])
        self.v0 = np.array([100, 0])
        self.a = np.array([0, 0.0])
        self.v = self.v0
        self.s = self.s0

class Repulsor:
    C = 10000
    corpos_repulsores = []
    def __init__(self):
        x , y = np.random.randint(300, 600), np.random.randint(300, 600)
        self.x = x
        self.y = y
        self.posicao = np.array([x, y])
        Repulsor.corpos_repulsores.append(self)
    
    def aceleracao_repulsora(self,s):
        direcao_aceleracao = self.posicao  - s
        direcao_aceleracao = direcao_aceleracao / np.linalg.norm(direcao_aceleracao)
        direcao_aceleracao *= -1
        magnitude_aceleracao = Celeste.C / np.linalg.norm(self.posicao - s)**2
        aceleracao = magnitude_aceleracao * direcao_aceleracao
        return aceleracao
    
    @classmethod
    def gera_corpos(cls, nivel):
        if nivel > 10:
            nivel = 10
        if nivel > 4:
            nivel -=4 
            for i in range(nivel):
                Repulsor()

    @classmethod
    def limpa_corpos(cls):
        cls.corpos_repulsores = []
