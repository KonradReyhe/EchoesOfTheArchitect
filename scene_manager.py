class SceneManager:
    def __init__(self, starting_scene):
        self.current_scene = starting_scene

    def switch_to(self, new_scene):
        self.current_scene = new_scene

    def handle_event(self, event):
        if self.current_scene:
            self.current_scene.handle_event(event)

    def update(self):
        if self.current_scene:
            self.current_scene.update()

    def draw(self, screen):
        if self.current_scene:
            self.current_scene.draw(screen)

# Export the class directly instead of using __all__
SceneManager = SceneManager
