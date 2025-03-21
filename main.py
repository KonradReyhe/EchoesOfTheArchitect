import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS
from scene_manager import SceneManager
from scenes.start_screen import StartScreen

def main():
    pygame.init()
    
    # Set up windowed display
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Echoes of the Architect")
    
    clock = pygame.time.Clock()
    
    # Initialize with start screen
    scene_manager = SceneManager(StartScreen(None))
    scene_manager.current_scene.scene_manager = scene_manager  # Inject manager
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Keep escape key to exit
                    running = False
            scene_manager.handle_event(event)
            
        scene_manager.update()
        scene_manager.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)
    
    pygame.quit()

if __name__ == "__main__":
    main()
