import json
import os

class GameState:
    def __init__(self, save_file="data/flags.json"):
        self.save_file = save_file
        self.choices = {
            "sacred_items": {
                "bell_of_awakening": False,    # Dispels illusions
                "hermes_staff": False,         # Balance of opposites
                "eye_of_architect": False,     # Divine vision
                "griffin_feather": False,      # Divine-earthly union
                "sacred_geometry": False       # Universal patterns
            },
            "world_state": {
                "chaos_level": 3,             # Decreases with understanding
                "divine_awareness": 0,         # Increases with discoveries
                "bells_rung": [],             # Cleansed locations
                "patterns_revealed": []        # Discovered sacred geometry
            },
            "soul": {
                "light_score": 0,
                "sin_score": 0,
                "memory_of_form": False,
                "inner_serpent": None,
                "scroll_warning_seen": False,
                "fruit_taken": False,
                "fruit_given": False,
                "trusted_fox": False,
                "granted_feather": False
            },
            "inventory": {
                "has_feather": False,
                "has_mirror_shard": False,
                "has_false_key": False,
                "has_true_key": False
            },
            "puzzles": {
                "mirror_solved": False,
                "scroll_revealed": False,
                "fox_encountered": False,
                "key_forged": False
            }
        }
        
        # Create data directory if it doesn't exist
        os.makedirs(os.path.dirname(save_file), exist_ok=True)
        
        self.load()
        
        # Initialize puzzle state if new game
        if not self.choices:
            self.choices = {
                "soul": {
                    "light_score": 0,
                    "sin_score": 0,
                    "memory_of_form": False,
                    "inner_serpent": None,
                    "scroll_warning_seen": False,
                    "fruit_taken": False,
                    "fruit_given": False,
                    "trusted_fox": False,
                    "granted_feather": False
                },
                "inventory": {
                    "has_feather": False,
                    "has_mirror_shard": False,
                    "has_false_key": False,
                    "has_true_key": False
                },
                "puzzles": {
                    "mirror_solved": False,
                    "scroll_revealed": False,
                    "fox_encountered": False,
                    "key_forged": False
                }
            }

    def can_see_hidden(self):
        """Check if player can see veiled content"""
        return (self.get_choice("prayed") or 
                not self.get_choice("fruit_taken"))

    def can_forge_key(self):
        """Check if player has components for true key"""
        return (self.choices["inventory"]["has_feather"] and 
                self.choices["inventory"]["has_mirror_shard"] and 
                self.choices["soul"]["memory_of_form"])

    def get_soul_state(self):
        """Determine current soul condition"""
        light = self.get_choice("soul.light_score", 0)
        sin = self.get_choice("soul.sin_score", 0)
        
        if light >= 2 and self.get_choice("soul.memory_of_form"):
            return "purified"
        elif sin > light:
            if self.get_choice("soul.trusted_fox"):
                return "pride"
            elif self.get_choice("soul.fruit_taken") and not self.get_choice("soul.fruit_given"):
                return "envy"
            return "apathy"
        return "neutral"

    def set_choice(self, key, value):
        """Set a game state flag"""
        self.choices[key] = value
        self.save()

    def get_choice(self, key, default=False):
        """Get a game state flag"""
        return self.choices.get(key, default)

    def add_score(self, key, amount):
        """Modify a soul score"""
        current = self.choices.get(key, 0)
        self.choices[key] = current + amount
        self.save()

    def save(self):
        """Save game state to file"""
        with open(self.save_file, "w") as f:
            json.dump(self.choices, f)

    def load(self):
        """Load game state from file"""
        if os.path.exists(self.save_file):
            with open(self.save_file, "r") as f:
                self.choices = json.load(f)

# Make sure the class is available for import
__all__ = ['GameState']
