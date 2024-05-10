import pygame
import random
import time

class Cell():
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size
        self.is_alive = False
        self.hovered = False  # Флаг для отслеживания наведения мыши на клетку

    def draw(self, surface):
        color = (0, 255, 0) if self.hovered else (255, 255, 255) if self.is_alive else (0, 0, 0)
        pygame.draw.rect(surface, color, (self.x * self.size, self.y * self.size, self.size, self.size))
        pygame.draw.rect(surface, (10, 10, 10), (self.x * self.size, self.y * self.size, self.size, self.size), 1) 

    def check_hover(self, pos):
        # Проверка, находится ли позиция мыши над клеткой
        x, y = pos
        cell_rect = pygame.Rect(self.x * self.size, self.y * self.size, self.size, self.size)
        self.hovered = cell_rect.collidepoint(x, y)


class GameOfLife():
    def __init__(self, width, height, cell_size):
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.grid = [[Cell(x, y, cell_size) for x in range(width)] for y in range(height)]
        self.mouse_coords = (0, 0)
    
    def block2x2(self, x, y):
        pattern = [
            (0, 0), (1, 0),
            (0, 1), (1, 1),
        ]
        
        for dx, dy in pattern:
            new_x, new_y = x + dx, y + dy
            if 0 <= new_x < self.width and 0 <= new_y < self.height:
                self.grid[new_y][new_x].is_alive = True

    def planer(self, x, y):
        pattern = [
            (0, 0), (2, 0),
            (1, 1), (2, 1),
            (1, 2),
        ]
        
        for dx, dy in pattern:
            new_x, new_y = x + dx, y + dy
            if 0 <= new_x < self.width and 0 <= new_y < self.height:
                self.grid[new_y][new_x].is_alive = True

    def z_to_planers(self, x, y):
        pattern = [
        (0, 0), (1, 0), (2, 0), (3, 0), (4, 0),
                                (3, 1),
                        (2, 2),
                (1, 3),    
        (0, 4), (1, 4), (2, 4), (3, 4), (4, 4), 
        ]
        
        for dx, dy in pattern:
            new_x, new_y = x + dx, y + dy
            if 0 <= new_x < self.width and 0 <= new_y < self.height:
                self.grid[new_y][new_x].is_alive = True

    def randomize_cells(self):
        for row in self.grid:
            for cell in row:
                cell.is_alive = bool(random.getrandbits(1))

    def update(self):
        new_grid = [[Cell(x, y, self.cell_size) for x in range(self.width)] for y in range(self.height)]

        for y, row in enumerate(self.grid):
            for x, cell in enumerate(row):
                neighbors = self.count_neighbors(x, y)
                new_grid[y][x].is_alive = self.apply_rules(cell.is_alive, neighbors)

        self.grid = new_grid

    def count_neighbors(self, x, y):
        neighbors = 0

        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue

                new_x, new_y = x + i, y + j

                if 0 <= new_x < self.width and 0 <= new_y < self.height:
                    neighbors += self.grid[new_y][new_x].is_alive

        return neighbors

    def apply_rules(self, current_state, neighbors):
        if current_state == 1 and (neighbors < 2 or neighbors > 3):
            return 0  # Условие для "живой" клетки
        elif current_state == 0 and neighbors == 3:
            return 1  # Условие для "мертвой" клетки, у которой ровно 3 соседа
        else:
            return current_state  # Клетка остается в том же состоянии

    def draw(self, surface):
        surface.fill((0, 0, 0))  
        for y, row in enumerate(self.grid):
            for x, cell in enumerate(row):
                cell.draw(surface)
    
        self.draw_cell_coordinates(surface, self.mouse_coords)  # Отрисовываем координаты клеток в углу
        pygame.display.flip()  

    def handle_mouse_motion(self, pos):
        for row in self.grid:
            for cell in row:
                cell.check_hover(pos)
        self.mouse_coords = pos 

    def draw_cell_coordinates(self, surface, mouse_coords):
        font = pygame.font.Font(None, 16)
        x, y = mouse_coords  # Получаем координаты мыши
        cell_coords = f"({x // self.cell_size}, {y // self.cell_size})"
        text_surface = font.render(cell_coords, True, (255, 255, 255))
        surface.blit(text_surface, (10, 10)) #x,y


class Admin():
    def __init__(self):
        self.game_paused = False
        self.last_space_press_time = 0
        self.build_mode = False
        self.current_cube_size = 2

    def check_delay(self):
        current_time = time.time()
        if current_time - self.last_space_press_time > 0.3:
            self.last_space_press_time = current_time
            return True
        return False

    def controls(self):
        global GAME_TIME
        keys = pygame.key.get_pressed()

        if keys[pygame.K_KP_PLUS]:
            GAME_TIME -= 50
            print(f"[NumPad +], delay: {GAME_TIME} | GAME_TIME: {GAME_TIME}")
        
        elif keys[pygame.K_KP_MINUS]:
            GAME_TIME += 50
            print(f"[NumPad -], delay: {GAME_TIME} | GAME_TIME: {GAME_TIME}")
        
        elif keys[pygame.K_SPACE]:
            if self.check_delay():
                if self.game_paused == False:
                    self.game_paused = True
                    print(f"[space] game: paused | game_paused: {self.game_paused}")
                elif self.game_paused == True:
                    self.game_paused = False
                    print(f"[space] game: resume | game_paused: {self.game_paused}")

        elif keys[pygame.K_r]:
            if self.check_delay():
                game.randomize_cells()
                print(f"[r] game: random cells | game.randomize_cells()")

        elif keys[pygame.K_c]: 
            if self.check_delay():
                for row in game.grid:
                    for cell in row:
                        cell.is_alive = False
                print(f"[с] game: clear all cells | cell.is_alive: False")

        elif keys[pygame.K_1]:
            x, y = game.mouse_coords
            game.block2x2(x // game.cell_size, y // game.cell_size)

        elif keys[pygame.K_2]:
            if self.check_delay():
                x, y = game.mouse_coords
                game.planer(x // game.cell_size, y // game.cell_size)

        elif keys[pygame.K_3]:
            if self.check_delay():
                x, y = game.mouse_coords
                game.z_2_planers(x // game.cell_size, y // game.cell_size)

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

admin = Admin()

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
    if not admin.game_paused:
        game.update()
    
    # Обновление экрана
    game.draw(screen)
    pygame.display.flip()

    # Задержка для контроля скорости обновления
    pygame.time.delay(GAME_TIME)