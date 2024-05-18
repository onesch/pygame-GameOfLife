import pygame


class Cell:
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size
        self.is_alive = False
        self.hovered = False
        self.color = (255, 255, 255)

    def draw(self, surface):
        color = (self.color if self.is_alive else (0, 0, 0))

        if self.hovered:
            color = (255, 255, 0)

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
        mx, my = pos
        if (self.x * self.size <= mx < (self.x + 1) * self.size
                and self.y * self.size <= my < (self.y + 1) * self.size):
            self.hovered = True
        else:
            self.hovered = False
