import pygame
import os
from settings import SCREEN_WIDTH, SCREEN_HEIGHT

class Inventory:
    def __init__(self):
        self.items = []
        self.slot_size = 64
        self.padding = 8
        self.slots = 5
        self.selected_item = None
        self.images = {}
        
        # Position inventory at top right
        self.x = SCREEN_WIDTH - (self.slot_size + self.padding) * self.slots - 20
        self.y = 20

    def add_item(self, item_name):
        if len(self.items) >= self.slots:
            return False
            
        if item_name not in self.items:
            try:
                image_path = f"assets/images/inventory/{item_name}.png"
                if not os.path.exists(image_path):
                    return False
                    
                if item_name not in self.images:
                    image = pygame.image.load(image_path).convert_alpha()
                    image = pygame.transform.scale(image, (self.slot_size, self.slot_size))
                    self.images[item_name] = image
                
                self.items.append(item_name)
                return True
            except Exception:
                return False
        return False

    def has_item(self, item_id):
        """Check if inventory contains specific item"""
        return item_id in self.items

    def remove_item(self, item_name):
        """Remove an item from inventory by name"""
        if item_name in self.items:
            self.items.remove(item_name)
            if self.selected_item == item_name:
                self.selected_item = None
            return True
        return False

    def get_selected(self):
        return self.selected_item

    def handle_click(self, pos):
        # Check if click is in inventory area
        for i, item in enumerate(self.items):
            slot_x = self.x + (self.slot_size + self.padding) * i
            slot_rect = pygame.Rect(slot_x, self.y, self.slot_size, self.slot_size)
            if slot_rect.collidepoint(pos):
                self.selected_item = item
                return item
        return None

    def draw(self, screen):
        # Draw inventory background
        bg_width = (self.slot_size + self.padding) * self.slots + self.padding
        bg_height = self.slot_size + self.padding * 2
        inventory_bg = pygame.Surface((bg_width, bg_height))
        inventory_bg.fill((20, 20, 20))
        inventory_bg.set_alpha(200)
        screen.blit(inventory_bg, (self.x - self.padding, self.y - self.padding))
        
        # Draw slots with glow effect for filled slots
        for i in range(self.slots):
            slot_x = self.x + (self.slot_size + self.padding) * i
            slot_rect = pygame.Rect(slot_x, self.y, self.slot_size, self.slot_size)
            
            # Draw glow effect if slot has item
            if i < len(self.items):
                glow_surface = pygame.Surface((self.slot_size + 4, self.slot_size + 4), pygame.SRCALPHA)
                pygame.draw.rect(glow_surface, (255, 223, 100, 40), glow_surface.get_rect())
                screen.blit(glow_surface, (slot_x - 2, self.y - 2))
            
            # Draw slot background
            pygame.draw.rect(screen, (40, 40, 40), slot_rect)
            pygame.draw.rect(screen, (60, 60, 60), slot_rect, 2)
        
        # Draw items
        for i, item_name in enumerate(self.items):
            if item_name in self.images:
                slot_x = self.x + (self.slot_size + self.padding) * i
                screen.blit(self.images[item_name], (slot_x, self.y))

    def can_forge_true_key(self):
        """Check if player has components for true key"""
        required_items = {
            "soul_shard": False,
            "dove_feather": False
        }
        
        for item in self.items:
            if item in required_items:
                required_items[item] = True
                
        return (all(required_items.values()) and 
                self.game_state.get_choice("soul.memory_of_form"))

    def forge_true_key(self):
        """Attempt to create the true key"""
        if self.can_forge_true_key():
            self.remove_item("soul_shard")
            self.remove_item("dove_feather")
            self.add_item("true_key")
            return True
        return False

    def create_placeholder_image(self):
        """Create a placeholder for missing inventory items"""
        surface = pygame.Surface((self.slot_size, self.slot_size))
        surface.fill((100, 100, 100))
        pygame.draw.rect(surface, (200, 200, 200), surface.get_rect(), 2)
        return surface

    def toggle_debug_visuals(self, enabled=False):
        """Toggle debug visualization"""
        self.show_debug = enabled
        if enabled:
            print("DEBUG: Inventory debug visuals enabled")
