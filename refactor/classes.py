import numpy as np

class Celeste:
    C = 10000 # Constante 
    corpos_celestes = [] # lista de corpos celestes
    def __init__(self):
        x , y = np.random.randint(300, 600), np.random.randint(300, 600)
        self.x = x # posicao de x
        self.y = y # posicao de y
        self.posicao = np.array([x, y]) # posicao de x e y
        Celeste.corpos_celestes.append(self)
    
    def aceleracao_gravitacional(self,s):
        # calcula a aceleração gravitacional sobre o corpo celes
        direcao_aceleracao = self.posicao  - s # vetor direção da aceleração
        direcao_aceleracao = direcao_aceleracao / np.linalg.norm(direcao_aceleracao) # normaliza o vetor direção
        magnitude_aceleracao = Celeste.C / np.linalg.norm(self.posicao - s)**2 # # magnitude da aceleração
        aceleracao = magnitude_aceleracao * direcao_aceleracao # vetor aceleração
        return aceleracao
    
    @classmethod
    def gera_corpos(cls, nivel): # gera corpos celestes aleatórios
        if nivel > 4: # limita o número de corpos gerados
            nivel = 4
        for i in range(nivel):
            Celeste()

    @classmethod
    def limpa_corpos(cls): # remove todos os corpos celestes da lista
        cls.corpos_celestes = []

class Nave:
    def __init__(self):
        self.s0 = np.array([50,200])  # posição inicial da nave
        self.v0 = np.array([100, 0])  # velocidade inicial da nave
        self.a = np.array([0.0, 0.0]) # aceleração inicial da nave
        self.v = self.v0 # velocidade atual da nave
        self.s = self.s0 # velocidade atual da nave

class Repulsor:
    C = 1500
    corpos_repulsores = []
    def __init__(self):
        x , y = np.random.randint(300, 600), np.random.randint(300, 600)
        self.x = x
        self.y = y
        self.posicao = np.array([x, y])
        Repulsor.corpos_repulsores.append(self)
    
    def aceleracao_repulsora(self,s): # calcula a aceleração repulsora sobre o corpo repulsor
        direcao_aceleracao = self.posicao  - s # vetor direção da aceleração
        direcao_aceleracao = direcao_aceleracao / np.linalg.norm(direcao_aceleracao) # normaliza o vetor direção
        direcao_aceleracao *= -1 # inverte a direção da aceleração
        magnitude_aceleracao = Celeste.C / np.linalg.norm(self.posicao - s)**2 # magnitude da aceleração
        aceleracao = magnitude_aceleracao * direcao_aceleracao # vetor aceleração
        return aceleracao
    
    @classmethod
    def gera_corpos(cls, nivel): # gera corpos celestes aleatórios
        if nivel > 10: # limita o número de corpos gerados
            nivel = 10
        if nivel > 4: # limita o nivel para gerar
            nivel -=4 
            for i in range(nivel):
                Repulsor()

    @classmethod
    def limpa_corpos(cls):
        cls.corpos_repulsores = [] # retira todos os repulsores
