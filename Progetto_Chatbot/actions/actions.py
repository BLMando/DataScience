from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, FollowupAction
from rasa_sdk.types import DomainDict
from difflib import SequenceMatcher
import requests
from dotenv import load_dotenv
import os
from .utils import get_platform_id, get_genre_id, get_developer_slug, format_game_snapshot

load_dotenv()
API_KEY = os.getenv("RAWG_API_KEY")
BASE_URL = "https://api.rawg.io/api"


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
        if not slot_value:
            return {"platform": None}
        
        value = slot_value.lower().strip()
        
        # Accept skip variants
        if value in ["skip", "skipped", "no platform", "any", "none"]:
            return {"platform": "skipped"}
        
        # Check if it's a valid platform
        platform_id = get_platform_id(value)
        if platform_id:
            return {"platform": value}
        
        # Invalid input - ask again
        dispatcher.utter_message(text=f"🤔 I don't recognize '{slot_value}' as a platform. Try PC, PS5, Xbox, Switch, etc. or 'skip'.")
        return {"platform": None}

    def validate_genre(self, slot_value: Any, dispatcher: CollectingDispatcher, tracker: Tracker, domain: DomainDict) -> Dict[Text, Any]:
        if not slot_value:
            return {"genre": None}
        
        value = slot_value.lower().strip()
        
        # Accept skip variants
        if value in ["skip", "skipped", "no genre", "any", "none"]:
            return {"genre": "skipped"}
        
        # Check if it's a valid genre
        genre_id = get_genre_id(value)
        if genre_id:
            return {"genre": value}
        
        # Invalid input - ask again
        dispatcher.utter_message(text=f"🤔 I don't recognize '{slot_value}' as a genre. Try Action, RPG, Shooter, Adventure, etc. or 'skip'.")
        return {"genre": None}

    def validate_developer(self, slot_value: Any, dispatcher: CollectingDispatcher, tracker: Tracker, domain: DomainDict) -> Dict[Text, Any]:
        if not slot_value:
            return {"developer": None}
        
        value = slot_value.lower().strip()
        
        # Accept skip variants
        if value in ["skip", "skipped", "no developer", "any", "none"]:
            return {"developer": "skipped"}
        
        # Accept any developer name (we can't validate all possible developers)
        slug = value.replace(" ", "-")
        return {"developer": slug}

class ActionSearchGameByName(Action):
    """Search for a specific game by title."""
    
    def name(self) -> Text:
        return "action_search_game_by_name"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        entities = tracker.latest_message.get("entities", [])
        game_title_entity = next((e for e in entities if e["entity"] == "game_title"), None)
        game_title = tracker.get_slot("game_title")

        # Prioritize fresh entity over stale slot
        if game_title_entity:
            game_title = game_title_entity["value"]
        
        if not game_title:
            dispatcher.utter_message(response="utter_ask_game_name")
            return [SlotSet("game_title", None)]
        
        # Search for the game
        params = {
            "key": API_KEY,
            "search": game_title,
            "page_size": 1
        }

        try:
            response = requests.get(f"{BASE_URL}/games", params=params)
            response.raise_for_status()
            result = response.json().get("results", [])
            
            if not result:
                dispatcher.utter_message(response="utter_game_not_found")
                return [SlotSet("game_title", None)]
            
            format_game_snapshot(dispatcher, result[0])
            dispatcher.utter_message(response="utter_ask_game_details")
            return [SlotSet("game_id", str(result[0].get("id"))), SlotSet("game_title", None)]
    
        except Exception as e:
            print(f"❌ Error: {e}")
            dispatcher.utter_message(text="💥 Critical Hit! Something went wrong with the server. Please try again.")
            return [SlotSet("game_title", None), SlotSet("game_id", None)]

