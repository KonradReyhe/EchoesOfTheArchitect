import pygame
from engine.ui import Message, ChoiceBox
from settings import SCREEN_WIDTH, SCREEN_HEIGHT
from engine.scene_base import Scene

class SerpentRoom(Scene):
    def __init__(self, game_state, scene_manager):
        super().__init__(game_state, scene_manager)
        self.messages = []
        self.choice_box = None
        self.font = pygame.font.SysFont("georgia", 28)
        self.preload()
        
        # Show initial message
        self.messages.append(Message("The serpent coils in the shadows of your soul..."))
        
        # Create choice box
        self.choice_box = ChoiceBox(
            font=self.font,
            options=[
                ("Name it", "name"),
                ("Rebuke it", "rebuke"),
                ("Remain silent", "silence")
            ],
            callback=self.handle_serpent_choice
        )

    def load_assets(self):
        """Load all scene-specific assets"""
        self.background = pygame.image.load("assets/images/backgrounds/serpent_room.png")
        self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        
        serpent_type = self.game_state.get_choice("inner_serpent", "pride")
        self.serpent = pygame.image.load(f"assets/images/cutouts/serpent_shadow_{serpent_type}.png")
        self.serpent_rect = self.serpent.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))

    def update(self, dt):
        """Update scene state"""
        self.messages = [msg for msg in self.messages if not msg.is_expired()]
        self.update_transition(dt)

    def handle_serpent_choice(self, choice):
        if choice == "name" and self.game_state.get_choice("soul.memory_of_form"):
            self.messages.append(Message("The serpent dissolves as you speak its true name..."))
            self.game_state.set_choice("serpent_named", True)
            self.scene_manager.switch_to("ending_room")
        elif choice == "rebuke":
            self.messages.append(Message("Your words echo back, revealing your own pride..."))
            self.game_state.set_choice("ending_type", "pride")
            self.scene_manager.switch_to("ending_room")
        else:  # silence
            self.messages.append(Message("The silence grows deeper..."))
            self.game_state.set_choice("ending_type", "emptiness")
            self.scene_manager.switch_to("ending_room")

    def draw(self, screen):
        """Draw scene contents"""
        screen.blit(self.background, (0, 0))
        screen.blit(self.serpent, self.serpent_rect)
        
        # Draw messages
        for i, msg in enumerate(self.messages):
            msg.draw(screen, 40, SCREEN_HEIGHT - 100 + i * 30)
        
        # Draw choice box
        if self.choice_box:
            self.choice_box.draw(screen, SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT - 200) 