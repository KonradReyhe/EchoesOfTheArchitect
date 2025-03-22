import pygame
import os
from game_state import GameState
from engine.inventory import Inventory
from engine.ui import Message

class GardenScene:
    def __init__(self, game_state, scene_manager):
        self.game_state = game_state
        self.scene_manager = scene_manager
        self.messages = []
        self.inventory = Inventory()

        # Load and scale background
        self.background = pygame.image.load("assets/images/backgrounds/background_garden.png")
        self.background = pygame.transform.scale(self.background, (1280, 720))

        # Load core objects (always visible)
        self.fruit_tree = pygame.image.load("assets/images/cutouts/fruit_tree.png")
        self.fruit_tree = pygame.transform.scale(self.fruit_tree, (200, 250))
        self.fruit_tree_rect = self.fruit_tree.get_rect(topleft=(100, 320))

        # Load traveler with state check
        traveler_image = "traveler_radiant.png" if self.game_state.get_choice("traveler_state") == "radiant" else "traveler_thirsty.png"
        self.traveler = pygame.image.load(f"assets/images/cutouts/{traveler_image}")
        self.traveler = pygame.transform.scale(self.traveler, (150, 200))
        self.traveler_rect = self.traveler.get_rect(topleft=(950, 440))

        # Load altar
        self.altar = pygame.image.load("assets/images/cutouts/altar_prayer.png")
        self.altar = pygame.transform.scale(self.altar, (120, 150))
        self.altar_rect = self.altar.get_rect(topleft=(580, 380))

        # Load conditional objects based on soul state
        # Scroll appears after taking fruit
        if self.game_state.get_choice("fruit_taken"):
            self.scroll = pygame.image.load("assets/images/cutouts/scroll_stone.png")
            self.scroll = pygame.transform.scale(self.scroll, (80, 80))
            self.scroll_rect = self.scroll.get_rect(topleft=(80, 500))

        # Mirror appears after prayer or giving fruit
        if self.game_state.get_choice("prayed") or self.game_state.get_choice("fruit_given"):
            self.mirror = pygame.image.load("assets/images/cutouts/mirror_shard.png")
            self.mirror = pygame.transform.scale(self.mirror, (100, 100))
            self.mirror_rect = self.mirror.get_rect(topleft=(520, 580))

        # Fox appears after sinful action
        if self.game_state.get_choice("fruit_taken") and not self.game_state.get_choice("fruit_given"):
            self.fox = pygame.image.load("assets/images/cutouts/fox_shadow.png")
            self.fox = pygame.transform.scale(self.fox, (120, 100))
            self.fox_rect = self.fox.get_rect(topleft=(1080, 300))

        # Welcome message
        if not self.game_state.get_choice("garden_entered"):
            self.messages.append(Message("The Garden whispers with ancient echoes..."))
            self.game_state.set_choice("garden_entered", True)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = pygame.mouse.get_pos()
            selected = self.inventory.get_selected()

            # Handle inventory clicks
            clicked_item = self.inventory.handle_click(pos)
            if clicked_item:
                self.messages.append(Message(f"Selected: {clicked_item}"))
                return

            # FRUIT TREE - Free Will Test
            if self.fruit_tree_rect.collidepoint(pos):
                if not self.game_state.get_choice("fruit_taken"):
                    self.inventory.add_item("golden_fruit")
                    self.messages.append(Message("You have taken the Golden Fruit."))
                    self.game_state.set_choice("fruit_taken", True)
                    self.game_state.set_choice("fruit_given", False)
                    self.game_state.add_score("soul.sin_score", 1)
                else:
                    self.messages.append(Message("The tree is still. You already made your choice."))

            # TRAVELER - Compassion Test
            elif self.traveler_rect.collidepoint(pos):
                if self.game_state.get_choice("fruit_taken") and not self.game_state.get_choice("fruit_given") and selected == "golden_fruit":
                    self.inventory.remove_item("golden_fruit")
                    self.messages.append(Message("You gave the fruit to the traveler."))
                    self.game_state.set_choice("fruit_given", True)
                    self.game_state.add_score("soul.light_score", 1)
                    self.game_state.set_choice("traveler_state", "radiant")
                elif self.game_state.get_choice("fruit_given"):
                    self.messages.append(Message("The traveler smiles faintly."))
                else:
                    self.messages.append(Message("He looks at you with gentle hope."))

            # ALTAR - Divine Connection
            elif self.altar_rect.collidepoint(pos):
                if not self.game_state.get_choice("prayed"):
                    self.messages.append(Message("You kneel and whisper nothing. Still, something changes."))
                    self.game_state.set_choice("prayed", True)
                    self.game_state.add_score("soul.light_score", 1)
                else:
                    self.messages.append(Message("You have already prayed."))

            # FOX - Temptation
            elif hasattr(self, "fox_rect") and self.fox_rect.collidepoint(pos):
                if not self.game_state.get_choice("trusted_fox"):
                    self.messages.append(Message("The fox speaks gently. 'Take this key. You'll need it.'"))
                    self.game_state.set_choice("trusted_fox", True)
                    self.inventory.add_item("false_key")
                    self.game_state.add_score("soul.sin_score", 1)
                else:
                    self.messages.append(Message("The fox watches you in silence."))

            # SCROLL - Hidden Wisdom
            elif hasattr(self, "scroll_rect") and self.scroll_rect.collidepoint(pos):
                self.messages.append(Message("You feel the scroll whisper: 'All things hidden will return.'"))

            # MIRROR - Self Reflection
            elif hasattr(self, "mirror_rect") and self.mirror_rect.collidepoint(pos):
                self.messages.append(Message("You see a faint outline... it looks like you. But different."))

    def update(self):
        # Check for scene transition conditions (to be implemented)
        light_score = self.game_state.get_choice("soul.light_score", 0)
        sin_score = self.game_state.get_choice("soul.sin_score", 0)
        
        # TODO: Add scene transition logic
        pass

    def draw(self, screen):
        # Draw background
        screen.blit(self.background, (0, 0))
        
        # Draw objects in symbolic order
        screen.blit(self.fruit_tree, self.fruit_tree_rect)
        
        if hasattr(self, "scroll"):
            screen.blit(self.scroll, self.scroll_rect)
        
        if hasattr(self, "mirror"):
            screen.blit(self.mirror, self.mirror_rect)
        
        screen.blit(self.traveler, self.traveler_rect)
        
        if hasattr(self, "fox"):
            screen.blit(self.fox, self.fox_rect)
        
        screen.blit(self.altar, self.altar_rect)

        # Draw messages
        self.messages = [msg for msg in self.messages if not msg.is_expired()]
        for i, msg in enumerate(self.messages):
            msg.draw(screen, 40, 640 + i * 30)

        # Draw inventory
        self.inventory.draw(screen)

# Make sure the class is available for import
__all__ = ['GardenScene']
