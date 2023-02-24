# Importando dependências
import pygame
import numpy as np
from classes import Celeste, Nave

# Inicializando pygame
pygame.init()

# Tamanho da tela e definição do FPS
screen = pygame.display.set_mode((800, 800))
clock = pygame.time.Clock()

FPS = 60  # Frames per Second
BLACK = (0, 0, 0)

# Carregando imagens usadas no jogo
assets = {
    "inicio": pygame.image.load("imagens/inicio.png"),
    "background": pygame.image.load("imagens/space.jpg"),
    "personagem": pygame.image.load("imagens/spaceship.png"),
    "celeste": pygame.image.load("imagens/black_hole.png"),
    "alvo": pygame.image.load("imagens/terra.png"),
    "fim": pygame.image.load("imagens/fim.png")
}

# Fazendo ajustes nas imagens
assets['background'] = pygame.transform.scale(assets['background'], (800, 800))
assets['personagem'] = pygame.transform.scale(assets['personagem'], (70, 70))
assets['personagem'] = pygame.transform.rotate(assets['personagem'], 270)
assets['celeste'] = pygame.transform.scale(assets['celeste'], (50, 50))
assets['alvo'] = pygame.transform.scale(assets['alvo'], (90, 90))


# Inicializando posicaoções dos buracos negros e do alvo (Terra)


x1_alvo = np.random.randint(600,750)
y1_alvo = np.random.randint(400,600)


# Definindo o estado inicial do jogo
state = {
    "nivel": 0,
    "x1_alvo": x1_alvo,
    "y1_alvo": y1_alvo,
    "tela": 0,
    "venceu": True
}


# Constante gravitacional
C = 10000

# Variáveis de controle
rodando = True
tentativas = 0
soltei = False
# cria os objetos celestres
c1 = Celeste()
c2 = Celeste()
# cira nave
nave = Nave()
# Loop principal
while rodando:
    pos = pygame.mouse.get_pos()    # Capturando a posicaoção do mouse dentro da tela do jogo

    if state['tela'] == 0:  # Tela inicial
        screen.blit(assets['inicio'], (0, 0))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                rodando = False

            if event.type == pygame.MOUSEBUTTONUP and pos[0] > 265 and pos[0] < 599 and pos[1] > 559 and pos[1] < 629:  
                # Se o usuário clicar em uma determinada faixa de coordenadas, as quais representam o botão de iniciar na tela inicial, o jogo começa (tela 1)
                state['tela'] = 1

    # Tela do jogo
    if state['tela'] == 1:
        # se passar de x tentativas termiana a fase
        if tentativas == 10:
            print(tentativas)
            print("entrei no de tentativas")
            state['tela'] = 2
            state['venceu'] = False

        # Carrega os itens do jogo (fundo, personagem, etc.)
        screen.blit(assets['background'], (0, 0))
        screen.blit(assets['personagem'], nave.s)
        screen.blit(assets['celeste'], c1.posicao)
        screen.blit(assets['celeste'], c2.posicao)
        screen.blit(assets['alvo'], (state['x1_alvo'], state['y1_alvo']))

        # Carrega o número de tentativas do usuário e as exibe na tela do jogo
        font = pygame.font.SysFont("arialblack", 20)
        text = font.render("Tentativas: " + str(tentativas), True, (255, 255, 255))
        screen.blit(text, (10, 10))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                rodando = False

            # A cada jogada, aumenta em 1 o número de tentativas
            if event.type == pygame.MOUSEBUTTONUP:
                

                if not soltei:
                    vetor_direcao = pygame.mouse.get_pos() - nave.s0
                    nave.v = vetor_direcao / np.linalg.norm(vetor_direcao) * 80
                    boost_velo = np.random.randn(1)
                    nave.v *= (boost_velo/10 +1)
                    soltei = True

        if nave.s[0]<10 or nave.s[0]>790 or nave.s[1]<10 or nave.s[1]>790: # Se eu chegar ao limite da tela, reinicio a posicaoção do personagem
            soltei = False
            nave.s, nave.v = nave.s0, nave.v0
            tentativas += 1


            # # Verificar se a nave nao esta em orbita infinitamente
            # if np.linalg.norm(s - np.array([state['x1_celeste'], state['y1_celeste']])) < 60:
            #     state['x1_celeste'] = np.random.randint(300, 600)
            #     state['y1_celeste'] = np.random.randint(300, 600)
            #     state['c1_celeste'] = np.array([state['x1_celeste'], state['y1_celeste']])
   

        clock.tick(FPS)

        # Se o usuário soltou o botão esquerdo do mouse, a nave é lançada
        if soltei:
            # Celeste 1
            a_c1 = c1.aceleracao_sobre(nave.s)
            a_c2 = c2.aceleracao_sobre(nave.s)
            # Resultante 
            a = a_c1 + a_c2
            
            nave.v = nave.v + a
            nave.s = nave.s + 0.1 * nave.v


        # Se a nave colidir com o alvo (Terra), o jogo acaba (tela 2)
        if np.linalg.norm(nave.s - np.array([state['x1_alvo'], state['y1_alvo']])) < 40:
            state['tela'] = 2
            state['nivel'] += 1
            tentativas += 1

    # Tela de fim de jogo
    if state['tela'] == 2:
        if state['venceu']:
            mensagem_header = "Parabéns!"
            mensagem_texto = "Você acertou o alvo em "
        else: 
            mensagem_header = "Você Falhou"
            mensagem_texto = "Você gastou todas suas "
        screen.blit(assets['fim'], (0, 0))  # Mostra a tela do final do jogo
        
        # Mostrar uma mensagem de fim de jogo com o numero total de tentativas
        font = pygame.font.SysFont("arialblack", 50)

        text = font.render(mensagem_header, True, (255, 255, 255))
        text_rect = text.get_rect(center=(400, 100))
        screen.blit(text, text_rect)

        font = pygame.font.SysFont("arial", 45)

        text = font.render(mensagem_texto + str(tentativas) + " tentativa(s)!", True, (255, 255, 255))
        text_rect = text.get_rect(center=(400, 200))
        screen.blit(text, text_rect)


        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                rodando = False

            # Reiniciar o jogo (reiniciando todas as variáveis)
            if event.type == pygame.MOUSEBUTTONUP and pos[0] > 272 and pos[0] < 550 and pos[1] > 414 and pos[1] < 483:
                state['tela'] = 1
                state['venceu'] = True
                tentativas = 0
                soltei = False
                nave.s, nave.v = nave.s0, nave.v0

                c1 = Celeste()
                c2 = Celeste()

                x1_alvo = np.random.randint(600, 750)
                y1_alvo = np.random.randint(400, 600)
                state['x1_alvo'] = x1_alvo
                state['y1_alvo'] = y1_alvo
                


            # Sair do jogo
            if event.type == pygame.MOUSEBUTTONUP and pos[0] > 273 and pos[0] < 550 and pos[1] > 544 and pos[1] < 614:
                rodando = False


        pygame.display.update()
