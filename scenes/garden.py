import pygame
import os
from game_state import GameState
from engine.ui import Message

class GardenScene:
    def __init__(self, game_state, scene_manager):
        self.game_state = game_state
        self.scene_manager = scene_manager
        self.messages = []  # Initialize message list

        # Load background and scale to window size
        self.background = pygame.image.load("assets/images/backgrounds/background_garden.png")
        self.background = pygame.transform.scale(self.background, (1280, 720))

        # Load cutouts (no scaling)
        self.fruit_tree = pygame.image.load("assets/images/cutouts/fruit_tree.png")
        self.traveler = pygame.image.load("assets/images/cutouts/traveler_thirsty.png")
        self.altar = pygame.image.load("assets/images/cutouts/altar_prayer.png")
        self.fox = pygame.image.load("assets/images/cutouts/fox_shadow.png")
        self.mirror = pygame.image.load("assets/images/cutouts/broken_mirror.png")
        self.scroll = pygame.image.load("assets/images/cutouts/scroll_stone.png")

        # Adjust positions to match the reference image spacing
        self.fruit_tree_rect = self.fruit_tree.get_rect(center=(100, 360))     # Far left - fruit tree
        self.mirror_rect = self.mirror.get_rect(center=(450, 300))             # Crystal/mirror higher and left
        self.altar_rect = self.altar.get_rect(center=(640, 450))              # Center altar
        self.traveler_rect = self.traveler.get_rect(center=(900, 360))        # Traveler more right
        self.fox_rect = self.fox.get_rect(center=(1150, 360))                 # Fox far right
        self.scroll_rect = self.scroll.get_rect(center=(640, 600))           # Scroll lower

        # State flags
        self.has_fruit = False
        self.gave_fruit = False
        self.redeemed = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = pygame.mouse.get_pos()

            if self.fruit_tree_rect.collidepoint(pos):
                if self.game_state.get_choice("has_fruit"):
                    self.messages.append(Message("You already picked the fruit."))
                elif not self.game_state.get_choice("fruit_decided"):
                    self.messages.append(Message("You feel the weight of the fruit in your spirit. Do you take it?"))
                    self.messages.append(Message("[1] Take it  [2] Leave it", color=(200, 200, 255)))
                    choice = input("Choose 1 or 2: ")  # We'll replace this with buttons later

                    if choice == "1":
                        self.game_state.set_choice("has_fruit", True)
                        self.game_state.set_choice("fruit_decided", True)
                        self.game_state.add_score("soul.sin_score", 1)
                        self.game_state.set_choice("soul.last_action", "took_fruit")
                        self.messages.append(Message("You took the fruit. Something inside you feels uncertain."))

                    elif choice == "2":
                        self.game_state.set_choice("fruit_decided", True)
                        self.game_state.add_score("soul.light_score", 1)
                        self.game_state.set_choice("soul.last_action", "resisted_fruit")
                        self.messages.append(Message("You turned away. A soft wind stirs the leaves."))

            elif self.traveler_rect.collidepoint(pos):
                if self.has_fruit and not self.gave_fruit:
                    self.gave_fruit = True
                    self.has_fruit = False
                    self.game_state.set_choice("gave_fruit_to_traveler", True)
                    self.messages.append(Message("You gave the fruit to the traveler."))
                elif not self.has_fruit:
                    self.messages.append(Message("You have nothing to offer him."))
                else:
                    self.messages.append(Message("You already gave him fruit."))

            elif self.altar_rect.collidepoint(pos):
                if self.has_fruit and not self.gave_fruit:
                    self.game_state.set_choice("ate_fruit", True)
                    self.has_fruit = False
                    self.messages.append(Message("You consumed the fruit at the altar..."))
                elif not self.gave_fruit:
                    self.redeemed = True
                    self.game_state.set_choice("prayed_at_garden_altar", True)
                    self.messages.append(Message("You prayed for forgiveness."))

            elif self.fox_rect.collidepoint(pos):
                if not self.game_state.get_choice("fox_clicked"):
                    self.messages.append(Message("The fox whispers: 'Let me take the fruit for you. You need not touch it.'"))
                    self.game_state.set_choice("fox_clicked", True)

            elif self.mirror_rect.collidepoint(pos):
                if not self.game_state.get_choice("mirror_clicked"):
                    self.messages.append(Message("You glimpse a shadow that moves like you, but feels hollow."))
                    self.game_state.set_choice("mirror_clicked", True)

            elif self.scroll_rect.collidepoint(pos):
                if not self.game_state.get_choice("scroll_clicked"):
                    self.messages.append(Message("Engraved: 'He who walks in truth shall not stumble.'"))
                    self.game_state.set_choice("scroll_clicked", True)

    def update(self):
        pass

    def draw(self, screen):
        screen.blit(self.background, (0, 0))
        screen.blit(self.fruit_tree, self.fruit_tree_rect)
        screen.blit(self.traveler, self.traveler_rect)
        screen.blit(self.altar, self.altar_rect)
        screen.blit(self.fox, self.fox_rect)
        screen.blit(self.mirror, self.mirror_rect)
        screen.blit(self.scroll, self.scroll_rect)

        # Remove expired messages
        self.messages = [msg for msg in self.messages if not msg.is_expired()]

        # Draw messages (bottom center)
        for i, msg in enumerate(self.messages):
            msg.draw(screen, 40, 640 + i * 30)  # Adjust position as needed

# Make sure the class is available for import
__all__ = ['GardenScene']
