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
        "playstation 5": 187, "ps5": 187,
        "playstation 4": 18, "ps4": 18,
        "xbox one": 1,
        "xbox series s/x": 186, "xbox series x": 186, "xbox series s": 186,
        "nintendo switch": 7, "switch": 7,
        "ios": 3, "android": 21,
        "nintendo 3ds": 8, "3ds": 8,
        "nintendo ds": 9, "ds": 9,
        "macos": 5, "mac": 5, "linux": 6,
        "xbox 360": 14, "xbox": 80,
        "playstation 3": 16, "ps3": 16,
        "playstation 2": 15, "ps2": 15,
        "playstation": 27, "ps1": 27, "psx": 27,
        "ps vita": 19, "vita": 19, "psp": 17,
        "wii u": 10, "wii": 11,
        "gamecube": 105, "nintendo 64": 83, "n64": 83,
        "game boy advance": 24, "gba": 24,
        "game boy color": 43, "gbc": 43,
        "game boy": 26, "gb": 26,
        "snes": 79, "nes": 49,
        "dreamcast": 106, "genesis": 167, "sega genesis": 167,
        "neo geo": 12
    }
    
    return mapping.get(platform_name)

def get_genre_id(genre_name: str) -> int:
    """Maps user-provided genre names to RAWG API Genre IDs."""
    if not genre_name:
        return None
    
    genre_name = genre_name.lower()
    
    mapping = {
        "action": 4, "indie": 51, "adventure": 3,
        "rpg": 5, "strategy": 10, "shooter": 2,
        "casual": 40, "simulation": 14, "puzzle": 7,
        "arcade": 11, "platformer": 83, "massively multiplayer": 59,
        "racing": 1, "sports": 15, "fighting": 6,
        "family": 19, "board games": 28, "board": 28,
        "card": 17, "educational": 34
    }
    
    return mapping.get(genre_name)

def get_developer_slug(developer_name: str) -> str:
    """Converts developer name to slug format for RAWG API."""
    if not developer_name:
        return None
    return developer_name.lower().replace(" ", "-")


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

