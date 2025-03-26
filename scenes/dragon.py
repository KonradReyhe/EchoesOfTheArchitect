import pygame
from engine.scene_base import Scene  # Ensure this import is present
from settings import SCREEN_WIDTH, SCREEN_HEIGHT

class DragonScene(Scene):
    """Scene 6: Material attachment - Players confront their attachments to the material world."""
    
    def __init__(self, game_state, scene_manager):
        super().__init__(game_state, scene_manager)
        self.preload()
        self.dragon_states = ["sleeping", "awakened", "transcended"]
        
    def confront_dragon(self):
        """Face the dragon (ego/material attachment)"""
        if self.has_divine_items():
            self.messages.append(Message(
                "The dragon transforms into pure light..."
            ))
            self.game_state.add_score("divine_awareness", 3)
            self.sounds["bell"].play()

    def load_assets(self):
        """Load all scene-specific assets"""
        try:
            self.background = pygame.image.load("assets/images/backgrounds/background_dragon.png")
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