import pygame
import random
import sys
sys.setrecursionlimit(2000)

LARGURA = 400
ALTURA = 400

PRETO = (0, 0, 0)
VERDE = (0, 255, 0)
VERMELHO = (255, 0, 0)

TAMANHO = 20

FPS = 60

pygame.init()

tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Cobrinha DFS")

controle_fps = pygame.time.Clock()

cobra_inicio_x = LARGURA // 2
cobra_inicio_y = ALTURA // 2

cobra_velocidade_x = 0
cobra_velocidade_y = TAMANHO

corpo_cobra = []
comprimento_cobra = 1

comida_x = 0
comida_y = 0

pilha_caminho = []

quadrados_percorridos = 0

pontuacao = 0

fonte = pygame.font.Font(None, 36)


def atualizar_textos():
    global pontuacao_texto, quadrados_texto
    pontuacao_texto = fonte.render("Pontuação: " + str(pontuacao), True, VERDE)
    quadrados_texto = fonte.render("Quadrados: " + str(quadrados_percorridos), True, VERDE)


atualizar_textos()


def gerar_comida():
    global comida_x, comida_y
    while True:
        comida_x = round(random.randrange(0, LARGURA - TAMANHO) / 20.0) * 20.0
        comida_y = round(random.randrange(0, ALTURA - TAMANHO) / 20.0) * 20.0
        # Verifica se a comida não está no corpo da cobra
        if (comida_x, comida_y) not in [(segmento[0], segmento[1]) for segmento in corpo_cobra]:
            break


def dfs(cobra_x, cobra_y, destino_x, destino_y, visitados, corpo_atual):
    if (cobra_x, cobra_y) == (destino_x, destino_y):
        return True

    visitados.add((cobra_x, cobra_y))

    movimentos = [(TAMANHO, 0), (-TAMANHO, 0), (0, TAMANHO), (0, -TAMANHO)]

    for movimento in movimentos:
        nova_x = cobra_x + movimento[0]
        nova_y = cobra_y + movimento[1]

        if nova_x >= LARGURA or nova_x < 0 or nova_y >= ALTURA or nova_y < 0:
            continue

        if (nova_x, nova_y) in corpo_atual:
            continue

        if (nova_x, nova_y) in visitados:
            continue

        if dfs(nova_x, nova_y, destino_x, destino_y, visitados, corpo_atual):
            pilha_caminho.append((movimento[0], movimento[1]))
            return True

    return False


def mover_cobra():
    global cobra_inicio_x, cobra_inicio_y, cobra_velocidade_x, cobra_velocidade_y
    global quadrados_percorridos

    if not pilha_caminho:
        dfs(cobra_inicio_x, cobra_inicio_y, comida_x, comida_y, set(), set(tuple(c) for c in corpo_cobra))

    if pilha_caminho:
        movimento = pilha_caminho.pop()
        cobra_velocidade_x, cobra_velocidade_y = movimento[0], movimento[1]

    cobra_inicio_x += cobra_velocidade_x
    cobra_inicio_y += cobra_velocidade_y

    quadrados_percorridos += 1
    atualizar_textos()


def mostrar_pontuacao():
    tela.blit(pontuacao_texto, (10, 10))
    tela.blit(quadrados_texto, (10, 40))


# Inicializa a primeira comida
gerar_comida()

jogo_em_andamento = True
while jogo_em_andamento:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            jogo_em_andamento = False

    mover_cobra()

    if cobra_inicio_x >= LARGURA or cobra_inicio_x < 0 or cobra_inicio_y >= ALTURA or cobra_inicio_y < 0:
        jogo_em_andamento = False

    if cobra_inicio_x == comida_x and cobra_inicio_y == comida_y:
        gerar_comida()
        comprimento_cobra += 1
        pontuacao += 1
        atualizar_textos()

    if comprimento_cobra > (LARGURA / TAMANHO * ALTURA / TAMANHO):
        jogo_em_andamento = False

    tela.fill(PRETO)
    mostrar_pontuacao()

    cabeca_cobra = [cobra_inicio_x, cobra_inicio_y]
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

print("Quantidade de Quadrados: ", quadrados_percorridos)
print("Pontuacao: ", pontuacao)
pygame.quit()
