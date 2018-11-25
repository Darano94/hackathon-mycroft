import requests

baseurl = "https://api.meetup.com"
event_route ="/find/upcoming_events"

#radius='smart' makes a good radius
defaultradius = "smart"
krefeldzipcode = "47798"
defaultzipcode = krefeldzipcode

class MeetupConsumer:

    def _getauthparameters(self):
        apikey = "15556e7c33805595a5d7c68487079"
        return "&sign=true&key=" + apikey
    
    def _makerequest(self, route, parameters):
        fields = ["id", "name", "status", "time", "local_time", "local_date", "venue.name", "group.name", "venue.city", "venue.address_1"]
        for i in range(0, len(fields) - 1):
            fields[i] = "events." + fields[i]
            
        fields_filter_str = "&only=" + (",".join(fields))
        
        url = baseurl + route
        url += "?" + ("&".join(parameters)) + self._getauthparameters() + fields_filter_str  

        return requests.get(url)
        
    def get_json(self):
        return self._makerequest(event_route, ["radius=" + defaultradius]).json()
