import pygame
from game import GameOfLife
from admin import Admin

# Инициализация Pygame
pygame.init()

# Параметры
width, height = 900, 700
cell_size = 8
GAME_TIME = 100

# Создание объекта игры
game = GameOfLife(width // cell_size, height // cell_size, cell_size)
game.randomize_cells()

# Создание экрана
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Game of Life")

# Создание объекта администратора и передача объекта игры и значения GAME_TIME в конструктор
admin = Admin(game, GAME_TIME)

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

    # Передача текущего значения GAME_TIME из объекта администратора в основной цикл
    GAME_TIME = admin.game_time

    if not admin.game_paused:
        game.update()

    # Обновление экрана
    game.draw(screen)
    pygame.display.flip()

    # Задержка для контроля скорости обновления
    pygame.time.delay(GAME_TIME)
