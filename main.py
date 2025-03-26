import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS
from engine.scene_manager import SceneManager
from engine.scene_base import Scene
from scenes.start_screen import StartScreen
from scenes.garden import GardenScene
from scenes.house_of_mirrors import HouseOfMirrorsScene
from scenes.serpent_room import SerpentRoom
from scenes.temple import TempleScene
from game_state import GameState
from scenes.bridge import BridgeScene
from scenes.dragon import DragonScene
from scenes.caduceus import CaduceusScene

def main():
    pygame.init()
    
    # Set up windowed display
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Echoes of the Architect")
    
    clock = pygame.time.Clock()
    
    # Initialize game state and scene manager
    game_state = GameState()
    scene_manager = SceneManager(game_state)
    
    # Register all scenes with new symbolic progression
    scene_manager.register_scene("start", StartScreen)
    scene_manager.register_scene("garden", GardenScene)      # First moral choice
    scene_manager.register_scene("temple", TempleScene)      # Sacred architecture
    scene_manager.register_scene("mirrors", HouseOfMirrorsScene)
    scene_manager.register_scene("bridge", BridgeScene)      # Path of trials
    scene_manager.register_scene("caduceus", CaduceusScene)  # Balance of forces
    scene_manager.register_scene("dragon", DragonScene)      # Material attachment
    scene_manager.register_scene("serpent", SerpentRoom)     # Final transformation
    
    # Start with start screen
    scene_manager.switch_to("start")
    
    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0  # Delta time in seconds
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            scene_manager.handle_event(event)
            
        scene_manager.update(dt)
        scene_manager.draw(screen)
        pygame.display.flip()
    
    pygame.quit()

if __name__ == "__main__":
    main()
