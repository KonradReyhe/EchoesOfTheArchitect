import pygame
from engine.scene_base import Scene
from settings import SCREEN_WIDTH, SCREEN_HEIGHT

class BridgeScene(Scene):
    """Scene 4: Path of trials - Players navigate the bridge of choices."""
    
    def __init__(self, game_state, scene_manager):
        super().__init__(game_state, scene_manager)
        self.messages = []  # List to hold messages for the player
        self.preload()

    def load_assets(self):
        """Load all scene-specific assets"""
        try:
            self.background = pygame.image.load("assets/images/backgrounds/background_bridge.png")
            self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        except pygame.error as e:
            print(f"Error loading background: {e}")
            self.background = self.load_fallback_assets()  # Load fallback asset

    def handle_event(self, event):
        """Handle player interactions"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            # Add logic for handling mouse clicks on the bridge

    def update(self, dt):
        """Update scene state"""
        # Update messages
        self.messages = [msg for msg in self.messages if not msg.is_expired()]
        for msg in self.messages:
            msg.update(dt)

    def draw(self, screen):
        """Draw scene contents"""
        screen.blit(self.background, (0, 0))
        
        # Draw messages
        for msg in self.messages:
            msg.draw(screen)

        # Debug: Show clickable areas if needed
        if __debug__:
            # Example of drawing a debug rectangle
            pygame.draw.rect(screen, (255, 0, 0), (100, 100, 200, 50), 1)  # Example area