class ActionRecommendGames(Action):
    """Recommend games based on genre, platform, and developer filters."""
    
    def name(self) -> Text:
        return "action_recommend_games"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        genre = tracker.get_slot("genre")
        platform = tracker.get_slot("platform")
        developer = tracker.get_slot("developer")
        
        params = {
            "key": API_KEY,
            "page_size": 5,
            "ordering": "-rating"
        }
        
        # Check if all filters are skipped
        if (not genre or genre == "skipped") and \
           (not platform or platform == "skipped") and \
           (not developer or developer == "skipped"):
            params["page_size"] = 10
            dispatcher.utter_message(text="No filters? Going hardcore mode! 🕹️ Here are the top 10 games:")
        else:
            if genre and genre != "skipped":
                genre_id = get_genre_id(genre)
                params["genres"] = genre_id if genre_id else genre
                print(f"Genre: {genre}")

            if platform and platform != "skipped":
                platform_id = get_platform_id(platform)
                if platform_id:
                    params["platforms"] = platform_id if platform_id else platform
                print(f"Platform: {platform}")
            
            if developer and developer != "skipped":
                dev_slug = get_developer_slug(developer)
                params["developers"] = dev_slug
                print(f"Developer: {developer}")

        try:
            response = requests.get(f"{BASE_URL}/games", params=params)
            response.raise_for_status()
            data = response.json()
            results = data.get("results", [])
            
            if not results:
                dispatcher.utter_message(response="utter_game_not_found")
                return [
                    SlotSet("genre", None),
                    SlotSet("platform", None),
                    SlotSet("developer", None),
                    FollowupAction("game_search_form")
                ]

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
            print(f"❌ Error: {e}")
            dispatcher.utter_message(text="💥 Critical Hit! Something went wrong with the server. Please try again.")
            return [SlotSet("genre", None), SlotSet("platform", None), SlotSet("developer", None)]

        return [SlotSet("genre", None), SlotSet("platform", None), SlotSet("developer", None)]

class ActionGameDetails(Action):
    def name(self) -> Text:
        return "action_game_details"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        game_id = tracker.get_slot("game_id")
        game_title = tracker.get_slot("game_title")

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
                    "page_size": 1
                }
         
                try:
                    search_response = requests.get(f"{BASE_URL}/games", params=search_params)
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
            response = requests.get(f"{BASE_URL}/games/{game_id}", params=params)
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
            
            return [SlotSet("game_id", None), SlotSet("game_title", None)]

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

class ActionGameDLC(Action):
    def name(self) -> Text:
        return "action_game_dlc"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        game_id = tracker.get_slot("game_id")
        game_title = tracker.get_slot("game_title")

        # If no game_id, but game_title exists, search for ID
        if not game_id:
            if game_title:
                dispatcher.utter_message(text=f"🔍 Consulting the archives for {game_title}...")

                search_params = {
                    "key": API_KEY, 
                    "search": game_title, 
                    "page_size": 1
                }

                try:
                    search_response = requests.get(f"{BASE_URL}/games", params=search_params)
                    search_response.raise_for_status()
                    results = search_response.json().get("results", [])

                    if results:
                        game_id = results[0].get("id")
                    else:
                        dispatcher.utter_message(text=f"Couldn't find the game '{game_title}', so no DLC info is available.")
                        return [SlotSet("game_id", None), SlotSet("game_title", None)]
                except Exception as e:
                    print(f"❌ Error searching for game ID: {e}")
                    dispatcher.utter_message(text="💥 Something went wrong while searching for the game. Please try again.")
                    return [SlotSet("game_id", None), SlotSet("game_title", None)]
            else:
                dispatcher.utter_message(text="🤷‍♂️ I need a game first! Please search for one by title.")
                return []
        
        params = {
            "key": API_KEY,
            "page_size": 10   
        }

        # Now fetch DLCs using the game_id
        try:
            response = requests.get(f"{BASE_URL}/games/{game_id}/additions", params=params)
            response.raise_for_status()
            dlcs = response.json().get("results", [])

            if not dlcs:
                dispatcher.utter_message(text=f"No DLCs or editions found for this game.")
                return []

            message = f"DLCs and editions for {game_title}:\n"
            for dlc in dlcs:
                name = dlc.get("name")
                released = dlc.get("released", "N/A")
                message += f"• {name} (Released: {released})\n"

            dispatcher.utter_message(text=message)
            return [SlotSet("game_id", None), SlotSet("game_title", None)]

        except requests.exceptions.RequestException as e:
            print(f"❌ Error fetching DLCs: {e}")
            dispatcher.utter_message(text="💥 Something went wrong while fetching DLCs. Please try again later.")
            return [SlotSet("game_id", None), SlotSet("game_title", None)]

