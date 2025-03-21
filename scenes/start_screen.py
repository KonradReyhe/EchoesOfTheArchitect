import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT

class StartScreen:
    def __init__(self, scene_manager):
        self.scene_manager = scene_manager
        self.background = pygame.image.load("assets/images/backgrounds/title_screen.png")
        # Scale background to fit screen
        self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.font = pygame.font.SysFont("georgia", 64)
        self.small_font = pygame.font.SysFont("georgia", 32)  # Made slightly larger
        self.clicked = False

    def draw_text_with_shadow(self, screen, text, font, color, position):
        # Draw dark background box
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=(SCREEN_WIDTH//2, position))
        padding = 20
        
        bg_rect = pygame.Rect(
            text_rect.left - padding,
            text_rect.top - padding//2,
            text_rect.width + padding * 2,
            text_rect.height + padding
        )
        pygame.draw.rect(screen, (0, 0, 0, 128), bg_rect, border_radius=10)
        pygame.draw.rect(screen, (20, 20, 20, 128), bg_rect, 2, border_radius=10)  # Border
        
        # Draw text
        screen.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.clicked = True

    def update(self):
        if self.clicked:
            from scenes.garden import GardenScene
            from game_state import GameState
            game_state = GameState()
            self.scene_manager.switch_to(GardenScene(game_state, self.scene_manager))

    def draw(self, screen):
        screen.blit(self.background, (0, 0))

        # Draw text with shadow boxes
        self.draw_text_with_shadow(
            screen,
            "Echoes of the Architect",
            self.font,
            (255, 240, 200),  # Warm white color
            180
        )

        self.draw_text_with_shadow(
            screen,
            "A journey not of conquest, but of return.",
            self.small_font,
            (220, 220, 220),
            270
        )

        self.draw_text_with_shadow(
            screen,
            "Click to begin",
            self.small_font,
            (200, 200, 255),  # Slight blue tint
            500
        )

# Make sure the class is available for import
__all__ = ['StartScreen'] 