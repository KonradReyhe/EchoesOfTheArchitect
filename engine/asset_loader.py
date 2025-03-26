import pygame

class AssetLoader:
    """Centralized asset management"""
    def __init__(self):
        self.cache = {}
        self.base_path = "assets/images"
    
    def load_cutout(self, name, size=None):
        key = f"cutout_{name}"
        if key not in self.cache:
            path = f"{self.base_path}/cutouts/{name}.png"
            image = pygame.image.load(path)
            if size:
                image = pygame.transform.scale(image, size)
            self.cache[key] = image
        return self.cache[key]

    def load_image(self, path, size=None):
        try:
            image = pygame.image.load(path)
            if size:
                image = pygame.transform.scale(image, size)
            return image
        except pygame.error:
            print(f"Warning: Could not load image: {path}")
            # Return a default/placeholder image
            return self.create_placeholder(size) 