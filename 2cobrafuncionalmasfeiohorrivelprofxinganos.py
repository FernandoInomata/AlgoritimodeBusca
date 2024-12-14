import pygame
import random
import sys
import heapq

sys.setrecursionlimit(2000)

# Game constants
LARGURA = 400
ALTURA = 400
FUNDO = (0, 0, 0)
PONTUACAO = (0, 255, 0)
COMIDA = (255, 0, 0)
TAMANHO = 20
FPS = 30


def new_food():
    '''
    Função para gerar uma nova posição para a comida
    '''


    while True:
        comida_x = round(random.randrange(0, LARGURA - TAMANHO) / TAMANHO) * TAMANHO
        comida_y = round(random.randrange(0, ALTURA - TAMANHO) / TAMANHO) * TAMANHO
        #Verificando se a comida estã no corpo da cobra
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
    
    #adiciona a cabe~ca da cobra na lista de prioridade
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

            #Calcula o custo do caminho
            tentative_g_score = g_score.get(current, float('inf')) + TAMANHO
            if (nova_x, nova_y) not in g_score or tentative_g_score < g_score[(nova_x, nova_y)]:
                came_from[(nova_x, nova_y)] = current
                g_score[(nova_x, nova_y)] = tentative_g_score
                f_score[(nova_x, nova_y)] = tentative_g_score + heuristica(nova_x, nova_y, destino_x, destino_y)
                heapq.heappush(open_list, (f_score[(nova_x, nova_y)], (nova_x, nova_y)))
    return []

# Setup for the first game (A* pathfinding)
cobra_inicio_x = LARGURA // 2
cobra_inicio_y = ALTURA // 2
corpo_cobra = []

comprimento_cobra = 1

pilha_caminho = []

comida_x, comida_y = new_food()

# Setup for the second game (DFS)
cobra2_inicio_x = LARGURA // 2
cobra2_inicio_y = ALTURA // 2
corpo_cobra2 = [(cobra2_inicio_x, cobra2_inicio_y)]
comprimento_cobra2 = 1
comida2_x = round(random.randrange(0, LARGURA - TAMANHO) / TAMANHO) * TAMANHO
comida2_y = round(random.randrange(0, ALTURA - TAMANHO) / TAMANHO) * TAMANHO
pilha_caminho2 = []

# DFS for the second game
def dfs(cobra_x, cobra_y, destino_x, destino_y, visitados):
    if (cobra_x, cobra_y) == (destino_x, destino_y):
        return True
    visitados.add((cobra_x, cobra_y))
    movimentos = [(TAMANHO, 0), (-TAMANHO, 0), (0, TAMANHO), (0, -TAMANHO)]
    for movimento in movimentos:
        nova_x = cobra_x + movimento[0]
        nova_y = cobra_y + movimento[1]
        if nova_x >= LARGURA or nova_x < 0 or nova_y >= ALTURA or nova_y < 0:
            continue
        if (nova_x, nova_y) in corpo_cobra2:
            continue
        if (nova_x, nova_y) in visitados:
            continue
        if dfs(nova_x, nova_y, destino_x, destino_y, visitados):
            pilha_caminho2.append((movimento[0], movimento[1]))
            return True
    return False

#Inicializar o jogo
pygame.init()

# Game loop
screen = pygame.display.set_mode((LARGURA * 2, ALTURA))
pygame.display.set_caption("Snake A* and DFS")

controle_fps = pygame.time.Clock()
font = pygame.font.Font(None, 36)

