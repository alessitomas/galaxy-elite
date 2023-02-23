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
    "alvo": pygame.image.load("imagens/terra.png"),
    "fim": pygame.image.load("imagens/fim.png")
}

assets['background'] = pygame.transform.scale(assets['background'], (800, 800))
assets['personagem'] = pygame.transform.scale(assets['personagem'], (70, 70))
assets['personagem'] = pygame.transform.rotate(assets['personagem'], 270)
assets['celeste'] = pygame.transform.scale(assets['celeste'], (50, 50))
assets['alvo'] = pygame.transform.scale(assets['alvo'], (90, 90))


x1_celeste = np.random.randint(300, 600)
y1_celeste = np.random.randint(300, 600)
c1_celeste = np.array([x1_celeste, y1_celeste])

x2_celeste = np.random.randint(300, 600)
y2_celeste = np.random.randint(300, 600)
c2_celeste = np.array([x2_celeste, y2_celeste])

x1_alvo = np.random.randint(600,750)
y1_alvo = np.random.randint(400,600)


state = {
    "x1_celeste": x1_celeste,
    "y1_celeste": y1_celeste,
    "c1_celeste": np.array([x1_celeste, y1_celeste]),
    "x2_celeste": x2_celeste,
    "y2_celeste": y2_celeste,
    "c2_celeste": np.array([x2_celeste, y2_celeste]),
    "x1_alvo": x1_alvo,
    "y1_alvo": y1_alvo,
    "tela": 0
}

s0 = np.array([50,200])
v0 = np.array([100, 0])
a = np.array([0, 0.1])
v = v0
s = s0

C = 100000



rodando = True
tentativas = 0
soltei = False

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
        screen.blit(assets['personagem'], s)
        screen.blit(assets['celeste'], state['c1_celeste'])
        screen.blit(assets['celeste'], state['c2_celeste'])
        screen.blit(assets['alvo'], (state['x1_alvo'], state['y1_alvo']))

        font = pygame.font.SysFont("arialblack", 20)
        text = font.render("Tentativas: " + str(tentativas), True, (255, 255, 255))
        screen.blit(text, (10, 10))

        pygame.display.update()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                rodando = False

            if event.type == pygame.MOUSEBUTTONUP:
                tentativas += 1

                if not soltei:
                    vetor_direcao = pygame.mouse.get_pos() - s0
                    v = vetor_direcao / np.linalg.norm(vetor_direcao) * 80
                    boost_velo = np.random.randn(1)
                    v *= (boost_velo/10 +1)
                    soltei = True

        if s[0]<10 or s[0]>790 or s[1]<10 or s[1]>790: # Se eu chegar ao limite da tela, reinicio a posição do personagem
            soltei = False
            s, v = s0, v0

            # verificar se a nave nao esta em orbita infinitamente
            if np.linalg.norm(s - np.array([state['x1_celeste'], state['y1_celeste']])) < 60:
                state['x1_celeste'] = np.random.randint(300, 600)
                state['y1_celeste'] = np.random.randint(300, 600)
                state['c1_celeste'] = np.array([state['x1_celeste'], state['y1_celeste']])
   

        clock.tick(FPS)

        if soltei:
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

        if np.linalg.norm(s - np.array([state['x1_alvo'], state['y1_alvo']])) < 40:
            state['tela'] = 2

    if state['tela'] == 2:
        screen.blit(assets['fim'], (0, 0))
        
        # mostrar uma mensagem de fim de jogo com o numero total de tentativas
        font = pygame.font.SysFont("arialblack", 50)

        text = font.render("Parabéns!", True, (255, 255, 255))
        text_rect = text.get_rect(center=(400, 100))
        screen.blit(text, text_rect)

        font = pygame.font.SysFont("arial", 45)

        text = font.render("Você acertou o alvo em " + str(tentativas) + " tentativa(s)!", True, (255, 255, 255))
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
                s, v = s0, v0

                x1_celeste = np.random.randint(300, 600)
                y1_celeste = np.random.randint(300, 600)
                state['c1_celeste'] = np.array([x1_celeste, y1_celeste])

                x2_celeste = np.random.randint(300, 600)
                y2_celeste = np.random.randint(300, 600)
                state['c2_celeste'] = np.array([x2_celeste, y2_celeste])

                x1_alvo = np.random.randint(600, 750)
                y1_alvo = np.random.randint(400, 600)
                state['x1_alvo'] = x1_alvo
                state['y1_alvo'] = y1_alvo
                


            # Sair do jogo
            if event.type == pygame.MOUSEBUTTONUP and pos[0] > 273 and pos[0] < 550 and pos[1] > 544 and pos[1] < 614:
                rodando = False


        pygame.display.update()
