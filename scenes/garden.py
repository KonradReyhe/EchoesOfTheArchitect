import pygame
import os
from game_state import GameState

class GardenScene:
    def __init__(self, game_state, scene_manager):
        self.game_state = game_state
        self.scene_manager = scene_manager

        # Load background
        self.background = pygame.image.load("assets/images/backgrounds/background_garden.png")
        # Scale background to fit screen
        self.background = pygame.transform.scale(self.background, (1280, 720))

        # Load cutouts
        self.fruit_tree = pygame.image.load("assets/images/cutouts/fruit_tree.png")
        self.traveler = pygame.image.load("assets/images/cutouts/traveler_thirsty.png")
        self.altar = pygame.image.load("assets/images/cutouts/altar_prayer.png")
        
        # Load new cutouts
        self.fox = pygame.image.load("assets/images/cutouts/fox_shadow.png")
        self.mirror = pygame.image.load("assets/images/cutouts/broken_mirror.png")
        self.scroll = pygame.image.load("assets/images/cutouts/scroll_stone.png")

        # Adjust positions to match the visual layout in the scene
        self.fruit_tree_rect = self.fruit_tree.get_rect(center=(150, 360))    # Far left - fruit tree
        self.mirror_rect = self.mirror.get_rect(center=(400, 360))            # Left - broken mirror/crystal
        self.altar_rect = self.altar.get_rect(center=(640, 500))             # Center bottom - altar
        self.traveler_rect = self.traveler.get_rect(center=(750, 360))       # Right of center - traveler
        self.fox_rect = self.fox.get_rect(center=(1000, 360))               # Far right - fox
        self.scroll_rect = self.scroll.get_rect(center=(640, 580))          # Below altar - scroll

        # State flags
        self.has_fruit = False
        self.gave_fruit = False
        self.redeemed = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Limit the number of significant actions (any choice)
            max_choices = 2
            current_choices = sum([
                self.game_state.get_choice("gave_fruit_to_traveler"),
                self.game_state.get_choice("fox_clicked"),
                self.game_state.get_choice("mirror_clicked"),
                self.game_state.get_choice("scroll_clicked")
            ])

            if current_choices >= max_choices:
                print("You feel that you should no longer act... only reflect.")
                return

            pos = pygame.mouse.get_pos()

            if self.fruit_tree_rect.collidepoint(pos):
                self.has_fruit = True
                self.game_state.set_choice("has_fruit", True)
                print("You picked the fruit.")

            elif self.traveler_rect.collidepoint(pos):
                if self.has_fruit and not self.gave_fruit:
                    self.gave_fruit = True
                    self.has_fruit = False
                    self.game_state.set_choice("gave_fruit_to_traveler", True)
                    print("You gave the fruit to the traveler.")
                elif not self.has_fruit:
                    print("You have nothing to offer him.")
                else:
                    print("You already gave him fruit.")

            elif self.altar_rect.collidepoint(pos):
                if not self.gave_fruit:
                    self.redeemed = True
                    self.game_state.set_choice("prayed_at_garden_altar", True)
                    print("You prayed for forgiveness.")

            elif self.fox_rect.collidepoint(pos):
                if not self.game_state.get_choice("fox_clicked"):
                    print("The fox whispers: 'Let me take the fruit for you. You need not touch it.'")
                    self.game_state.set_choice("fox_clicked", True)

            elif self.mirror_rect.collidepoint(pos):
                if not self.game_state.get_choice("mirror_clicked"):
                    print("You glimpse a shadow that moves like you, but feels hollow. Is that who you've become?")
                    self.game_state.set_choice("mirror_clicked", True)

            elif self.scroll_rect.collidepoint(pos):
                if not self.game_state.get_choice("scroll_clicked"):
                    print("Engraved: 'He who walks in truth shall not stumble.'")
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

# Make sure the class is available for import
__all__ = ['GardenScene']
