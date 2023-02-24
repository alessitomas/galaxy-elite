import pygame
import numpy as np

pygame.init()

# Tamanho da tela e definição do FPS
screen = pygame.display.set_mode((800, 800))
clock = pygame.time.Clock()

FPS = 60  # Frames per Second
BLACK = (0, 0, 0)

assets = {
    "inicio": pygame.image.load("imagens/inicio.png"),
    "background": pygame.image.load("imagens/space.jpg"),
    "personagem": pygame.image.load("imagens/spaceship.png"),
    "celeste": pygame.image.load("imagens/black_hole.png"),
    "alien": pygame.image.load("imagens/alien2.png"),
    "fim": pygame.image.load("imagens/fim.png")
}

assets['background'] = pygame.transform.scale(assets['background'], (800, 800))
assets['personagem'] = pygame.transform.scale(assets['personagem'], (70, 70))
assets['personagem'] = pygame.transform.rotate(assets['personagem'], 270)
assets['celeste'] = pygame.transform.scale(assets['celeste'], (50, 50))
assets['alien'] = pygame.transform.scale(assets['alien'], (80, 80))

tiro = pygame.Surface((12, 12))
tiro.fill((0, 255, 0))

x1_celeste = np.random.randint(300, 600)
y1_celeste = np.random.randint(300, 600)
c1_celeste = np.array([x1_celeste, y1_celeste])

x2_celeste = np.random.randint(300, 600)
y2_celeste = np.random.randint(300, 600)
c2_celeste = np.array([x2_celeste, y2_celeste])

x1_alien = np.random.randint(600,750)
y1_alien = np.random.randint(400,600)


state = {
    "x1_celeste": x1_celeste,
    "y1_celeste": y1_celeste,
    "c1_celeste": np.array([x1_celeste, y1_celeste]),
    "x2_celeste": x2_celeste,
    "y2_celeste": y2_celeste,
    "c2_celeste": np.array([x2_celeste, y2_celeste]),
    "x1_alien": x1_alien,
    "y1_alien": y1_alien,
    "tela": 0
}

s_nave = np.array([50,200])
v0 = np.array([100, 0])
a = np.array([0, 0.1])
v = v0
s = np.array([80,230])

C = 14000


rodando = True
tentativas = 0
soltei = False
deu_tiro = True

while rodando:

    pos = pygame.mouse.get_pos()

    if state['tela'] == 0:
        screen.blit(assets['inicio'], (0, 0))
        pygame.display.update()
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                rodando = False

            if event.type == pygame.MOUSEBUTTONUP and pos[0] > 265 and pos[0] < 599 and pos[1] > 559 and pos[1] < 629:
                state['tela'] = 1

    if state['tela'] == 1:
        screen.blit(assets['background'], (0, 0))
        screen.blit(assets['celeste'], state['c1_celeste'])
        screen.blit(assets['celeste'], state['c2_celeste'])
        screen.blit(assets['alien'], (state['x1_alien'], state['y1_alien']))
        screen.blit(tiro, s)
        screen.blit(assets['personagem'], s_nave)

        font = pygame.font.SysFont("arialblack", 20)
        text = font.render("Tentativas: " + str(tentativas), True, (255, 255, 255))
        screen.blit(text, (10, 10))

        pygame.display.update()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                rodando = False

            # se o botao do mouse for solto e a posição do tiro estiver sendo atualizada, eu solto o tiro e atualizo o numero de tentativas
            if event.type == pygame.MOUSEBUTTONUP:

                if not soltei:
                    deu_tiro = False
                    vetor_direcao = pygame.mouse.get_pos() - s_nave
                    v = vetor_direcao / np.linalg.norm(vetor_direcao) * 80
                    boost_velo = np.random.randn(1)
                    v *= (boost_velo/10 +1)
                    soltei = True

        if s[0]<10 or s[0]>790 or s[1]<10 or s[1]>790: # Se eu chegar ao limite da tela, reinicio a posição do personagem
            soltei = False
            s = [80,230]
            v = v0

            tentativas += 1

            # verificar se a nave nao esta em orbita infinitamente
            if np.linalg.norm(s - np.array([state['x1_celeste'], state['y1_celeste']])) < 60:
                state['x1_celeste'] = np.random.randint(300, 600)
                state['y1_celeste'] = np.random.randint(300, 600)
                state['c1_celeste'] = np.array([state['x1_celeste'], state['y1_celeste']])
   

        clock.tick(FPS)

        if soltei:
            deu_tiro = True
            # celeste 1
            direcao_a_c1 = state['c1_celeste']  - s
            direcao_a_c1 = direcao_a_c1 / np.linalg.norm(direcao_a_c1)
            mag_a_c1 = C / np.linalg.norm(state['c1_celeste'] - s)**2
            a_c1 = mag_a_c1 * direcao_a_c1
            
            # celeste 2
            direcao_a_c2 = state['c2_celeste']  - s
            direcao_a_c2 = direcao_a_c2 / np.linalg.norm(direcao_a_c2)
            mag_a_c2 = C / np.linalg.norm(state['c2_celeste'] - s)**2
            a_c2 = mag_a_c2 * direcao_a_c2

            # resultante 
            a = a_c1 + a_c2
            v = v + a
            s = s + 0.1 * v

        # colisão
        if np.linalg.norm(s - np.array([state['x1_alien'], state['y1_alien']])) < 20:
            state['tela'] = 2

    if state['tela'] == 2:
        screen.blit(assets['fim'], (0, 0))

            # mostrar uma mensagem de fim de jogo com o numero total de tentativas
        font = pygame.font.SysFont("arialblack", 50)

        text = font.render("Parabéns!", True, (255, 255, 255))
        text_rect = text.get_rect(center=(400, 100))
        screen.blit(text, text_rect)

        font = pygame.font.SysFont("arial", 45)

        if tentativas >= 1:

            text = font.render("Você acertou o alien em " + str(1 + tentativas) + " tentativa(s)!", True, (255, 255, 255))
            text_rect = text.get_rect(center=(400, 200))
            screen.blit(text, text_rect)
        
        elif tentativas == 0:
            text = font.render("Você acertou o alien em " + str(1 + tentativas) + " tentativa!", True, (255, 255, 255))
            text_rect = text.get_rect(center=(400, 200))
            screen.blit(text, text_rect)
        

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                rodando = False

            # Reiniciar o jogo
            if event.type == pygame.MOUSEBUTTONUP and pos[0] > 272 and pos[0] < 550 and pos[1] > 414 and pos[1] < 483:
                state['tela'] = 1
                tentativas = 0
                soltei = False
                s = [80,230]
                v = v0

                x1_celeste = np.random.randint(300, 600)
                y1_celeste = np.random.randint(300, 600)
                state['c1_celeste'] = np.array([x1_celeste, y1_celeste])

                x2_celeste = np.random.randint(300, 600)
                y2_celeste = np.random.randint(300, 600)
                state['c2_celeste'] = np.array([x2_celeste, y2_celeste])

                x1_alien = np.random.randint(600, 750)
                y1_alien = np.random.randint(400, 600)
                state['x1_alien'] = x1_alien
                state['y1_alien'] = y1_alien
                


            # Sair do jogo
            if event.type == pygame.MOUSEBUTTONUP and pos[0] > 273 and pos[0] < 550 and pos[1] > 544 and pos[1] < 614:
                rodando = False


        pygame.display.update()
