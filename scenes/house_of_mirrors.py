import pygame
from engine.scene_base import Scene
from engine.ui import Message, ChoiceBox
from settings import SCREEN_WIDTH, SCREEN_HEIGHT

class HouseOfMirrorsScene(Scene):
    """Scene 3: Soul reflection - Players confront their reflections and make choices"""
    
    def __init__(self, game_state, scene_manager):
        super().__init__(game_state, scene_manager)
        self.mirrors = {
            "truth_mirror": {
                "active": False,
                "rect": pygame.Rect(200, 100, 200, 300),
                "message": "Your true self gazes back..."
            },
            "illusion_mirror": {
                "active": False,
                "rect": pygame.Rect(500, 100, 200, 300),
                "message": "Reflections of what could be..."
            },
            "soul_mirror": {
                "active": False,
                "rect": pygame.Rect(800, 100, 200, 300),
                "message": "The depths of your inner being..."
            }
        }
        self.preload()

    def load_assets(self):
        """Load all scene-specific assets"""
        try:
            self.background = pygame.image.load("assets/images/backgrounds/background_mirrors.png")
            self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))
            
            # Load mirror images
            for mirror_name in self.mirrors:
                image_path = f"assets/images/cutouts/mirror_{mirror_name}.png"
                try:
                    image = pygame.image.load(image_path)
                    self.mirrors[mirror_name]["image"] = image
                except pygame.error as e:
                    print(f"Could not load {image_path}: {e}")
                    self.mirrors[mirror_name]["image"] = self.load_fallback_assets()
                    
        except pygame.error as e:
            print(f"Error loading background: {e}")
            self.background = self.load_fallback_assets()

    def handle_event(self, event):
        """Handle player interactions with mirrors"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            for mirror_name, mirror in self.mirrors.items():
                if mirror["rect"].collidepoint(mouse_pos):
                    if not mirror["active"]:
                        mirror["active"] = True
                        self.messages.append(Message(mirror["message"]))
                        # Update soul state based on mirror interaction
                        if mirror_name == "truth_mirror":
                            self.game_state.choices["soul"]["memory_of_form"] = True

    def update(self, dt):
        """Update scene state"""
        # Update messages
        self.messages = [msg for msg in self.messages if not msg.is_expired()]
        for msg in self.messages:
            msg.update(dt)

    def draw(self, screen):
        """Draw scene contents"""
        # Draw background
        screen.blit(self.background, (0, 0))
        
        # Draw mirrors
        for mirror in self.mirrors.values():
            if "image" in mirror:
                screen.blit(mirror["image"], mirror["rect"])
            
            # Debug: Show clickable areas
            if __debug__:
                pygame.draw.rect(screen, (255, 0, 0), mirror["rect"], 1)
        
        # Draw messages
        for msg in self.messages:
            msg.draw(screen) 