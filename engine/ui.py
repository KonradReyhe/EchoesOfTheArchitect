import pygame
import time

class Message:
    def __init__(self, text, duration=5.0, color=(255, 240, 200)):
        self.text = text
        self.duration = duration
        self.time_left = duration
        self.color = color
        self.font = pygame.font.SysFont("georgia", 28)  # Match UI standards
        
    def draw(self, screen, x, y):
        # Draw text with better shadow for readability
        shadow_surface = self.font.render(self.text, True, (0, 0, 0))
        text_surface = self.font.render(self.text, True, self.color)  # Use stored color
        
        # Draw shadow slightly offset
        screen.blit(shadow_surface, (x + 2, y + 2))
        # Draw main text
        screen.blit(text_surface, (x, y))
    
    def update(self, dt):
        self.time_left -= dt
    
    def is_expired(self):
        return self.time_left <= 0

class ChoiceBox:
    def __init__(self, font, options, callback):
        self.font = font
        self.options = options
        self.callback = callback
        self.selected = 0
        self.x = 0  # Will be set when drawing
        self.y = 0  # Will be set when drawing

    def draw(self, screen, x, y):
        self.x = x  # Store position for click detection
        self.y = y
        for i, (text, _) in enumerate(self.options):
            color = (255, 255, 0) if i == self.selected else (255, 240, 200)
            text_surface = self.font.render(text, True, color)
            screen.blit(text_surface, (x, y + i * 30))

    def handle_click(self, pos):
        for i, (_, choice_id) in enumerate(self.options):
            option_rect = pygame.Rect(
                self.x, 
                self.y + i * 30,
                300,  # width of clickable area
                25   # height of clickable area
            )
            if option_rect.collidepoint(pos):
                if self.callback:
                    self.callback(choice_id)
                return True
        return False

    def handle_event(self, event):
        """Legacy method - redirects to handle_click for compatibility"""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            return self.handle_click(event.pos)
        return False 