import pygame
from engine.scene_base import Scene
from engine.ui import Message
from settings import SCREEN_WIDTH, SCREEN_HEIGHT

class TempleScene(Scene):
    def __init__(self, game_state, scene_manager):
        super().__init__(game_state, scene_manager)
        self.sacred_elements = {
            "bell_tower": {
                "active": False,
                "rect": pygame.Rect(600, 200, 100, 300),
                "message": "The bell's resonance reveals hidden truths..."
            },
            "all_seeing_eye": {
                "active": False,
                "rect": pygame.Rect(400, 100, 150, 150),
                "message": "The Architect's gaze penetrates illusion..."
            },
            "pillars": {
                "active": False,
                "rect": pygame.Rect(200, 300, 400, 200),
                "message": "Twin pillars: mercy and severity, wisdom and strength..."
            }
        }
        
        self.sounds = {
            "bell": pygame.mixer.Sound("assets/sounds/bell.wav"),
            "revelation": pygame.mixer.Sound("assets/sounds/revelation.wav")
        }
        self.preload()

    def load_assets(self):
        """Load all scene-specific assets"""
        self.background = pygame.image.load("assets/images/backgrounds/temple.png")
        self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        
        # Load sacred element images
        for element_name in self.sacred_elements:
            image_path = f"assets/images/cutouts/{element_name}.png"
            try:
                image = pygame.image.load(image_path)
                self.sacred_elements[element_name]["image"] = image
            except pygame.error:
                print(f"Could not load {image_path}")

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = pygame.mouse.get_pos()
            
            # Handle sacred element interactions
            for element_name, element in self.sacred_elements.items():
                if element["rect"].collidepoint(pos) and not element["active"]:
                    self.activate_element(element_name)
                    self.messages.append(Message(element["message"]))

    def activate_element(self, element_name):
        element = self.sacred_elements[element_name]
        element["active"] = True
        
        if element_name == "bell_tower":
            self.sounds["bell"].play()
            self.cleanse_area()
        
        if element_name == "all_seeing_eye":
            self.reveal_divine_patterns()
            
        if element_name == "pillars":
            self.balance_forces()
            
        # Check if all elements are activated
        if all(e["active"] for e in self.sacred_elements.values()):
            self.complete_temple_awakening()

    def cleanse_area(self):
        """Bell tower function - dispels darkness"""
        self.game_state.add_score("light_score", 1)
        self.create_light_effect()
        self.messages.append(Message(
            "The bell's pure tone drives away shadows..."
        ))

    def reveal_divine_patterns(self):
        """All-seeing eye function - reveals sacred geometry"""
        if self.game_state.get_choice("soul.memory_of_form"):
            self.show_sacred_geometry()
            self.messages.append(Message(
                "Golden ratios and divine proportions become visible..."
            ))
            self.sounds["revelation"].play()

    def balance_forces(self):
        """Pillar function - helps transform the serpent"""
        serpent = self.game_state.get_choice("inner_serpent")
        if serpent in ["pride", "envy", "apathy"]:
            self.begin_serpent_transformation()

    def show_sacred_geometry(self):
        """Reveal divine patterns in temple architecture"""
        patterns_found = self.game_state.choices["world_state"]["patterns_revealed"]
        if "temple_geometry" not in patterns_found:
            patterns_found.append("temple_geometry")
            self.game_state.add_score("divine_awareness", 2)

    def begin_serpent_transformation(self):
        """Start the process of serpent transformation"""
        self.game_state.set_choice("serpent_transformation_begun", True)
        self.messages.append(Message(
            "The pillars resonate with your inner nature..."
        ))
        self.scene_manager.switch_to("serpent")

    def complete_temple_awakening(self):
        """Handle completion of all temple elements"""
        self.messages.append(Message(
            "The temple resonates with divine harmony..."
        ))
        self.sounds["bell"].play()
        self.game_state.add_score("light_score", 3)
        self.game_state.set_choice("temple_awakened", True)

    def draw(self, screen):
        """Draw scene contents"""
        # Draw background
        screen.blit(self.background, (0, 0))
        
        # Draw sacred elements
        for element_name, element in self.sacred_elements.items():
            if "image" in element:
                screen.blit(element["image"], element["rect"])
            
            # Draw glow effect for active elements
            if element["active"]:
                glow_surface = pygame.Surface((element["rect"].width + 20, element["rect"].height + 20), pygame.SRCALPHA)
                pygame.draw.rect(glow_surface, (255, 223, 100, 40), glow_surface.get_rect())
                screen.blit(glow_surface, (element["rect"].x - 10, element["rect"].y - 10))
        
        # Draw messages
        for msg in self.messages:
            msg.draw(screen)

    def update(self, dt):
        """Update scene state"""
        self.messages = [msg for msg in self.messages if not msg.is_expired()]
        self.update_transition(dt)