class ActionFetchGameSeries(Action):
    """Fetch related games belonging to the same series"""

    def name(self) -> Text:
        return "action_fetch_game_series"
    
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        game_id = tracker.get_slot("game_id")
        game_title = tracker.get_slot("game_title")

        # If no game_id, but game_title exists, search for ID
        if not game_id:
            if game_title:
                dispatcher.utter_message(text=f"🔍 Consulting the archives for {game_title}...")

                search_params = {
                    "key": API_KEY, 
                    "search": game_title, 
                    "page_size": 1
                }

                try:
                    search_response = requests.get(f"{BASE_URL}/games", params=search_params)
                    search_response.raise_for_status()
                    results = search_response.json().get("results", [])

                    if results:
                        game_id = results[0].get("id")
                    else:
                        dispatcher.utter_message(text=f"Couldn't find the game '{game_title}', so no info is available.")
                        return [SlotSet("game_id", None), SlotSet("game_title", None)]
                except Exception as e:
                    print(f"❌ Error searching for game ID: {e}")
                    dispatcher.utter_message(text="💥 Something went wrong while searching for the game. Please try again.")
                    return [SlotSet("game_id", None), SlotSet("game_title", None)]
            else:
                dispatcher.utter_message(text="🤷‍♂️ I need a game first! Please search for one by title.")
                return []
        
        params = {
            "key": API_KEY,
            "page_size": 10   
        }

        
        try:
            response = requests.get(f"{BASE_URL}/games/{game_id}/game-series", params=params)
            response.raise_for_status()
            results = response.json().get("results", [])

            if not results:
                dispatcher.utter_message(text=f"There aren't any related games in the series for this title.")
                return []

            message = f"Related games in the series for {game_title}:\n"
            for g in results:
                name = g.get("name")
                released = g.get("released", "N/A")
                rating = g.get("rating", "N/A")
                message += f"• {name} (Release: {released}, Rating: {rating})\n"

            dispatcher.utter_message(text=message)
            return [SlotSet("game_id", None), SlotSet("game_title", None)]

        except requests.exceptions.RequestException as e:
            print(f"❌ Internal error while retrieving the series: {e}")
            dispatcher.utter_message(text="💥 Internal error while retrieving the series. Please try again later.")
            return [SlotSet("game_id", None), SlotSet("game_title", None)]

class ActionGameStores(Action):
    """Fetch stores where the game can be purchased"""

    def name(self) -> Text:
        return "action_game_stores"
    
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        game_id = tracker.get_slot("game_id")
        game_title = tracker.get_slot("game_title")

        if not game_id:
            if game_title:
                dispatcher.utter_message(text=f"🔍 Consulting the archives for {game_title}...")

                search_params = {
                    "key": API_KEY, 
                    "search": game_title, 
                    "page_size": 1
                }

                try:
                    search_response = requests.get(f"{BASE_URL}/games", params=search_params)
                    search_response.raise_for_status()
                    results = search_response.json().get("results", [])

                    if results:
                        game_id = results[0].get("id")
                    else:
                        dispatcher.utter_message(text=f"Couldn't find the game '{game_title}', so no info is available.")
                        return [SlotSet("game_id", None), SlotSet("game_title", None)]
                except Exception as e:
                    print(f"❌ Error searching for game ID: {e}")
                    dispatcher.utter_message(text="💥 Something went wrong while searching for the game. Please try again.")
                    return [SlotSet("game_id", None), SlotSet("game_title", None)]
        else:
            dispatcher.utter_message(text="🤷‍♂️ I need a game first! Please search for one by title.")
            return []
            
        params = {
            "key": API_KEY,
            "page_size": 10   
        }

        try:
            stores_response = requests.get(f"{BASE_URL}/games/{game_id}/stores", params=params)
            stores_response.raise_for_status()
            results = stores_response.json().get("results", [])

            if not results:
                dispatcher.utter_message(text=f"No store information found for this game.")
                return [SlotSet("game_id", None), SlotSet("game_title", None)]
            
            
            message = f"Stores where you can buy the {game_title}:\n"
            for g in results:
                store_data = g.get("store", {})
                store_name = store_data.get("name")
                store_url = g.get("url")
                message += f"• {store_url}\n"

            dispatcher.utter_message(text=message)
            return [SlotSet("game_id", None), SlotSet("game_title", None)]

        except requests.exceptions.RequestException as e:
            print(f"❌ Internal error while retrieving the stores: {e}")
            dispatcher.utter_message(text="💥 Internal error while retrieving the stores. Please try again later.")
            return [SlotSet("game_id", None), SlotSet("game_title", None)]
            
           


                    



