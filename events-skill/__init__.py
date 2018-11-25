from mycroft import MycroftSkill, intent_file_handler, util
from random import choice
from .api import Api
from .utils import normalize_umlauts

class Events(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)
        self.last_response = {"dialog": None, "args": None}
        self.api = Api()

    @intent_file_handler('events.random.intent')
    def handle_random_event(self, message):
        data = self.api.get_json()

        if len(data) == 0:
            self.speak("I could not find any events in Krefeld")
            return

        # Select one event and get its location
        event = self.api.get_event_with_location(choice(data))

        args = {
            "name": event["name"],
            "place": event["venue"],
            "date": event["local_date"],
            "time": event["local_time"]
        }

        self._save_last_event(event)
        
        self.last_response["dialog"] = "events.random"
        self.last_response["args"] = args
        self.speak_dialog("events.random", args)

    @intent_file_handler("events.problem.intent")
    def handle_problem(self, message):
        if self.last_response["dialog"] is None:
            self.speak_dialog("events.problem.nothing")
            return

        self.speak_dialog(self.last_response["dialog"], self.last_response["args"])

    @intent_file_handler('events.whatsup.intent')
    def handle_whatsup(self, message):
        events = self.api.get_json()

        if len(events) == 0:
            self.speak("I could not find any events in Krefeld")
            return
        
        count = 0
        for event in events[:2]:
            # Get location to event
            event = self.api.get_event_with_location(event)
            name = normalize_umlauts(event["name"])
            venue = normalize_umlauts(event["venue"])

            args = {
                "name": name,
                "venue": venue
            }

            self.last_response["dialog"] = "events.whatsup"
            self.last_response["args"] = args

            if count == 0:
                self.speak_dialog("events.whatsup", args)
            else:
                self.speak_dialog("events.whatsup2", args)
            count += 1

    def _save_last_event(self, event):
        """
        Saves the last event to a text file, so that other skills
        can communicate based on the information given.
        """
        with open("/tmp/last_event.txt", "w+") as file:
            if "name" in event and "street_address" in event and "city" in event\
                and event["name"] is not None and event["street_address"] is not None\
                and event["city"] is not None:
                name = event["name"]
                street_address = event["street_address"]
                city = event["city"]            
                file.write(name + "\n")
                file.write(street_address + "\n")
                file.write(city + "\n")
            else:
                file.write("NOT_FOUND")
    
def create_skill():
    return Events()

