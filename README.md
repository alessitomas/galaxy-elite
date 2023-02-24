# 🌌 Galaxy Elite 🌌
Jogo criado por Leonardo Scarlato e Tomás Alessi utilizando o que aprendemos na matéria de Algebra Linear (vetores).

## O que é o Galaxy Elite?
Galaxy Elite é um jogo criado em pygame onde o usuário comanda uma espaçonave que está voltando para a Terra depois de uma de suas missões. No entanto, quando se aproxima do planeta, se depara com dois **buracos negros** que dificultam a chegada até a Terra. Logo, o jogador (viajante) deve encontrar uma maneira de chegar até o planeta com a menor quantidade possível de tentativas (jogadas).

## Como jogar?
**1.** Clone o repositório em sua IDE <br>
**2.** Instale as dependências do projeto (Pygame e Numpy)<br>
**3.** Execute o arquivo `main.py`


## Instruções
Para fazer a nave se movimentar, basta **clicar em um ponto na tela** o qual você gostaria que a nave fosse. Desta maneira, a nave irá percorrer até chegar ao ponto em que você, usuário, clicou. No entanto, saiba que **a direção pode ser afetada pela gravidade dos buracos negros** 😉

## Descrição matemática do modelo físico implementado
O modelo físico utilizado é baseado no movimento da nave no espaço.

No arquivo Classes foi definida a Classe nave que define posição inicial velocidade inicial e a aceleração da Nave. A aceleração inicia como um vetor [0,0] já que decimos que na galáxia elite as úncias acelerações que influenciariam a nave seriam. A atração gravitacional dos corpos celestes e a Repulção dos corpos repulsores.

Assim que se inicia uma fase e a nave é lançada sua velocidade sofre a interferência da aceleração dos corpos.
    Cálculo da aceleração gravitacional
        
        direcao_aceleracao = self.posicao  - s
        direcao_aceleracao = direcao_aceleracao / np.linalg.norm(direcao_aceleracao)
        magnitude_aceleracao = Celeste.C / np.linalg.norm(self.posicao - s)**2
        aceleracao = magnitude_aceleracao * direcao_aceleracao
        return aceleracao

**1.** Para decobrir o vetor que representa a direção da aceleração que será aplicada sobre a velocidade da nave, pegamos a posição [x,y] do copro celeste e subitraímos a posição [x,y] da nave.

**2.** Normalizamos esse vetor, dividindo ele pela sua norma, pois queremos extrair apenas a direção e não levar em consideração as intencidades.

**3.** Cãlculo da magnitude da aceleração gravitacional, usando a fórmula da aceleração gravitacional trocando os valores de constante gravitacional e massa da fonte de campo por uma constante *C*.

**4.** Multiplicando o direção pela magnitude temos o vetor final da aceleração gravitacional que esse copro celeste irá influenciar a nave

**5.** Aceleração Resultante: depois de decobrir a aceleração de um corpo celeste 4-. Podemos somar todas as encontradas para chegar na aceleração resultante sobre a Nave.

Alteração na posição da Nave
    
    nave.v = nave.v + a
    nave.s = nave.s + 0.1 * nave.v

**6** A aceleração resultante irá somar com a velocidade<br>

**7** A velocidade uam vez influenciada irá ser reduzida a 10% (para melhor gameplay) e será somada coma posição da Nave

GIF da DEMO Galaxy-Elite
![alt text](refactor/imagens/galaxy-elite.gif)