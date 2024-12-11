import pygame
import random
import sys
import heapq
sys.setrecursionlimit(2000)

LARGURA = 400
ALTURA = 400

PRETO = (0, 0, 0)
VERDE = (0, 255, 0)
VERMELHO = (255, 0, 0)

TAMANHO = 20

FPS = 30

pygame.init()

tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Cobrinha A*")

controle_fps = pygame.time.Clock()

cobra_inicio_x = LARGURA // 2
cobra_inicio_y = ALTURA // 2

cobra_velocidade_x = 0
cobra_velocidade_y = TAMANHO

corpo_cobra = []
comprimento_cobra = 1

comida_x = round(random.randrange(0, LARGURA - TAMANHO) / 20.0) * 20.0
comida_y = round(random.randrange(0, ALTURA - TAMANHO) / 20.0) * 20.0

pilha_caminho = []

# Função heurística (distância de Manhattan)
def heuristica(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)

# A* para encontrar o caminho
def a_star(cobra_x, cobra_y, destino_x, destino_y):
    open_list = []
    closed_list = set()
    came_from = {}
    g_score = { (cobra_x, cobra_y): 0 }
    f_score = { (cobra_x, cobra_y): heuristica(cobra_x, cobra_y, destino_x, destino_y) }

    heapq.heappush(open_list, (f_score[(cobra_x, cobra_y)], (cobra_x, cobra_y)))

    movimentos = [(TAMANHO, 0), (-TAMANHO, 0), (0, TAMANHO), (0, -TAMANHO)]

    while open_list:
        _, current = heapq.heappop(open_list)
        current_x, current_y = current

        if current == (destino_x, destino_y):
            path = []
            while current in came_from:
                current = came_from[current]
                path.append(current)
            path.reverse()
            return path

        closed_list.add(current)

        for movimento in movimentos:
            nova_x = current_x + movimento[0]
            nova_y = current_y + movimento[1]

            if nova_x >= LARGURA or nova_x < 0 or nova_y >= ALTURA or nova_y < 0:
                continue

            if (nova_x, nova_y) in corpo_cobra or (nova_x, nova_y) in closed_list:
                continue

            tentative_g_score = g_score.get((current_x, current_y), float('inf')) + TAMANHO
            if (nova_x, nova_y) not in g_score or tentative_g_score < g_score[(nova_x, nova_y)]:
                came_from[(nova_x, nova_y)] = (current_x, current_y)
                g_score[(nova_x, nova_y)] = tentative_g_score
                f_score[(nova_x, nova_y)] = tentative_g_score + heuristica(nova_x, nova_y, destino_x, destino_y)
                heapq.heappush(open_list, (f_score[(nova_x, nova_y)], (nova_x, nova_y)))

    return []

# Função para mover a cobra
def mover_cobra():
    global cobra_inicio_x, cobra_inicio_y, cobra_velocidade_x, cobra_velocidade_y, pilha_caminho

    # Verifica se não há caminho calculado e recalcula
    if not pilha_caminho:
        caminho = a_star(cobra_inicio_x, cobra_inicio_y, comida_x, comida_y)
        pilha_caminho = caminho

    if pilha_caminho:
        proximo = pilha_caminho.pop(0)
        cobra_velocidade_x, cobra_velocidade_y = proximo[0] - cobra_inicio_x, proximo[1] - cobra_inicio_y

    cobra_inicio_x += cobra_velocidade_x
    cobra_inicio_y += cobra_velocidade_y

pontuacao = 0

fonte = pygame.font.Font(None, 36)

pontuacao_texto = fonte.render("Pontuação: " + str(pontuacao), True, VERDE)

def mostrar_pontuacao():
    tela.blit(pontuacao_texto, (10, 10))

jogo_em_andamento = True
pilha_caminho = []  # Pilha para armazenar o caminho
while jogo_em_andamento:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            jogo_em_andamento = False

    mover_cobra()

    if cobra_inicio_x >= LARGURA or cobra_inicio_x < 0 or cobra_inicio_y >= ALTURA or cobra_inicio_y < 0:
        jogo_em_andamento = False

    if cobra_inicio_x == comida_x and cobra_inicio_y == comida_y:
        comida_x = round(random.randrange(0, LARGURA - TAMANHO) / 20.0) * 20.0
        comida_y = round(random.randrange(0, ALTURA - TAMANHO) / 20.0) * 20.0
        comprimento_cobra += 1
        pontuacao += 1
        pontuacao_texto = fonte.render("Pontuação: " + str(pontuacao), True, VERDE)

        # Recalcular o caminho para a nova comida
        pilha_caminho = []  # Resetar a pilha para recalcular o caminho

    if comprimento_cobra > (LARGURA/TAMANHO * ALTURA/TAMANHO):
        jogo_em_andamento = False

    tela.fill(PRETO)
    mostrar_pontuacao()

    cabeca_cobra = []
    cabeca_cobra.append(cobra_inicio_x)
    cabeca_cobra.append(cobra_inicio_y)
    corpo_cobra.append(cabeca_cobra)
    if len(corpo_cobra) > comprimento_cobra:
        del corpo_cobra[0]

    for segmento in corpo_cobra[:-1]:
        if segmento[0] == cabeca_cobra[0] and segmento[1] == cabeca_cobra[1]:
            jogo_em_andamento = False

    for segmento in corpo_cobra:
        pygame.draw.rect(tela, VERDE, [segmento[0], segmento[1], TAMANHO, TAMANHO])

    pygame.draw.rect(tela, VERMELHO, [comida_x, comida_y, TAMANHO, TAMANHO])

    pygame.display.update()

    controle_fps.tick(FPS)

pygame.quit()
