import pygame
import os
from game_state import GameState
from engine.inventory import Inventory
from engine.ui import Message, ChoiceBox
from engine.serpent_within import SerpentWithin
import random
from engine.scene_base import Scene
from settings import SCREEN_WIDTH, SCREEN_HEIGHT  # Add this at the top
from abc import ABC

class GardenScene(Scene):
    def __init__(self, game_state, scene_manager):
        super().__init__(game_state, scene_manager)
        self.messages = []
        self.choice_box = None
        self.font = pygame.font.SysFont("georgia", 28)
        self.serpent = SerpentWithin(game_state)
        self.divine_patterns_found = 0
        self.chaos_elements = ["withered_tree", "muddy_water", "dark_sky"]
        self.restored_elements = []
        
        # Load sound effects with error handling
        self.sounds = {}
        sound_files = {
            "fruit_take": "assets/sounds/fruit_take.wav",
            "prayer": "assets/sounds/prayer.wav",
            "choice": "assets/sounds/choice.wav"
        }
        
        # Create sounds directory if it doesn't exist
        os.makedirs("assets/sounds", exist_ok=True)
        
        # Try to load each sound, skip if file missing
        for sound_name, sound_path in sound_files.items():
            try:
                self.sounds[sound_name] = pygame.mixer.Sound(sound_path)
            except FileNotFoundError:
                print(f"Warning: Sound file not found: {sound_path}")
                continue
        
        self.preload()  # This will call load_assets()

    def preload(self):
        self.load_assets()

    def load_assets(self):
        """Load all scene-specific assets"""
        # Load and scale background
        self.background = pygame.image.load("assets/images/backgrounds/background_garden.png")
        self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))

        # Load tree with adjusted position and clickable area
        self.fruit_tree = pygame.image.load("assets/images/cutouts/fruit_tree.png")
        self.fruit_tree = pygame.transform.scale(self.fruit_tree, (250, 450))
        self.fruit_tree_rect = self.fruit_tree.get_rect(topleft=(150, 270))
        
        # Make clickable area larger and positioned on the fruit part of the tree
        self.fruit_tree_clickable = pygame.Rect(
            self.fruit_tree_rect.left + 75,  # Adjust these values based on where
            self.fruit_tree_rect.top + 150,   # the fruit appears in your tree image
            150,  # Make clickable area wider
            150   # and taller
        )

        # Load altar - position more to the right
        self.altar = pygame.image.load("assets/images/cutouts/altar_prayer.png")
        self.altar = pygame.transform.scale(self.altar, (100, 120))  # Slightly smaller
        self.altar_rect = self.altar.get_rect(topleft=(600, 600))  # More to the right

        # Load traveler based on state
        traveler_image = "traveler_radiant.png" if self.game_state.get_choice("traveler_state") == "radiant" else "traveler_thirsty.png"
        self.traveler = pygame.image.load(f"assets/images/cutouts/{traveler_image}")
        self.traveler = pygame.transform.scale(self.traveler, (150, 200))
        self.traveler_rect = self.traveler.get_rect(topleft=(950, 520))  # Place at ground level

        # Load conditional objects based on soul state
        if self.game_state.get_choice("fruit_taken"):
            self.scroll = pygame.image.load("assets/images/cutouts/scroll_stone.png")
            self.scroll = pygame.transform.scale(self.scroll, (80, 80))
            self.scroll_rect = self.scroll.get_rect(topleft=(80, 500))

        if self.game_state.get_choice("prayed") or self.game_state.get_choice("fruit_given"):
            self.mirror = pygame.image.load("assets/images/cutouts/mirror_shard.png")
            self.mirror = pygame.transform.scale(self.mirror, (100, 100))
            self.mirror_rect = self.mirror.get_rect(topleft=(520, 580))

        if self.game_state.get_choice("fruit_taken") and not self.game_state.get_choice("fruit_given"):
            self.fox = pygame.image.load("assets/images/cutouts/fox_shadow.png")
            self.fox = pygame.transform.scale(self.fox, (120, 150))
            self.fox_rect = self.fox.get_rect(topleft=(700, 520))

        # Welcome message
        if not self.game_state.get_choice("garden_entered"):
            self.messages.append(Message("The Garden whispers with ancient echoes..."))
            self.game_state.set_choice("garden_entered", True)

    def handle_event(self, event):
        """Handle scene-specific events"""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left click
            pos = pygame.mouse.get_pos()
            
            # Handle choice box first if it exists
            if self.choice_box:
                if self.choice_box.handle_click(pos):
                    self.sounds["choice"].play()
                return
            
            # Handle tree interaction
            if hasattr(self, 'fruit_tree_clickable') and self.fruit_tree_clickable.collidepoint(pos):
                self.take_fruit()
                return

            # Handle traveler interaction
            elif self.traveler_rect.collidepoint(pos):
                self.choice_box = ChoiceBox(
                    font=self.font,
                    options=[
                        ("Give fruit", "give"),
                        ("Say nothing", "ignore"),
                        ("Ask who he is", "ask")
                    ],
                    callback=self.handle_traveler_choice
                )

            # Handle altar interaction
            elif self.altar_rect.collidepoint(pos):
                self.interact_with_altar()
                return

            # Handle scroll interaction
            elif hasattr(self, "scroll_rect") and self.scroll_rect.collidepoint(pos):
                self.examine_scroll()
                return

            # Handle fox interaction
            elif hasattr(self, "fox_rect") and self.fox_rect.collidepoint(pos):
                self.interact_with_fox()
                return

            # Handle mirror interaction
            elif hasattr(self, "mirror_rect") and self.mirror_rect.collidepoint(pos):
                self.look_into_mirror()
                return

    def handle_traveler_choice(self, choice):
        """Handle choices related to the traveler."""
        if choice == "give":
            if self.inventory.has_item("golden_fruit"):
                self.inventory.remove_item("golden_fruit")
                self.game_state.set_choice("fruit_given", True)
                self.game_state.add_score("light_score", 2)
                self.messages.append(Message("The traveler's thirst is quenched. His form seems to shimmer..."))
                self.game_state.set_choice("traveler_state", "radiant")
                self.load_traveler_image("traveler_radiant.png")
            else:
                self.messages.append(Message("You have nothing to give..."))
        elif choice == "ignore":
            self.messages.append(Message("You turn away from his suffering..."))
            self.game_state.add_score("sin_score", 1)
        elif choice == "ask":
            if self.game_state.get_choice("traveler_state") == "thirsty":
                self.messages.append(Message("I am a wanderer, seeking the light of truth. Will you help me?"))
            else:
                self.messages.append(Message("I am a guide, transformed by your kindness. The path ahead is clearer now."))
        
        self.choice_box = None  # Clear choice box after selection

    def handle_serpent_recognition(self, choice_id):
        if choice_id == "name_serpent":
            self.game_state.set_choice("recognized_serpent", True)
            self.messages.append(Message("You see it clearly now - your own shadow given form..."))

    def update(self, dt):
        """Update scene state"""
        # Update messages
        self.messages = [msg for msg in self.messages if not msg.is_expired()]
        
        # Add serpent whisper if needed
        if self.serpent.should_appear_in_scene("garden"):
            self.messages.append(Message(
                self.serpent.get_whisper(),  # Just pass positional arguments
                5.0,
                (150, 100, 100)  # Reddish color for serpent messages
            ))
        
        self.update_transition(dt)

    def draw(self, screen):
        """Draw scene contents"""
        # Draw background first
        screen.blit(self.background, (0, 0))
        
        # Draw scene objects in correct order (back to front)
        screen.blit(self.fruit_tree, self.fruit_tree_rect)
        if hasattr(self, 'altar'):
            screen.blit(self.altar, self.altar_rect)
        if hasattr(self, 'traveler'):
            screen.blit(self.traveler, self.traveler_rect)
        
        # Draw messages at top of screen with proper styling
        if self.messages:
            # Create semi-transparent background for messages
            msg_background = pygame.Surface((800, 100))
            msg_background.fill((0, 0, 0))
            msg_background.set_alpha(160)
            screen.blit(msg_background, (40, 20))
            
            # Draw most recent message
            msg = self.messages[-1]
            msg.draw(screen, 60, 40)
        
        # Draw choice box below message if active
        if self.choice_box:
            choice_background = pygame.Surface((300, 120))
            choice_background.fill((0, 0, 0))
            choice_background.set_alpha(128)
            screen.blit(choice_background, (40, 130))
            self.choice_box.draw(screen, 50, 140)
        
        # Draw inventory at top-right
        self.inventory.draw(screen)

        # Draw serpent manifestation if present
        if self.serpent.should_appear_in_scene("garden"):
            manifestation = self.serpent.get_current_manifestation("garden")
            if manifestation:
                self.draw_serpent_manifestation(screen, manifestation)

    def draw_serpent_manifestation(self, screen, manifestation):
        """Draw the serpent's current manifestation with its specific visual effect"""
        # Load and draw the appropriate serpent image based on manifestation.form
        # Apply the visual effect specified in manifestation.visual_effect
        # Position according to manifestation.scene_specific["garden"]
        pass  # Implement actual drawing logic based on your asset system

    def reveal_divine_pattern(self):
        """Each scene can have hidden patterns that reveal divine design"""
        patterns = {
            "garden": {
                "golden_ratio": "Tree and altar placement follows divine proportion",
                "sacred_geometry": "Path layout reveals sacred pattern",
                "symbolic_meaning": "Tree of knowledge represents choice"
            },
            "mirrors": {
                "reflection_truth": "Mirrors show true nature of reality",
                "hidden_order": "Seemingly random cracks form meaningful pattern"
            }
        }

    def restore_element(self, element):
        """Transform chaos into order when player discovers truth"""
        if element in self.chaos_elements:
            self.chaos_elements.remove(element)
            self.restored_elements.append(element)
            self.game_state.add_score("divine_awareness", 1)
            self.messages.append(Message(
                "As you recognize the divine pattern, order returns..."
            ))

    def take_fruit(self):
        """Handle taking the golden fruit from the tree."""
        if not self.inventory.has_item("golden_fruit"):
            success = self.inventory.add_item("golden_fruit")
            if success:
                self.sounds["fruit_take"].play()
                self.messages.append(Message("You have taken the Golden Fruit."))
                self.game_state.set_choice("fruit_taken", True)
            else:
                self.messages.append(Message("Your inventory is full."))
        else:
            self.messages.append(Message("The tree stands silent. You already have its fruit."))

    def interact_with_altar(self):
        """Handle interaction with the altar."""
        if not self.game_state.get_choice("prayed"):
            self.messages.append(Message("You kneel in silence... something inside you becomes still."))
            self.game_state.set_choice("prayed", True)
            self.game_state.add_score("light_score", 1)
        else:
            self.messages.append(Message("The altar remains silent."))

    def examine_scroll(self):
        """Handle examining the scroll."""
        if not self.game_state.get_choice("fruit_taken"):
            self.messages.append(Message("You notice faint writing: 'He who offers paths before the trial is not your guide.'"))
            self.game_state.set_choice("scroll_warning_seen", True)
        else:
            self.messages.append(Message("The scroll seems blank..."))

    def interact_with_fox(self):
        """Handle interaction with the fox."""
        if not self.game_state.get_choice("trusted_fox"):
            if not self.game_state.get_choice("scroll_warning_seen"):
                self.inventory.add_item("false_key")
                self.messages.append(Message("The fox smirks: 'This will open the way.'"))
                self.game_state.set_choice("trusted_fox", True)
                self.game_state.add_score("sin_score", 1)
            else:
                self.messages.append(Message("You hesitate. You remember the scroll's warning..."))
        else:
            self.messages.append(Message("The fox watches you in silence."))

    def look_into_mirror(self):
        """Handle looking into the mirror."""
        self.messages.append(Message("You see a faint outline... it looks like you. But different."))

# Make sure the class is available for import
__all__ = ['GardenScene']
