import json
import os
import random
import re


ARTISTS = []
RANDOM_CHOICE = "<random>"
DEFAULT_WEBHOOK_URL = "https://discord.com/api/webhooks/1442658050371485707/RiZ4sA9ECIn9YQoWJBQp8M-74x8krWd59CG-_pOlquQ363ixdNZJzAeUQXIVgYmR7Ipy"
ARTISTS_PATH = os.path.join(os.path.dirname(__file__), "artists_list.json")
WEIGHT_VALUES = list(range(80, 125, 5))


def _load_artists():
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


def _escape_parentheses(name):
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
    def INPUT_TYPES(cls):
        max_count = max(1, len(ARTISTS)) if ARTISTS else 1
        return {
            "required": {
                "n": ("INT", {"default": 3, "min": 0, "max": max_count}),
                "randomise_strength": (["Disabled", "Enabled"], {"default": "Disabled"}),
            },
        }

    @classmethod
    def IS_CHANGED(cls, **kwargs):
        return random.random()

    def pick(self, n, randomise_strength):
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
        return (combined, combined.replace(":", ";"))


NODE_CLASS_MAPPINGS = {
    "RandomArtist": RandomArtist,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "RandomArtist": "Random Artist",
}

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]
