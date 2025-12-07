from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from rasa_sdk.types import DomainDict
from difflib import SequenceMatcher
import requests
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("RAWG_API_KEY")
BASE_URL = "https://api.rawg.io/api"

# Similarity function for comparing game names
def similarity(a, b):
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()

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


class ActionMyFallback(Action):
    def name(self) -> Text:
        return "action_my_fallback"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(response="utter_fallback")
        return [SlotSet("game_title", None), SlotSet("genre", None), SlotSet("platform", None)]


class ValidateGameSearchForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_game_search_form"

    def validate_platform(self, slot_value: Any, dispatcher: CollectingDispatcher, tracker: Tracker, domain: DomainDict) -> Dict[Text, Any]:
        if slot_value.lower() == "skipped":
            return {"platform": "skipped"}
        
        platform_id = get_platform_id(slot_value)
        if platform_id:
            return {"platform": slot_value}
        else:
            return {"platform": slot_value.lower()}

    def validate_genre(self, slot_value: Any, dispatcher: CollectingDispatcher, tracker: Tracker, domain: DomainDict) -> Dict[Text, Any]:
        if slot_value.lower() == "skipped":
            return {"genre": "skipped"}
        
        genre_id = get_genre_id(slot_value)
        if genre_id:
            return {"genre": slot_value}
        else:
            slug = slot_value.lower().replace(" ", "-")
            return {"genre": slug}

    def validate_developer(self, slot_value: Any, dispatcher: CollectingDispatcher, tracker: Tracker, domain: DomainDict) -> Dict[Text, Any]:
        if slot_value.lower() == "skipped":
            return {"developer": "skipped"}
        
        slug = slot_value.lower().replace(" ", "-")
        return {"developer": slug}


