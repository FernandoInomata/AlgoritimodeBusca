import pygame
import random
import sys
import heapq
sys.setrecursionlimit(2000)

LARGURA = 400
ALTURA = 400

FUNDO = (0, 0, 0)
PONTUACAO = (0, 255, 0)
COMIDA = (255, 0, 0)

TAMANHO = 20

FPS = 30

cobra_inicio_x = LARGURA // 2
cobra_inicio_y = ALTURA // 2

cobra_velocidade_x = 0
cobra_velocidade_y = TAMANHO

corpo_cobra = []
comprimento_cobra = 1

pilha_caminho = []

quadrados_percorridos = 0

def new_food():
    '''
    Função para gerar uma nova posição para a comida
    '''
    while True:
        comida_x = round(random.randrange(0, LARGURA - TAMANHO) / TAMANHO) * TAMANHO
        comida_y = round(random.randrange(0, ALTURA - TAMANHO) / TAMANHO) * TAMANHO
        # Verifica se a nova posição não está no corpo da cobra
        if (comida_x, comida_y) not in corpo_cobra:
            return comida_x, comida_y

def heuristica(x1, y1, x2, y2):
    '''
    Função heurística para calcular a distância entre dois pontos

    :param x1: coordenada x do ponto 1
    :param y1: coordenada y do ponto 1
    :param x2: coordenada x do ponto 2
    :param y2: coordenada y do ponto 2
    '''
    return abs(x1 - x2) + abs(y1 - y2)

def a_star(cobra_x, cobra_y, destino_x, destino_y):
    '''
    Função para calcular o caminho entre a cabeça da cobra e a comida usando o algoritmo A*

    :param cobra_x: coordenada x da cabeça da cobra
    :param cobra_y: coordenada y da cabeça da cobra
    :param destino_x: coordenada x da comida
    :param destino_y: coordenada y da comida
    '''
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
                path.append(current)
                current = came_from[current]
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

            tentative_g_score = g_score.get(current, float('inf')) + TAMANHO
            if (nova_x, nova_y) not in g_score or tentative_g_score < g_score[(nova_x, nova_y)]:
                came_from[(nova_x, nova_y)] = current
                g_score[(nova_x, nova_y)] = tentative_g_score
                f_score[(nova_x, nova_y)] = tentative_g_score + heuristica(nova_x, nova_y, destino_x, destino_y)
                heapq.heappush(open_list, (f_score[(nova_x, nova_y)], (nova_x, nova_y)))

    return []

def mover_cobra():
    '''
    Função para mover a cobra
    '''
    global cobra_inicio_x, cobra_inicio_y, pilha_caminho, jogo_em_andamento, quadrados_percorridos

    movimentos = [(TAMANHO, 0), (-TAMANHO, 0), (0, TAMANHO), (0, -TAMANHO)]

    valida_colisão = corpo_cobra.copy()
    if len(valida_colisão) > 0:
        valida_colisão.pop(-1)
    if (cobra_inicio_x, cobra_inicio_y) in valida_colisão:
        jogo_em_andamento = False
        return

    if cobra_inicio_x >= LARGURA or cobra_inicio_x < 0 or cobra_inicio_y >= ALTURA or cobra_inicio_y < 0:
        jogo_em_andamento = False
        return

    if pilha_caminho:
        proximo_x, proximo_y = pilha_caminho.pop(0)
        cobra_inicio_x = proximo_x
        cobra_inicio_y = proximo_y
    else:
        pilha_caminho = a_star(cobra_inicio_x, cobra_inicio_y, comida_x, comida_y)
        if not pilha_caminho:
            for movimento in movimentos:
                nova_x = cobra_inicio_x + movimento[0]
                nova_y = cobra_inicio_y + movimento[1]

                if (
                    0 <= nova_x < LARGURA and
                    0 <= nova_y < ALTURA and
                    (nova_x, nova_y) not in corpo_cobra
                ):
                    cobra_inicio_x = nova_x
                    cobra_inicio_y = nova_y
                    break

    corpo_cobra.append((cobra_inicio_x, cobra_inicio_y))
    if len(corpo_cobra) > comprimento_cobra:
        del corpo_cobra[0]
    quadrados_percorridos += 1

def mostrar_pontuacao():
    '''
    Função para mostrar a pontuação na tela
    '''
    texto_pontuacao = fonte.render("Pontuação: " + str(pontuacao), True, PONTUACAO)
    tela.blit(texto_pontuacao, (10, 10))

    texto_quadrados = fonte.render("Quadrados: " + str(quadrados_percorridos), True, PONTUACAO)
    tela.blit(texto_quadrados, (10, 40))

pygame.init()

comida_x, comida_y = new_food()

tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Cobrinha A*")

controle_fps = pygame.time.Clock()

pontuacao = 0
fonte = pygame.font.Font(None, 36)

jogo_em_andamento = True
pilha_caminho = []
while jogo_em_andamento:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            jogo_em_andamento = False

    mover_cobra()

    if cobra_inicio_x == comida_x and cobra_inicio_y == comida_y:
        comida_x, comida_y = new_food()
        comprimento_cobra += 1
        pontuacao += 1
        pilha_caminho = a_star(cobra_inicio_x, cobra_inicio_y, comida_x, comida_y)

    tela.fill(FUNDO)
    mostrar_pontuacao()

    for segmento in corpo_cobra:
        pygame.draw.rect(tela, PONTUACAO, [segmento[0], segmento[1], TAMANHO, TAMANHO])

    pygame.draw.rect(tela, COMIDA, [comida_x, comida_y, TAMANHO, TAMANHO])
    pygame.display.update()
    controle_fps.tick(FPS)
    
print("Pontuacao Total: ", pontuacao)
print("Quantidade de Quadrados: ", quadrados_percorridos)

pygame.quit()
