import pygame
import time
import random

VelCobra = 100

Win_x = 720
Win_y = 480

Cor0 = pygame.Color(0, 0, 0)
Cor1 = pygame.Color(255, 255, 255)
CorR = pygame.Color(255, 0, 0)
CorG = pygame.Color(0, 255, 0)

pygame.init()
pygame.display.set_caption("SnakeGame_Busca")
Window = pygame.display.set_mode((Win_x, Win_y))
fps = pygame.time.Clock()


def IniciarJogo():
    PosSnake = [100, 50]
    BodySnake = [[100, 50], [90, 50]]
    PosFruit = GerarFruta()
    Direction = 'Dir'
    Score = 0
    return PosSnake, BodySnake, PosFruit, Direction, Score


def GerarFruta():
    return [
        random.randrange(1, (Win_x // 10)) * 10,
        random.randrange(1, (Win_y // 10)) * 10]


def AtualizarPosSnake(PosSnake, Direction):
    if Direction == "Up":
        PosSnake[1] -= 10
    elif Direction == 'Down':
        PosSnake[1] += 10
    elif Direction == "Esq":
        PosSnake[0] -= 10
    elif Direction == "Dir":
        PosSnake[0] += 10
    return PosSnake


def Mov(CurrentDirection, PosSnake, PosFruit):
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and CurrentDirection != 'Down':
                return 'Up'
            elif event.key == pygame.K_DOWN and CurrentDirection != 'Up':
                return 'Down'
            elif event.key == pygame.K_LEFT and CurrentDirection != 'Dir':
                return 'Esq'
            elif event.key == pygame.K_RIGHT and CurrentDirection != 'Esq':
                return 'Dir'

    return CurrentDirection


def CrescimentoSnake(BodySnake, PosSnake, PosFruit, Score):
    BodySnake.insert(0, list(PosSnake))
    if PosSnake == PosFruit:
        Score += 10
        PosFruit = GerarFruta()
    else:
        BodySnake.pop()
    return BodySnake, PosFruit, Score


def Collision(PosSnake, BodySnake):
    if (PosSnake[0] < 0 or PosSnake[0] >= Win_x or
            PosSnake[1] < 0 or PosSnake[1] >= Win_y):
        return True
    for Corpo in BodySnake[1:]:
        if PosSnake == Corpo:
            return True
    return False


def Renderizar(BodySnake, PosFruit, Score):
    Window.fill(Cor0)
    for pos in BodySnake:
        pygame.draw.rect(Window, CorG, pygame.Rect(pos[0], pos[1], 10, 10))
    pygame.draw.rect(Window, Cor1, pygame.Rect(PosFruit[0], PosFruit[1], 10, 10))
    Pontuacao(Score)
    pygame.display.update()


def Pontuacao(Score):
    Fonte = pygame.font.SysFont('times new roman', 20)
    HudScore = Fonte.render(f'Pontuação: {Score}', True, Cor1)
    Window.blit(HudScore, (10, 10))


def GameOver(Score):
    Fonte = pygame.font.SysFont('times new roman', 50)
    HudGameOver = Fonte.render(f'Sua Pontuação Final: {Score}', True, CorR)
    Window.blit(HudGameOver, HudGameOver.get_rect(center=(Win_x / 2, Win_y / 2)))
    pygame.display.flip()
    time.sleep(2)
    pygame.quit()
    quit()


def Main():
    PosSnake, BodySnake, PosFruit, Direction, Score = IniciarJogo()

    while True:
        Direction = Mov(Direction, PosSnake, PosFruit)
        PosSnake = AtualizarPosSnake(PosSnake, Direction)
        BodySnake, PosFruit, Score = CrescimentoSnake(BodySnake, PosSnake, PosFruit, Score)

        if Collision(PosSnake, BodySnake):
            GameOver(Score)

        Renderizar(BodySnake, PosFruit, Score)
        fps.tick(VelCobra)


if __name__ == "__main__":
    Main()
