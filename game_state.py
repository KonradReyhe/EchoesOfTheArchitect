import json
import os

class GameState:
    def __init__(self, save_file="data/flags.json"):
        self.save_file = save_file
        self.choices = {}
        self.load()

    def set_choice(self, key, value):
        self.choices[key] = value
        self.save()

    def get_choice(self, key):
        return self.choices.get(key, False)

    def add_score(self, key, amount):
        current = self.choices.get(key, 0)
        self.choices[key] = current + amount
        self.save()

    def save(self):
        with open(self.save_file, "w") as f:
            json.dump(self.choices, f)

    def load(self):
        if os.path.exists(self.save_file):
            with open(self.save_file, "r") as f:
                self.choices = json.load(f)
        else:
            self.choices = {
                "soul.light_score": 0,
                "soul.sin_score": 0,
                "soul.last_action": "none"
            }

# Make sure the class is available for import
__all__ = ['GameState']
