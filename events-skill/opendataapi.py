import requests

class OpenDataApi:
    def __init__(self):
        self.base_url = "https://www.krefeld.de" 

    def get_json(self): 
        event_url = self.base_url + "/www/event.nsf/apijson.xsp/view-event-month?compact=true"
        r = requests.get(event_url)
        return r.json()

    def get_location(self, location_url): 
        r = requests.get(self.base_url + location_url)
        json = r.json()
        
        venue = json["LocationName"] if "LocationName" in json else None
        street_address = json["LocationStreetAddress"] if "LocationStreetAddress" in json else None
        city = json["LocationCity"] if "LocationCity" in json else None

        return {
            "venue": venue,
            "street_address": street_address,
            "city": city
        }
