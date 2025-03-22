import pygame
import os

class Inventory:
    def __init__(self):
        self.items = []
        self.slot_size = 64
        self.padding = 10
        self.slots = 5  # Number of visible slots
        self.selected = None  # Add this line
        
        # Position inventory at bottom right
        self.x = 1280 - (self.slot_size + self.padding) * self.slots - self.padding
        self.y = 720 - self.slot_size - self.padding
        print("Inventory initialized")  # Debug message

    def add_item(self, item_id):
        if len(self.items) < self.slots:
            try:
                # Use os.path.join for proper path handling
                image_path = os.path.join("assets", "images", "inventory", f"{item_id}.png")
                print(f"Attempting to load: {os.path.abspath(image_path)}")  # Debug full path
                
                if not os.path.exists(image_path):
                    print(f"File does not exist: {image_path}")
                    return False
                
                image = pygame.image.load(image_path)
                image = pygame.transform.scale(image, (self.slot_size, self.slot_size))
                self.items.append({"id": item_id, "image": image})
                print(f"Successfully added {item_id} to inventory. Total items: {len(self.items)}")
                return True
            except Exception as e:
                print(f"Error loading inventory image: {str(e)}")
                return False
        else:
            print("Inventory is full")
            return False

    def has_item(self, item_id):
        has = any(item["id"] == item_id for item in self.items)
        print(f"Checking for {item_id}: {has}")  # Debug message
        return has

    def remove_item(self, item_id):
        original_length = len(self.items)
        self.items = [item for item in self.items if item["id"] != item_id]
        print(f"Removed {item_id}. Items before: {original_length}, after: {len(self.items)}")

    def get_selected(self):
        return self.selected

    def handle_click(self, pos):
        # Check if click is in inventory area
        for i, item in enumerate(self.items):
            slot_x = self.x + (self.slot_size + self.padding) * i
            slot_rect = pygame.Rect(slot_x, self.y, self.slot_size, self.slot_size)
            if slot_rect.collidepoint(pos):
                self.selected = item["id"]  # Update selected item
                return item["id"]
        return None

    def draw(self, screen):
        # Draw empty slots
        for i in range(self.slots):
            slot_x = self.x + (self.slot_size + self.padding) * i
            slot_rect = pygame.Rect(slot_x, self.y, self.slot_size, self.slot_size)
            pygame.draw.rect(screen, (50, 50, 50), slot_rect)
            pygame.draw.rect(screen, (100, 100, 100), slot_rect, 2)

        # Draw items
        for i, item in enumerate(self.items):
            slot_x = self.x + (self.slot_size + self.padding) * i
            screen.blit(item["image"], (slot_x, self.y))
        
        if len(self.items) > 0:
            print(f"Drawing {len(self.items)} items in inventory")  # Debug message
