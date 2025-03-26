from engine.inventory import Inventory

class SceneManager:
    def __init__(self, game_state):
        self.game_state = game_state
        self.inventory = Inventory()
        self.current_scene = None
        self.next_scene = None
        self.scenes = {}
        
    def register_scene(self, name, scene_class):
        """Register a scene class for later instantiation"""
        self.scenes[name] = scene_class
    
    def switch_to(self, scene_name):
        """Switch to a registered scene"""
        if scene_name not in self.scenes:
            print(f"Warning: Scene {scene_name} not registered")
            return
            
        self.current_scene = self.scenes[scene_name](self.game_state, self)
    
    def update(self, dt):
        """Update current scene and handle transitions"""
        if self.current_scene:
            self.current_scene.update(dt)
            
            # Check for scene transition completion
            if (self.current_scene.is_transitioning and 
                self.current_scene.transition_alpha == 0):
                self.current_scene = self.next_scene
                self.next_scene = None
                self.current_scene.is_transitioning = True
    
    def draw(self, screen):
        """Draw current scene"""
        if self.current_scene:
            self.current_scene.draw(screen)

    def handle_event(self, event):
        """Handle events for current scene"""
        if self.current_scene:
            self.current_scene.handle_event(event) 