# Main loop
running = True
pontuacao1 = 0
pontuacao2 = 0
while running:
    screen.fill(FUNDO)

    # Handling events
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            running = False

    # Game 1: A* Pathfinding
    def move_cobra1():
        global cobra_inicio_x, cobra_inicio_y, pilha_caminho, corpo_cobra, comprimento_cobra, comida_x, comida_y, pontuacao1
        
        movimentos = [(TAMANHO, 0), (-TAMANHO, 0), (0, TAMANHO), (0, -TAMANHO)]

        #verifica se tem colisão com o corpo antes de adicionar a posição atual
        valida_colisao = corpo_cobra.copy()
        if len(valida_colisao) > 0:
            valida_colisao.pop(-1)
        if (cobra_inicio_x, cobra_inicio_y) in valida_colisao:
            print("Colisão")
            running = False
            return
        
        #Verifica colisão com as bordas
        if cobra_inicio_x >= LARGURA or cobra_inicio_x < 0 or cobra_inicio_y >= ALTURA or cobra_inicio_y < 0:
            print("Colisão")
            running = False
            return
        
        #Verifica se há um caminho disponível
        if pilha_caminho:
            proximo_x, proximo_y = pilha_caminho.pop(0)
            cobra_inicio_x = proximo_x
            cobra_inicio_y = proximo_y
        else:
            #calcula um novo caminho usando A*
            pilha_caminho = a_star(cobra_inicio_x, cobra_inicio_y, comida_x, comida_y)
            if not pilha_caminho:
                #Se não há caminho disponível, tenta mover para qualquer direção válida
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


        #Adiciona a nova posição no corpo da cobra
        corpo_cobra.append((cobra_inicio_x, cobra_inicio_y))
        if len(corpo_cobra) > comprimento_cobra:
            del corpo_cobra[0]
            
        if cobra_inicio_x == comida_x and cobra_inicio_y == comida_y:
            comida_x, comida_y = new_food()
            comprimento_cobra += 1
            pontuacao1 += 1
            pilha_caminho = a_star(cobra_inicio_x, cobra_inicio_y, comida_x, comida_y)        

    move_cobra1()
    
    # Drawing for game 1 (A* Pathfinding)
    for segmento in corpo_cobra:
        pygame.draw.rect(screen, PONTUACAO, [segmento[0], segmento[1], TAMANHO, TAMANHO])
    
    pygame.draw.rect(screen, COMIDA, [comida_x, comida_y, TAMANHO, TAMANHO])
    text1 = font.render(f"Pontuação A*: {pontuacao1}", True, (255, 255, 255))
    screen.blit(text1, (10, 10))

    # Game 2: DFS Pathfinding
    def move_cobra2():
        global cobra2_inicio_x, cobra2_inicio_y, pilha_caminho2, corpo_cobra2, comprimento_cobra2, comida2_x, comida2_y, pontuacao2
        if pilha_caminho2:
            movimento = pilha_caminho2.pop()
            cobra2_inicio_x += movimento[0]
            cobra2_inicio_y += movimento[1]
        else:
            dfs(cobra2_inicio_x, cobra2_inicio_y, comida2_x, comida2_y, set())

        
        corpo_cobra2.append((cobra2_inicio_x, cobra2_inicio_y))
        if len(corpo_cobra2) > comprimento_cobra2:
            del corpo_cobra2[0]
        if cobra2_inicio_x == comida2_x and cobra2_inicio_y == comida2_y:
            comida2_x = round(random.randrange(0, LARGURA - TAMANHO) / TAMANHO) * TAMANHO
            comida2_y = round(random.randrange(0, ALTURA - TAMANHO) / TAMANHO) * TAMANHO
            comprimento_cobra2 += 1
            pontuacao2 += 1

    move_cobra2()

    # Drawing for game 2 (DFS)
    for segmento in corpo_cobra2:
        pygame.draw.rect(screen, (0, 255, 0), [segmento[0] + LARGURA, segmento[1], TAMANHO, TAMANHO])
    pygame.draw.rect(screen, (255, 0, 0), [comida2_x + LARGURA, comida2_y, TAMANHO, TAMANHO])
    text2 = font.render(f"Pontuação DFS: {pontuacao2}", True, (255, 255, 255))
    screen.blit(text2, (LARGURA + 10, 10))

    pygame.display.update()
    controle_fps.tick(FPS)

pygame.quit()