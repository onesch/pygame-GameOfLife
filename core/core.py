import pygame
from classes.game import GameOfLife
from classes.admin import Admin

# Параметры
width, height = 900, 700
cell_size = 8  # 50
GAME_TIME = 100
GAME_MODE = "base"  # base # statistic

# Создание экрана
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Game of Life")

# Создание объекта игры
game = GameOfLife(GAME_MODE,
                  width // cell_size, height // cell_size,
                  cell_size)
game.randomize_cells()

# Создание объекта игрока, передача объекта игры и GAME_TIME
admin = Admin(game, GAME_TIME)


def start_game():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    x, y = event.pos
                    x //= cell_size
                    y //= cell_size
                    game.grid[y][x].is_alive = not game.grid[y][x].is_alive
            elif event.type == pygame.MOUSEMOTION:
                game.handle_mouse_motion(event.pos)

        admin.controls()

        # Передача текущего значения GAME_TIME
        # из объекта игрока в основной цикл
        GAME_TIME = admin.game_time

        if not admin.game_paused:
            game.update()

        # Обновление экрана
        game.draw(screen)
        pygame.display.flip()

        # Задержка для контроля
        # скорости обновления
        pygame.time.delay(GAME_TIME)