class ActionSearchGame(Action):
    def name(self) -> Text:
        return "action_search_game"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        """Search for games based on game title, genre, platform, or developer."""
        latest_message = tracker.latest_message
        intent = latest_message.get("intent", {}).get("name")
        entities = latest_message.get("entities", [])
        
        game_title_entity = next((e for e in entities if e["entity"] == "game_title"), None)
        game_title = tracker.get_slot("game_title")

        if intent == "search_game_by_name":
            if game_title_entity:
                game_title = game_title_entity["value"]
            elif not game_title:
                dispatcher.utter_message(response="utter_ask_game_name")
                return [SlotSet("game_title", None)]
        elif intent == "search_game":
            game_title = None
                
        if game_title:
            return self._handle_specific_search(dispatcher, game_title)
        else:
            return self._handle_recommendation_search(dispatcher, tracker)

    def _handle_specific_search(self, dispatcher: CollectingDispatcher, game_title: Text) -> List[Dict[Text, Any]]:
        """Dual-search strategy: compare flexible vs strict search and pick best match."""
        headers = {"User-Agent": "GameGuruChatbot/1.0"}
        base_params = {
            "key": API_KEY,
            "search": game_title,
            "page_size": 1,
            "search_precise": True,
            "ordering": "-rating"
        }

        try:
            # Search 1: Flexible (search_exact=False)
            params = {**base_params, "search_exact": False}
            print(f"🔍 Flexible search for '{game_title}'")
            response = requests.get(f"{BASE_URL}/games", params=params, headers=headers)
            response.raise_for_status()
            result_flexible = response.json().get("results", [])

            # Search 2: Strict (search_exact=True)
            params = {**base_params, "search_exact": True}
            print(f"🔍 Strict search for '{game_title}'")
            response = requests.get(f"{BASE_URL}/games", params=params, headers=headers)
            response.raise_for_status()
            result_strict = response.json().get("results", [])

            # Pick best match based on similarity score
            candidates = []
            if result_flexible:
                score = similarity(result_flexible[0]["name"], game_title)
                candidates.append((result_flexible[0], score, "flexible"))
            if result_strict:
                score = similarity(result_strict[0]["name"], game_title)
                candidates.append((result_strict[0], score, "strict"))

            if not candidates:
                dispatcher.utter_message(response="utter_game_not_found")
                return [SlotSet("game_title", None), SlotSet("genre", None), SlotSet("platform", None), SlotSet("developer", None)]

            # Select best match by highest similarity score
            best_match, best_score, source = max(candidates, key=lambda x: x[1])
            print(f"🎯 Best match: '{best_match['name']}' (Score: {best_score:.2f}, Source: {source})")
                 
            self._format_game_snapshot(dispatcher, best_match)
            dispatcher.utter_message(response="utter_ask_game_details")
            return [SlotSet("game_id", str(best_match.get("id"))), SlotSet("game_title", best_match.get("name"))]
    
        except Exception as e:
            print(f"❌ Error: {e}")
            dispatcher.utter_message(text="💥 Critical Hit! Something went wrong with the server. Please try again.")
            return [SlotSet("genre", None), SlotSet("platform", None), SlotSet("developer", None), SlotSet("game_title", None)]

    def _handle_recommendation_search(self, dispatcher: CollectingDispatcher, tracker: Tracker) -> List[Dict[Text, Any]]:
        genre = tracker.get_slot("genre")
        platform = tracker.get_slot("platform")
        developer = tracker.get_slot("developer")
        
        params = {
            "key": API_KEY,
            "page_size": 5,
            "ordering": "-rating"
        }
        
        if (not genre or genre == "skipped") and \
           (not platform or platform == "skipped") and \
           (not developer or developer == "skipped"):
            params["page_size"] = 10
            dispatcher.utter_message(text="No filters? Going hardcore mode! 🕹️ Here are the top 10 games:")
        else:
            if genre and genre != "skipped":
                genre_id = get_genre_id(genre)
                params["genres"] = genre_id if genre_id else genre

            if platform and platform != "skipped":
                platform_id = get_platform_id(platform)
                if platform_id:
                    params["platforms"] = platform_id
            
            if developer and developer != "skipped":
                dev_slug = get_developer_slug(developer)
                params["developers"] = dev_slug

        headers = {"User-Agent": "GameGuruChatbot/1.0"}
        print(f"Requesting games with params: {params}")

        try:
            response = requests.get(f"{BASE_URL}/games", params=params, headers=headers)
            response.raise_for_status()
            data = response.json()
            results = data.get("results", [])
            
            if not results:
                dispatcher.utter_message(response="utter_game_not_found")
                return [SlotSet("game_title", None), SlotSet("genre", None), SlotSet("platform", None), SlotSet("developer", None)]

            # Construct dynamic header
            header_parts = ["📦 Loot drop! Here are some"]
            if developer and developer != "skipped":
                header_parts.append(f"{str(developer).upper()}")
            if genre and genre != "skipped":
                header_parts.append(f"{str(genre).upper()}")
            header_parts.append("games")
            if platform and platform != "skipped":
                header_parts.append(f"for {str(platform).upper()}")
            header_parts.append("you might like:\n")
            
            dispatcher.utter_message(text=" ".join(header_parts))

            for game in results:
                title = game.get("name")
                rating = game.get("rating", "N/A")
                background_image = game.get("background_image")
                
                game_msg = f"🎮 {title} \n⭐ Rating: {rating}/5\n"
                
                details = []
                if not genre or genre == "skipped":
                    genres = [g.get("name") for g in game.get("genres", [])]
                    if genres:
                        details.append(f"🎭 Genre: {', '.join(genres)}")

                if not platform or platform == "skipped":
                    platforms = [p.get("platform", {}).get("name") for p in game.get("platforms", [])]
                    if platforms:
                        details.append(f"💻 Platforms: {', '.join(platforms)}")
                
                if details:
                    game_msg += "\n".join(details)
                
                if background_image:
                    dispatcher.utter_message(text=game_msg, image=background_image)
                else:
                    dispatcher.utter_message(text=game_msg)

        except Exception as e:
            print(f"Error: {e}")
            dispatcher.utter_message(text="💥 Critical Hit! Something went wrong with the server. Please try again.")
            return [SlotSet("genre", None), SlotSet("platform", None), SlotSet("developer", None), SlotSet("game_title", None)]

        return [SlotSet("genre", None), SlotSet("platform", None), SlotSet("developer", None)]

    def _format_game_snapshot(self, dispatcher: CollectingDispatcher, game: Dict[Text, Any]):
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


