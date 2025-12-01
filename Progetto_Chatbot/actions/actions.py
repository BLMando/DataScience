from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import requests
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("RAWG_API_KEY")
BASE_URL = "https://api.rawg.io/api"

def get_platform_id(platform_name: str) -> int:
    """
    Maps user-provided platform names to RAWG API Platform IDs.
    """
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
        "nintendo dsi": 13,
        "dsi": 13,
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
        "classic macintosh": 55,
        "apple ii": 41,
        "commodore / amiga": 166,
        "commodore": 166,
        "amiga": 166,
        "atari 7800": 28,
        "atari 5200": 31,
        "atari 2600": 23,
        "atari flashback": 22,
        "atari 8-bit": 25,
        "atari st": 34,
        "atari lynx": 46,
        "atari xegs": 50,
        "genesis": 167,
        "sega genesis": 167,
        "sega saturn": 107,
        "saturn": 107,
        "sega cd": 119,
        "sega 32x": 117,
        "sega master system": 74,
        "master system": 74,
        "dreamcast": 106,
        "3do": 111,
        "jaguar": 112,
        "game gear": 77,
        "neo geo": 12
    }
    
    return mapping.get(platform_name)

def get_genre_id(genre_name: str) -> int:
    """
    Maps user-provided genre names to RAWG API Genre IDs.
    """
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
        "educational": 34
    }
    
    return mapping.get(genre_name)

class ActionSearchGame(Action):
    def name(self) -> Text:
        return "action_search_game"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        """
            Search for games based on genre and platform (if provided).

            params:
             - dispatcher: CollectingDispatcher
                - used to send messages back to the user
             - tracker: Tracker
                - used to access the user's current state
             - domain: Dict[Text, Any]
                - used to access the domain file
        """
        genre = tracker.get_slot("genre")
        platform = tracker.get_slot("platform")

        print(f"genre: {genre}, platform: {platform}")
        
        params = {
            "key": API_KEY,
            "page_size": 5,
            "ordering": "-rating" # Show top rated by default
        }

        if genre:
            genre_id = get_genre_id(genre)
            print(f"genre: {genre}, genre_id: {genre_id}")
            if genre_id:
                params["genres"] = genre_id
        
        if platform:
            platform_id = get_platform_id(platform)
        
            if platform_id:
                params["platforms"] = platform_id
        
        headers = {
            "User-Agent": "GameGuruChatbot/1.0"
        }

        print(params)

        try:
            response = requests.get(f"{BASE_URL}/games", params=params, headers=headers)
            response.raise_for_status()
            data = response.json()
            
            results = data.get("results", [])
            
            if not results:
                dispatcher.utter_message(text="I couldn't find any games with these criteria. Try changing genre or platform.")
                return []

            print(results)
            message = "Here are some games you might like:\n"
            for game in results:
                title = game.get("name")
                rating = game.get("rating", "N/A")
                platforms = game.get("platforms.platform.name", "N/A")
                background_image = game.get("background_image", "N/A")
                message += f"- {title} (Rating: {rating}/5)\n"
                message += f"Platforms: {platforms}\n"
                message += f"Background Image: {background_image}\n"
            
            dispatcher.utter_message(text=message)
            
        except Exception as e:
            dispatcher.utter_message(text="Ops. Something went wrong, please try again.")

        return []

class MyFallback(Action):
    
    def name(self) -> Text:
        return "action_my_fallback"

    def run(self, dispatcher: CollectingDispatcher,tracker: Tracker,domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(response = "utter_fallback")
        # reset slots
        return [SlotSet("game_title", None), SlotSet("genre", None), SlotSet("platform", None)]