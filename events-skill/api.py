from .opendataapi import OpenDataApi
from .meetupconsumer import MeetupConsumer
from datetime import datetime
from .utils import normalize_umlauts

class Api:
    def __init__(self):
        self.opendata = OpenDataApi()
        self.meetup = MeetupConsumer() 

    def get_event_with_location(self, event):
        '''
        Check if the event has a URL key, if so then fetch the location.
        It is implemented this way because each location of an open data entry
        needs a GET requests where as a meetups entry contains it on first fetch.
        This way, the location is only fetched if needed.
        '''
        if "URL" in event:
            location = self.opendata.get_location(event["URL"])
            event["venue"] = location["venue"]
            event["street_address"] = location["street_address"]
            event["city"] = location["city"]
        
        return event
            

    def get_json(self):
        '''
        Returns the combined and unified json of both apis.
        '''
        opendata = self._parse_opendata()
        meetup = self._parse_meetup()

        parse_date = lambda x: datetime.strptime(x, "%Y-%m-%d")
        events_in_future = [x for x in opendata + meetup if parse_date(x["local_date"]) > datetime.now()]

        for x in events_in_future:
            x["name"] = normalize_umlauts(x["name"])

        return events_in_future

    def _parse_meetup(self):  
        data = self.meetup.get_json() 
 
        keywords = ["name", "local_time", "local_date", "venue"]
        filtered = []

        for x in data["events"]:
            entry = {}
            for key, value in x.items():
                if key in keywords:
                    if key == "venue":
                        if "name" in value:
                            entry[key] = value["name"]
                        if "address_1" in value:
                            entry["street_address"] = value["address_1"]
                        if "city" in value:
                            entry["city"] = value["city"]
                    else:
                        entry[key] = value
            filtered.append(entry)
        
        return filtered 

    def _parse_opendata(self):
        data = self.opendata.get_json()
        
        keywords = ["DocName", "Start", "URL"]
        filtered = []

        for x in data:
            entry = {}
            for key, value in x.items():
                if key in keywords:
                    if key == "Start":
                        d = datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ")
                        entry["local_time"] = str(d.time())
                        entry["local_date"] = str(d.date()) 
                    else:
                        entry[key] = value
            filtered.append(entry)  

        mapped = self._map_keys(filtered, {"DocName": "name"})
        return mapped

    def _map_keys(self, data, mappings):
        mapped = []
        for x in data:
            entry = {}
            for key, value in x.items():
                if key in mappings:
                    entry[mappings[key]] = value
                else:
                    entry[key] = value
            mapped.append(entry)
        return mapped

