import pygame
from abc import ABC, abstractmethod
import os
from settings import SCREEN_WIDTH, SCREEN_HEIGHT

class Scene(ABC):
    """Abstract base class for all scenes"""
    def __init__(self, game_state, scene_manager):
        self.game_state = game_state
        self.scene_manager = scene_manager
        self.messages = []
        self.inventory = scene_manager.inventory
        self.assets = {}
        self.transition_alpha = 255
        self.is_transitioning = False
        
    @abstractmethod
    def load_assets(self):
        """Load all scene-specific assets"""
        pass
        
    def preload(self):
        """Safely preload and scale assets"""
        try:
            self.load_assets()
        except pygame.error as e:
            print(f"Asset loading error: {e}")
            # Create data/assets directories if they don't exist
            os.makedirs("data", exist_ok=True)
            os.makedirs("assets/images/backgrounds", exist_ok=True)
            os.makedirs("assets/images/cutouts", exist_ok=True)
            os.makedirs("assets/images/inventory", exist_ok=True)
            # Load fallback assets
            self.background = self.load_fallback_assets()
    
    def handle_event(self, event):
        """Handle scene-specific events"""
        pass

    def update(self, dt):
        """Update scene state"""
        pass

    @abstractmethod
    def draw(self, screen):
        """Draw scene contents"""
        pass

    def update_transition(self, dt):
        """Handle scene transition effects"""
        if self.is_transitioning:
            self.transition_alpha = max(0, self.transition_alpha - dt * 255)
            if self.transition_alpha == 0:
                self.is_transitioning = False 

    def load_fallback_assets(self):
        """Create fallback assets when loading fails"""
        surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        surface.fill((50, 50, 50))  # Dark gray background
        font = pygame.font.SysFont("arial", 32)
        text = font.render("Asset loading failed", True, (255, 0, 0))
        text_rect = text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
        surface.blit(text, text_rect)
        return surface 

    def play_bell_sound(self):
        """Play bell sound with spiritual cleansing effect"""
        if hasattr(self, 'sounds') and 'bell' in self.sounds:
            self.sounds["bell"].play()
            self.create_light_effect()
            self.game_state.choices["world_state"]["chaos_level"] -= 1 