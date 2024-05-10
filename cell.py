import pygame


class Cell:
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size
        self.is_alive = False
        self.hovered = False  # Флаг для отслеживания наведения мыши на клетку

    def draw(self, surface):
        color = (
            (0, 255, 0)
            if self.hovered
            else (255, 255, 255) if self.is_alive else (0, 0, 0)
        )
        pygame.draw.rect(
            surface,
            color,
            (self.x * self.size, self.y * self.size, self.size, self.size),
        )
        pygame.draw.rect(
            surface,
            (10, 10, 10),
            (self.x * self.size, self.y * self.size, self.size, self.size),
            1,
        )

    def check_hover(self, pos):
        # Проверка, находится ли позиция мыши над клеткой
        x, y = pos
        cell_rect = pygame.Rect(
            self.x * self.size, self.y * self.size, self.size, self.size
        )
        self.hovered = cell_rect.collidepoint(x, y)
