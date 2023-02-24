import numpy as np

class Celeste:
    C = 10000
    def __init__(self):
        x , y = np.random.randint(300, 600), np.random.randint(300, 600)
        self.x = x
        self.y = y
        self.posicao = np.array([x, y])
    
    def aceleracao_sobre(self,s):
        direcao_aceleracao = self.posicao  - s
        direcao_aceleracao = direcao_aceleracao / np.linalg.norm(direcao_aceleracao)
        magnitude_aceleracao = Celeste.C / np.linalg.norm(self.posicao - s)**2
        aceleracao = magnitude_aceleracao * direcao_aceleracao
        return aceleracao


class Nave:
    def __init__(self):
        self.s0 = np.array([50,200])
        self.v0 = np.array([100, 0])
        self.a = np.array([0, 0.1])
        self.v = self.v0
        self.s = self.s0
