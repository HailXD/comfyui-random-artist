import json
import os
import random
import re


ARTISTS = []
RANDOM_CHOICE = "<random>"
ARTISTS_PATH = os.path.join(os.path.dirname(__file__), "artists_list.json")
WEIGHT_VALUES = list(range(50, 125, 5))


def _load_artists() -> None:
    global ARTISTS
    try:
        with open(ARTISTS_PATH, "r", encoding="utf-8") as handle:
            data = json.load(handle)
        if isinstance(data, list):
            ARTISTS = [str(item) for item in data if str(item).strip()]
        else:
            print("[random-artist] artists_list.json is not a list.")
            ARTISTS = []
    except Exception as exc:
        print(f"[random-artist] Failed to load artists_list.json: {exc}")
        ARTISTS = []


def _escape_parentheses(name: str) -> str:
    escaped = re.sub(r"(?<!\\)\(", r"\\(", name)
    escaped = re.sub(r"(?<!\\)\)", r"\\)", escaped)
    return escaped


_load_artists()


class RandomArtist:
    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("artists", "artists_semicolon")
    FUNCTION = "pick"
    CATEGORY = "Random"

    @classmethod
    def INPUT_TYPES(cls) -> dict:
        max_count = max(1, len(ARTISTS)) if ARTISTS else 1
        return {
            "required": {
                "n": ("INT", {"default": 3, "min": 0, "max": max_count}),
                "randomise_strength": (["Disabled", "Enabled"], {"default": "Disabled"}),
                "override": ("STRING", {"default": "", "multiline": True}),
                "prefix": ("STRING", {"default": "", "multiline": True}),
            },
        }

    @classmethod
    def IS_CHANGED(cls, **kwargs: object) -> float:
        return random.random()

    def pick(self, n: int, randomise_strength: str, override: str, prefix: str) -> tuple[str, str]:
        override_text = str(override) if override is not None else ""
        if override_text.strip():
            return (override_text, override_text)
        if not ARTISTS:
            return ("", "")
        count = max(0, int(n))
        if count == 0:
            return ("", "")
        if count <= len(ARTISTS):
            picks = random.sample(ARTISTS, count)
        else:
            picks = random.choices(ARTISTS, k=count)
        if str(randomise_strength).lower() == "enabled":
            weighted_picks = []
            for artist in picks:
                artist = _escape_parentheses(artist)
                weight_value = random.choice(WEIGHT_VALUES)
                if weight_value == 100:
                    weighted_picks.append(artist)
                    continue
                weight = weight_value / 100
                weight_str = f"{weight:.2f}".rstrip("0").rstrip(".")
                weighted_picks.append(f"({artist}:{weight_str})")
            combined = ", ".join(weighted_picks)
        else:
            combined = ", ".join(_escape_parentheses(artist) for artist in picks)
        combined_semicolon = combined.replace(":", ";").replace("\\", "")
        prefix_text = str(prefix) if prefix is not None else ""
        if prefix_text.strip():
            prefix_base = prefix_text.rstrip()
            if prefix_base.endswith(","):
                combined = f"{prefix_base} {combined}"
            else:
                combined = f"{prefix_base}, {combined}"
        return (combined, combined_semicolon)


NODE_CLASS_MAPPINGS = {
    "RandomArtist": RandomArtist,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "RandomArtist": "Random Artist",
}

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]
