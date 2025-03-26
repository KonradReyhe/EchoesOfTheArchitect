from enum import Enum
from dataclasses import dataclass
from typing import List, Dict, Optional

class SinType(Enum):
    PRIDE = "pride"
    ENVY = "envy"
    APATHY = "apathy"
    WRATH = "wrath"
    DECEPTION = "deception"

@dataclass
class SerpentManifestation:
    form: str
    message: str
    visual_effect: str
    required_light: int
    scene_specific: Dict[str, str]
    transformed: bool = False  # New property for transformation state

class SerpentWithin:
    def __init__(self, game_state):
        self.game_state = game_state
        self.current_form = None
        self.dominant_sin = None
        self.awakened = False
        self.named = False
        
        # Define serpent forms for each sin type
        self.manifestations = {
            SinType.PRIDE: SerpentManifestation(
                form="crowned_serpent",
                message="'Your wisdom exceeds their simple rules...'",
                visual_effect="golden_shimmer",
                required_light=3,
                scene_specific={
                    "garden": "coils_around_tree",
                    "temple": "wraps_around_pillar",
                    "mirrors": "wears_crown_reflection"
                }
            ),
            SinType.ENVY: SerpentManifestation(
                form="coiling_serpent",
                message="'They have what should be yours...'",
                visual_effect="shadow_tendrils",
                required_light=2,
                scene_specific={
                    "garden": "watches_fruit_tree",
                    "mirrors": "reflects_others_glory",
                    "temple": "circles_offerings"
                }
            ),
            SinType.APATHY: SerpentManifestation(
                form="grey_serpent",
                message="'Why bother? All paths lead nowhere...'",
                visual_effect="dulling_mist",
                required_light=1,
                scene_specific={
                    "garden": "blocks_traveler",
                    "mirrors": "clouds_reflection",
                    "temple": "dims_candles"
                }
            ),
            "wisdom": SerpentManifestation(  # New positive transformation
                form="caduceus_serpent",
                message="'As above, so below. The pattern reveals itself...'",
                visual_effect="divine_light",
                required_light=5,
                scene_specific={
                    "garden": "ascends_tree",
                    "temple": "forms_infinity",
                    "mirrors": "shows_true_form"
                }
            )
        }

    def update_sin_scores(self):
        """Track different types of sins based on player actions"""
        sin_scores = {
            SinType.PRIDE: 0,
            SinType.ENVY: 0,
            SinType.APATHY: 0
        }

        # Calculate pride score
        if self.game_state.get_choice("trusted_fox", False):
            sin_scores[SinType.PRIDE] += 2
        if not self.game_state.get_choice("prayed", False):
            sin_scores[SinType.PRIDE] += 1

        # Calculate envy score
        if self.game_state.get_choice("fruit_taken", False) and not self.game_state.get_choice("fruit_given", False):
            sin_scores[SinType.ENVY] += 2

        # Calculate apathy score
        if not any([
            self.game_state.get_choice("fruit_taken", False),
            self.game_state.get_choice("prayed", False),
            self.game_state.get_choice("scroll_warning_seen", False)
        ]):
            sin_scores[SinType.APATHY] += 3

        # Determine dominant sin
        self.dominant_sin = max(sin_scores.items(), key=lambda x: x[1])[0]

    def get_current_manifestation(self, scene_name: str) -> Optional[SerpentManifestation]:
        """Get the current serpent manifestation for the given scene"""
        if not self.dominant_sin:
            self.update_sin_scores()
        
        manifestation = self.manifestations.get(self.dominant_sin)
        if manifestation:
            return manifestation
        return None

    def can_be_confronted(self) -> bool:
        """Check if player has sufficient light score to confront their serpent"""
        light_score = self.game_state.get_choice("soul.light_score", 0)
        manifestation = self.get_current_manifestation("any")
        return light_score >= manifestation.required_light if manifestation else False

    def handle_confrontation(self, choice: str) -> str:
        """Handle player's choice when confronting their serpent"""
        if choice == "flee":
            self.game_state.set_choice("serpent_fled", True)
            return "emptiness"
        elif choice == "ignore":
            self.game_state.set_choice("serpent_ignored", True)
            return "pride"
        elif choice == "confront" and self.can_be_confronted():
            self.game_state.set_choice("serpent_confronted", True)
            if self.game_state.get_choice("memory_of_form", False):
                return "secret_echo"
            return "grace"
        return "current"  # No change in ending

    def get_whisper(self) -> str:
        """Get a context-appropriate serpent whisper"""
        manifestation = self.get_current_manifestation("any")
        return manifestation.message if manifestation else "Something stirs within..."

    def should_appear_in_scene(self, scene_name: str) -> bool:
        """Determine if serpent should manifest in current scene"""
        sin_score = self.game_state.get_choice("soul.sin_score", 0)
        light_score = self.game_state.get_choice("soul.light_score", 0)
        
        # Serpent appears more as sin grows, unless countered by light
        return sin_score > light_score and scene_name in ["garden", "mirrors", "temple"]

    def update_form(self):
        """Update the serpent's current form based on soul state"""
        sin_score = self.game_state.get_choice("soul.sin_score", 0)
        light_score = self.game_state.get_choice("soul.light_score", 0)
        
        # Determine dominant sin if not purified
        if sin_score > light_score:
            if self.game_state.get_choice("trusted_fox"):
                self.current_form = "pride"
            elif self.game_state.get_choice("fruit_taken") and not self.game_state.get_choice("fruit_given"):
                self.current_form = "envy"
            else:
                self.current_form = "apathy"
        else:
            self.current_form = "purified" 