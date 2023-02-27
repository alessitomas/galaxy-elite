# Importando dependências
import pygame
import numpy as np
from classes import Celeste, Nave, Repulsor

# Inicializando pygame
pygame.init()

# Inicializando mixer (efeitos sonoros e musica de fundo)
pygame.mixer.init()

pygame.mixer.music.load('assets/musica.mp3')
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.1)

efeito_passou = pygame.mixer.Sound(
    'assets/passou.mp3')
efeito_passou.set_volume(0.1)

efeito_foguete = pygame.mixer.Sound(
    'assets/foguete.mp3')
efeito_foguete.set_volume(0.01)

efeito_perdeu = pygame.mixer.Sound(
    'assets/game_over.mp3')
efeito_perdeu.set_volume(0.1)



# Tamanho da tela e definição do FPS
screen = pygame.display.set_mode((800, 800))
clock = pygame.time.Clock()

FPS = 60  # Frames per Second
BLACK = (0, 0, 0)

# Carregando assets usadas no jogo
assets = {
    "inicio": pygame.image.load("assets/inicio.png"),
    "background": pygame.image.load("assets/space.jpg"),
    "personagem": pygame.image.load("assets/spaceship.png"),
    "celeste": pygame.image.load("assets/black_hole.png"),
    "alvo": pygame.image.load("assets/terra.png"),
    "fim": pygame.image.load("assets/fim.png"),
    "repulsor": pygame.image.load("assets/repulsor.png"),
    "continuar": pygame.image.load("assets/homepage.png")
}

# Fazendo ajustes nas assets
assets['background'] = pygame.transform.scale(assets['background'], (800, 800))
assets['personagem'] = pygame.transform.scale(assets['personagem'], (70, 70))
assets['personagem'] = pygame.transform.rotate(assets['personagem'], 270)
assets['celeste'] = pygame.transform.scale(assets['celeste'], (50, 50))
assets['alvo'] = pygame.transform.scale(assets['alvo'], (90, 90))
assets['repulsor'] = pygame.transform.scale(assets['repulsor'], (50, 50))


# Inicializando posicaoções dos buracos negros e do alvo (Terra)


x1_alvo = np.random.randint(600,750)
y1_alvo = np.random.randint(400,600)


# Definindo o estado inicial do jogo
state = {
    "nivel": 1,
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
Celeste.gera_corpos(state['nivel'])

# cira nave
nave = Nave()
perdeu = True
foguete = True

# Loop principal do jogo
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
            state['tela'] = 2
            state['venceu'] = False
            state['nivel'] = 1

        # Carrega os itens do jogo (fundo, personagem, etc.)
        screen.blit(assets['background'], (0, 0))
        screen.blit(assets['personagem'], nave.s)
        for celeste in Celeste.corpos_celestes:
            screen.blit(assets['celeste'], celeste.posicao)
        for repulsor in Repulsor.corpos_repulsores:
            screen.blit(assets['repulsor'], repulsor.posicao)
        screen.blit(assets['alvo'], (state['x1_alvo'], state['y1_alvo']))

        # Carrega o número de tentativas do usuário e as exibe na tela do jogo
        font = pygame.font.SysFont("arialblack", 20)
        text = font.render("Tentativas: " + str(tentativas), True, (255, 255, 255))
        screen.blit(text, (10, 10))
        text1 = font.render("Nível: " + str(state['nivel']), True, (255, 255, 255))
        screen.blit(text1, (200, 10))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                rodando = False

            if event.type == pygame.MOUSEBUTTONUP:

                if foguete:
                    efeito_foguete.play()

                if not soltei:
                    vetor_direcao = pygame.mouse.get_pos() - nave.s0
                    nave.v = vetor_direcao / np.linalg.norm(vetor_direcao) * 80
                    boost_velo = np.random.randn(1)
                    nave.v *= (boost_velo/10 +1)
                    soltei = True

        # Se eu chegar ao limite da tela, reinicio a posicaoção do personagem
        if nave.s[0]<10 or nave.s[0]>790 or nave.s[1]<10 or nave.s[1]>790: 
            soltei = False
            nave.s, nave.v = nave.s0, nave.v0
            tentativas += 1
            efeito_foguete.stop()


        clock.tick(FPS)

        # Se o usuário soltou o botão esquerdo do mouse, a nave é lançada
        if soltei:

            a = np.array([0.0,0.0])
            # Calculo da aceleracao

            for celeste in Celeste.corpos_celestes:
                
                a +=celeste.aceleracao_gravitacional(nave.s)
                
            for repulsor in Repulsor.corpos_repulsores:
                a += repulsor.aceleracao_repulsora(nave.s)
            
            nave.v = nave.v + a
            nave.s = nave.s + 0.1 * nave.v

        # Se a nave colidir com o alvo (Terra), o jogo acaba (tela 2)
        if np.linalg.norm(nave.s - np.array([state['x1_alvo'], state['y1_alvo']])) < 40:
            state['tela'] = 2
            state['nivel'] += 1
            tentativas += 1

            efeito_foguete.stop()
            efeito_passou.play()

    # Tela de fim de jogo
    if state['tela'] == 2:
        if state['venceu']:
            mensagem_header = "Parabéns!"
            mensagem_texto = "Você acertou o alvo em "
            
            screen.blit(assets['continuar'], (0, 0))  # Mostra a tela de vitória
        else: 
            mensagem_header = "Você Falhou"
            mensagem_texto = "Você gastou todas suas "
            screen.blit(assets['fim'], (0, 0))  # Mostra a tela do final do jogo

            if perdeu:
                efeito_perdeu.play()
                perdeu = False
        
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
                
                Celeste.limpa_corpos()
                Celeste.gera_corpos(state['nivel'])
                Repulsor.limpa_corpos()
                Repulsor.gera_corpos(state['nivel'])
                x1_alvo = np.random.randint(600, 750)
                y1_alvo = np.random.randint(400, 600)
                state['x1_alvo'] = x1_alvo
                state['y1_alvo'] = y1_alvo
                


            # Sair do jogo
            if event.type == pygame.MOUSEBUTTONUP and pos[0] > 273 and pos[0] < 550 and pos[1] > 544 and pos[1] < 614:
                rodando = False


        pygame.display.update()
