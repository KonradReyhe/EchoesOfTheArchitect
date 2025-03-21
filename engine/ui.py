import pygame
import time

class Message:
    def __init__(self, text, duration=3, font_size=24, color=(255, 255, 255)):
        self.text = text
        self.start_time = time.time()
        self.duration = duration
        self.font_size = font_size
        self.color = color
        self.font = pygame.font.SysFont("georgia", self.font_size)

    def is_expired(self):
        return time.time() - self.start_time > self.duration

    def draw(self, screen, x, y):
        surface = self.font.render(self.text, True, self.color)
        screen.blit(surface, (x, y)) 