import pygame
from engine.scene_base import Scene  # Ensure this import is present
from settings import SCREEN_WIDTH, SCREEN_HEIGHT

class CaduceusScene(Scene):
    """Scene 5: Balance of forces - Players align the twin serpents to restore balance."""
    
    def __init__(self, game_state, scene_manager):
        super().__init__(game_state, scene_manager)
        self.staff_assembled = False
        self.snakes_balanced = False
        
    def balance_serpents(self):
        """Align the twin serpents (wisdom/ignorance)"""
        if self.game_state.get_choice("soul.memory_of_form"):
            self.snakes_balanced = True
            self.messages.append(Message(
                "The serpents align, revealing the path of wisdom..."
            ))
            self.sounds["bell"].play() 

    def load_assets(self):
        """Load all scene-specific assets"""
        try:
            self.background = pygame.image.load("assets/images/backgrounds/background_caduceus.png")
            self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        except pygame.error as e:
            print(f"Error loading background: {e}")
            self.background = self.load_fallback_assets()  # Load fallback asset

    def handle_event(self, event):
        """Handle player interactions"""
        pass

    def update(self, dt):
        """Update scene state"""
        pass

    def draw(self, screen):
        """Draw scene contents"""
        screen.blit(self.background, (0, 0)) 