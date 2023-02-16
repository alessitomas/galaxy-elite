import pygame
import numpy as np

pygame.init()

# Tamanho da tela e definição do FPS
screen = pygame.display.set_mode((800, 800))
clock = pygame.time.Clock()

FPS = 60  # Frames per Second
BLACK = (0, 0, 0)
COR_PERSONAGEM = (30, 200, 20)
COR_CELESTE = "red"

# Inicializar posicoes
# Celestes
c1_celeste = np.array([200,200])
c2_celeste = np.array([300,300])
C = 100000

s0 = np.array([50,200])
v0 = np.array([100, 0])
a = np.array([0, 0.1])
v = v0
s = s0

# Personagem
personagem = pygame.Surface((10, 10))  # Tamanho do personagem
personagem.fill(COR_PERSONAGEM)  # Cor do personagem
# Celeste
celeste = pygame.Surface((10, 10))  # Tamanho do personagem
celeste.fill(COR_CELESTE)  # Cor do personagem
soltei = False
#


rodando = True
while rodando:
    # Capturar eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False
            # handle MOUSEBUTTONUP
        if event.type == pygame.MOUSEBUTTONUP:
            if not soltei:
                vetor_direcao = pygame.mouse.get_pos() - s0
                v = vetor_direcao / np.linalg.norm(vetor_direcao) * 80
                boost_velo = np.random.randn(1)
                v *= (boost_velo/10 +1)
                soltei = True

    
    if s[0]<10 or s[0]>790 or s[1]<10 or s[1]>790: # Se eu chegar ao limite da tela, reinicio a posição do personagem
        soltei = False
        s, v = s0, v0


    # Controlar frame rate
    clock.tick(FPS)

    # Processar posicoes
    if soltei:
        
        # celeste 1
        direcao_a_c1 = c1_celeste  - s
        direcao_a_c1 = direcao_a_c1 / np.linalg.norm(direcao_a_c1)
        mag_a_c1 = C / np.linalg.norm(c1_celeste - s)**2
        a_c1 = mag_a_c1 * direcao_a_c1
        
        # celeste 2
        direcao_a_c2 = c2_celeste  - s
        direcao_a_c2 = direcao_a_c2 / np.linalg.norm(direcao_a_c2)
        mag_a_c2 = C / np.linalg.norm(c2_celeste - s)**2
        a_c2 = mag_a_c2 * direcao_a_c2

        # resultante 
        a = a_c1 + a_c2


        v = v + a
        s = s + 0.1 * v
    # Desenhar fundo
    screen.fill(BLACK)

    
    # Desenhar personagem
    rect_c1 = pygame.Rect(c1_celeste, (20, 20))  # First tuple is position, second is size.
    screen.blit(celeste, rect_c1)
    rect = pygame.Rect(s, (10, 10))  # First tuple is position, second is size.
    screen.blit(personagem, rect)
    rect_c2 = pygame.Rect(c2_celeste, (20, 20))  # First tuple is position, second is size.
    screen.blit(celeste, rect_c2)
    # Update!
    pygame.display.update()

# Terminar tela
pygame.quit()




