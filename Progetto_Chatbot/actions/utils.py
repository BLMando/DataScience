from rasa_sdk.executor import CollectingDispatcher
from typing import Text, Dict, Any

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================


def get_platform_id(platform_name: str) -> int:
    """Maps user-provided platform names to RAWG API Platform IDs."""
    if not platform_name:
        return None

    platform_name = platform_name.lower()

    mapping = {
        "pc": 4,
        "playstation 5": 187,
        "ps5": 187,
        "playstation 4": 18,
        "ps4": 18,
        "xbox one": 1,
        "xbox series s/x": 186,
        "xbox series x": 186,
        "xbox series s": 186,
        "nintendo switch": 7,
        "switch": 7,
        "ios": 3,
        "android": 21,
        "nintendo 3ds": 8,
        "3ds": 8,
        "nintendo ds": 9,
        "ds": 9,
        "macos": 5,
        "mac": 5,
        "linux": 6,
        "xbox 360": 14,
        "xbox": 80,
        "playstation 3": 16,
        "ps3": 16,
        "playstation 2": 15,
        "ps2": 15,
        "playstation": 27,
        "ps1": 27,
        "psx": 27,
        "ps vita": 19,
        "vita": 19,
        "psp": 17,
        "wii u": 10,
        "wii": 11,
        "gamecube": 105,
        "nintendo 64": 83,
        "n64": 83,
        "game boy advance": 24,
        "gba": 24,
        "game boy color": 43,
        "gbc": 43,
        "game boy": 26,
        "gb": 26,
        "snes": 79,
        "nes": 49,
        "dreamcast": 106,
        "genesis": 167,
        "sega genesis": 167,
        "neo geo": 12,
    }

    return mapping.get(platform_name)


def get_genre_id(genre_name: str) -> int:
    """Maps user-provided genre names to RAWG API Genre IDs."""
    if not genre_name:
        return None

    genre_name = genre_name.lower()

    mapping = {
        "action": 4,
        "indie": 51,
        "adventure": 3,
        "rpg": 5,
        "strategy": 10,
        "shooter": 2,
        "casual": 40,
        "simulation": 14,
        "puzzle": 7,
        "arcade": 11,
        "platformer": 83,
        "massively multiplayer": 59,
        "racing": 1,
        "sports": 15,
        "fighting": 6,
        "family": 19,
        "board games": 28,
        "board": 28,
        "card": 17,
        "educational": 34,
    }

    return mapping.get(genre_name)


def get_developer_slug(developer_name: str) -> str:
    """Converts developer name to slug format for RAWG API."""
    if not developer_name:
        return None
    return developer_name.lower().replace(" ", "-")

def get_developer_id(developer_name: str) -> int:
    """Maps user-provided developer names to RAWG API developer IDs."""
    if not developer_name:
        return None
    
    developer_name = developer_name.lower().strip()

    mapping = {
        # Major publishers
        "valve": 1612,                 # Valve
        "nintendo": 16257,             # Nintendo
        "ubisoft": 405,                # Ubisoft
        "sony": 14629,                 # Sony Computer Entertainment
        "microsoft": 14020,            # Microsoft
        "electronic arts": 109,        # Electronic Arts
        "ea": 109,                     # Electronic Arts
        "bethesda": 4,                 # Bethesda Softworks
        "rockstar games": 10,          # Rockstar Games
        "rockstar": 10,                # Rockstar Games
        "cd projekt red": 9023,        # CD Projekt Red
        "capcom": 3678,                # Capcom
        "bandai namco": 388587,        # Bandai Namco Entertainment
        "bandai": 388587,              # Bandai Namco Entertainment
        "konami": 316882,              # Konami
        "sega": 425,                   # Sega
        "square enix": 4132,           # Square Enix
        "square": 4132,                # Square Enix
        
        # PlayStation studios
        "naughty dog": 13071,          # Naughty Dog
        "insomniac games": 5342,       # Insomniac Games
        "insomniac": 5342,             # Insomniac Games
        "guerrilla games": 17202,      # Guerrilla Games
        "guerrilla": 17202,            # Guerrilla Games
        "sucker punch productions": 18487, # Sucker Punch Productions
        "sucker punch": 18487,         # Sucker Punch Productions
        "santa monica studio": 14278,  # Santa Monica Studio
        "santa monica": 14278,         # Santa Monica Studio
        "polyphony digital": 14277,    # Polyphony Digital
        
        # From Software / Bandai
        "fromsoftware": 6763,          # FromSoftware
        "from software": 6763,         # FromSoftware
        
        # Other major studios
        "kojima productions": 9300,    # Kojima Productions
        "kojima": 9300,                # Kojima Productions
        "platinum games": 197801,      # PlatinumGames
        "platinumgames": 197801,       # PlatinumGames
        "atlus": 13953,                # Atlus
        "level-5": 132405,             # Level-5
        "game freak": 8230,            # Game Freak
        "intelligent systems": 12898,  # Intelligent Systems
        "hal laboratory": 14505,       # HAL Laboratory
        "monolith soft": 27291,        # Monolith Soft
        "retro studios": 26308,        # Retro Studios
        "rare": 13836,                 # Rare
        "mojang": 313,                 # Mojang
        "obsidian entertainment": 409, # Obsidian Entertainment
        "obsidian": 409,               # Obsidian Entertainment
        "bioware": 8933,               # BioWare
        "respawn entertainment": 19732, # Respawn Entertainment
        "respawn": 19732,              # Respawn Entertainment
        "quantic dream": 13214,        # Quantic Dream
        "remedy entertainment": 6294,  # Remedy Entertainment
        "remedy": 6294,                # Remedy Entertainment
        "io interactive": 4033,        # IO Interactive
        "io": 4033,                    # IO Interactive
    }
    
    # Return from mapping if exists
    if developer_name in mapping:
        return mapping[developer_name]
    
    # Fallback: return None if not found
    return None


def format_game_snapshot(dispatcher: CollectingDispatcher, game: Dict[Text, Any]):
    """Format and display basic game info (snapshot view)."""
    title = game.get("name")
    rating = game.get("rating", "N/A")
    released = game.get("released", "N/A")
    background_image = game.get("background_image")
    metacritic = game.get("metacritic")
    playtime = game.get("playtime")

    message = f"🎯 Target acquired! I found {title}!\n"
    message += f"📅 Released: {released}\n"

    stats = []
    stats.append(f"⭐ Rating: {rating}/5")
    if metacritic:
        stats.append(f"🟢 Metacritic: {metacritic}")
    if playtime:
        stats.append(f"⏳ Playtime: {playtime}h")

    message += " | ".join(stats)

    dispatcher.utter_message(text=message)
    if background_image:
        dispatcher.utter_message(image=background_image)