class ActionGameDetails(Action):
    def name(self) -> Text:
        return "action_game_details"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        game_id = tracker.get_slot("game_id")
        game_title = tracker.get_slot("game_title")
        headers = {"User-Agent": "GameGuruChatbot/1.0"}

        latest_message = tracker.latest_message
        entities = latest_message.get("entities", [])
        
        # Check for game_id from button payload
        fresh_game_id = next((e["value"] for e in entities if e["entity"] == "game_id"), None)
        if fresh_game_id:
            game_id = fresh_game_id
        
        fresh_game_title = next((e["value"] for e in entities if e["entity"] == "game_title"), None)
        if fresh_game_title:
            game_title = fresh_game_title
            game_id = None
        
        if not game_id:
            if game_title:
                dispatcher.utter_message(text=f"🔍 Consulting the archives for {game_title}...")
                search_params = {
                    "key": API_KEY,
                    "search": game_title,
                    "page_size": 1,
                    "search_precise": True,
                    "search_exact": True
                }
         
                try:
                    search_response = requests.get(f"{BASE_URL}/games", params=search_params, headers=headers)
                    search_response.raise_for_status()
                    search_data = search_response.json()
                    results = search_data.get("results", [])
                    
                    if results:
                        game_id = results[0].get("id")
                    else:
                        dispatcher.utter_message(text=f"💨 The game '{game_title}' vanished like a ninja! I couldn't find it.")
                        return [SlotSet("game_id", None), SlotSet("game_title", None)]
                except Exception as e:
                    print(f"Error searching for game ID: {e}")
                    dispatcher.utter_message(text="👾 Glitch in the system! I couldn't find the details.")
                    return [SlotSet("game_id", None), SlotSet("game_title", None)]
            else:
                buttons = [{"title": "🔍 Search for a Game", "payload": "/search_game"}]
                dispatcher.utter_message(text="🤷‍♂️ I've lost the target! Which game are we talking about? Please search for it first.", buttons=buttons)
                return []

        params = {"key": API_KEY}
        
        try:
            response = requests.get(f"{BASE_URL}/games/{game_id}", params=params, headers=headers)
            response.raise_for_status()
            game = response.json()
            
            title = game.get("name")
            description = game.get("description_raw", "")
            if len(description) > 300:
                description = description[:300] + "..."
            
            released = game.get("released", "N/A")
            rating = game.get("rating", "N/A")
            metacritic = game.get("metacritic", "N/A")
            playtime = game.get("playtime", "N/A")
            esrb = game.get("esrb_rating")
            esrb_name = esrb.get("name") if esrb else "N/A"
            
            developers = [d.get("name") for d in game.get("developers", [])]
            genres = [g.get("name") for g in game.get("genres", [])]
            platforms = [p.get("platform", {}).get("name") for p in game.get("platforms", [])]
            
            website = game.get("website")
            background_image = game.get("background_image")

            # Build detailed message
            message = f"🎮 {title}\n\n"
            message += f"📖 {description}\n\n"
            
            message += f"📅 Released: {released}\n"
            message += f"⭐ Rating: {rating}/5\n"
            message += f"🟢 Metacritic: {metacritic}\n"
            message += f"⏳ Avg Playtime: {playtime}h\n"
            message += f"🔞 ESRB: {esrb_name}\n\n"
            
            if developers:
                message += f"🏢 Developers: {', '.join(developers)}\n"
            if genres:
                message += f"🎭 Genres: {', '.join(genres)}\n"
            if platforms:
                message += f"💻 Platforms: {', '.join(platforms)}\n"
            if website:
                message += f"🌐 Website: {website}\n"
            
            dispatcher.utter_message(text=message)
            if background_image:
                dispatcher.utter_message(image=background_image)

            # PC Requirements
            for platform_info in game.get("platforms", []):
                if platform_info.get("platform", {}).get("id") == 4:
                    requirements = platform_info.get("requirements", {})
                    if requirements:
                        min_req = requirements.get("minimum", "")
                        rec_req = requirements.get("recommended", "")
                        if min_req or rec_req:
                            req_msg = "🖥️ PC Requirements:\n"
                            if min_req:
                                req_msg += f"Minimum:\n{min_req}\n"
                            if rec_req:
                                req_msg += f"Recommended:\n{rec_req}\n"
                            dispatcher.utter_message(text=req_msg)
                    break
            
            return [SlotSet("game_id", str(game_id)), SlotSet("game_title", title)]

        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                dispatcher.utter_message(text=f"❌ Game not found! The game with ID '{game_id}' doesn't exist.")
            else:
                dispatcher.utter_message(text="👾 Glitch in the system! I couldn't fetch the game details.")
            return [SlotSet("game_id", None), SlotSet("game_title", None)]
        except Exception as e:
            print(f"Error: {e}")
            dispatcher.utter_message(text="💥 Critical Hit! Something went wrong. Please try again.")
            return [SlotSet("game_id", None), SlotSet("game_title", None)]