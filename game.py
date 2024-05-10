from cell import Cell
import pygame
import random


class GameOfLife:
    def __init__(self, width, height, cell_size):
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.grid = [
            [Cell(x, y, cell_size) for x in range(width)] for y in range(height)
        ]
        self.mouse_coords = (0, 0)

    def block2x2(self, x, y):
        pattern = [
            (0, 0),
            (1, 0),
            (0, 1),
            (1, 1),
        ]

        for dx, dy in pattern:
            new_x, new_y = x + dx, y + dy
            if 0 <= new_x < self.width and 0 <= new_y < self.height:
                self.grid[new_y][new_x].is_alive = True

    def planer(self, x, y):
        pattern = [
            (0, 0),
            (2, 0),
            (1, 1),
            (2, 1),
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
        new_grid = [
            [Cell(x, y, self.cell_size) for x in range(self.width)]
            for y in range(self.height)
        ]

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

        self.draw_cell_coordinates(
            surface, self.mouse_coords
        )  # Отрисовываем координаты клеток в углу
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
        surface.blit(text_surface, (10, 10))  # x,y
