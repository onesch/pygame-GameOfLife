import pygame
import time


class Admin:
    def __init__(
        self, game, game_time
    ):  # Принимаем объект игры и значение GAME_TIME в качестве параметров
        self.game = game  # Сохраняем объект игры для дальнейшего использования
        self.game_paused = False
        self.last_space_press_time = 0
        self.build_mode = False
        self.current_cube_size = 2
        self.game_time = (
            game_time  # Сохраняем значение GAME_TIME для дальнейшего использования
        )

    def controls(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_KP_PLUS]:
            self.game_time -= 50
            print(f"[NumPad +], delay: {self.game_time} | GAME_TIME: {self.game_time}")

        elif keys[pygame.K_KP_MINUS]:
            self.game_time += 50
            print(f"[NumPad -], delay: {self.game_time} | GAME_TIME: {self.game_time}")

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
                self.game.randomize_cells()
                print(f"[r] game: random cells | game.randomize_cells()")

        elif keys[pygame.K_c]:
            if self.check_delay():
                for row in self.game.grid:
                    for cell in row:
                        cell.is_alive = False
                print(f"[с] game: clear all cells | cell.is_alive: False")

        elif keys[pygame.K_1]:
            x, y = self.game.mouse_coords
            self.game.block2x2(x // self.game.cell_size, y // self.game.cell_size)

        elif keys[pygame.K_2]:
            if self.check_delay():
                x, y = self.game.mouse_coords
                self.game.planer(x // self.game.cell_size, y // self.game.cell_size)

        elif keys[pygame.K_3]:
            if self.check_delay():
                x, y = self.game.mouse_coords
                self.game.z_to_planers(
                    x // self.game.cell_size, y // self.game.cell_size
                )

    def check_delay(self):
        current_time = time.time()
        if current_time - self.last_space_press_time > 0.3:
            self.last_space_press_time = current_time
            return True
        return False
