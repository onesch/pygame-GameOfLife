import pygame
import random
from classes.cell import Cell
from patterns.block2x2 import block2x2_pattern
from patterns.planer import planer_pattern
from patterns.z_to_planers import z_to_planers_pattern


class GameOfLife:
    def __init__(self, game_mode, width, height, cell_size):
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.game_mode = game_mode
        self.grid = [
            [Cell(x, y, cell_size)
             for x in range(width)] for y in range(height)
        ]
        self.previous_states = [
            [False for x in range(width)] for y in range(height)
        ]
        self.mouse_coords = (0, 0)

    def block2x2(self, x, y):
        for dx, dy in block2x2_pattern:
            new_x, new_y = x + dx, y + dy
            if 0 <= new_x < self.width and 0 <= new_y < self.height:
                self.grid[new_y][new_x].is_alive = True

    def planer(self, x, y):
        for dx, dy in planer_pattern:
            new_x, new_y = x + dx, y + dy
            if 0 <= new_x < self.width and 0 <= new_y < self.height:
                self.grid[new_y][new_x].is_alive = True

    def z_to_planers(self, x, y):
        for dx, dy in z_to_planers_pattern:
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
                new_grid[y][x].is_alive = self.apply_rules(
                    cell.is_alive, neighbors)

        self.previous_states = [
            [cell.is_alive for cell in row] for row in self.grid
        ]

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
        if current_state == 1 and neighbors < 2 or neighbors > 3:
            return 0  # Условие для "живой" клетки
        elif current_state == 0 and neighbors == 3:
            return 1  # Условие для "мертвой" клетки, у которой ровно 3 соседа
        else:
            return current_state  # Клетка остается в том же состоянии

    def draw(self, surface):
        surface.fill((0, 0, 0))
        for y, row in enumerate(self.grid):
            for x, cell in enumerate(row):
                if self.game_mode == "base":
                    # if cell.is_alive:
                    cell.color = (255, 255, 255)  # white cell all

                elif self.game_mode == "statistic":
                    # if cell.is_alive:
                    if cell.is_alive == self.previous_states[y][x]:
                        cell.color = (0, 0, 255)  # blue cell frozen
                    else:
                        cell.color = (255, 0, 0)  # red cell in move
                cell.draw(surface)

        self.draw_info(surface, self.mouse_coords)
        pygame.display.flip()

    def handle_mouse_motion(self, pos):
        for row in self.grid:
            for cell in row:
                cell.check_hover(pos)
        self.mouse_coords = pos

    def draw_info(self, surface, mouse_coords):
        font = pygame.font.Font(None, 16)
        x, y = mouse_coords
        cell_coords = f"({x // self.cell_size}, {y // self.cell_size})"

        total_cells = 0
        static_cells = 0
        dynamic_cells = 0

        for y, row in enumerate(self.grid):
            for x, cell in enumerate(row):
                if cell.is_alive:
                    total_cells += 1
                    if cell.is_alive == self.previous_states[y][x]:
                        static_cells += 1
                    else:
                        dynamic_cells += 1

        info_text = (
            f"coords: {cell_coords}\n"
            f"total: {total_cells}\n"
            f"frozen: {static_cells}\n"
            f"in move: {dynamic_cells}"
        )

        y_offset = 10
        for line in info_text.split('\n'):
            color = (255, 255, 255)
            if "frozen" in line:
                color = (0, 0, 255)  # text frozen
            elif "in move" in line:
                color = (255, 0, 0)  # text in move
            text_surface = font.render(line, True, color)
            surface.blit(text_surface, (10, y_offset))
            y_offset += 20
