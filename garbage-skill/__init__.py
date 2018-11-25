from mycroft import MycroftSkill, intent_handler, intent_file_handler
from adapt.intent import IntentBuilder
import json


class KretaGarbage(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    #handles the first intent being spoken -> when to put out trashcan?
    @intent_file_handler('garbage.kreta.intent')

    #handles the intent above, wants a response for a street
    def handle_garbage_kreta(self, message):
        street = self.get_response("street.kreta")

    #handles response above -> i live on <street>
    @intent_file_handler('street.kreta.intent')

    def handle_street_kreta(self, message):
        garbageJSON=open("/opt/mycroft/skills/kreta-garbage-skill.rayncooper/Trash_All_Streets.json").read()
        garbageData=json.loads(garbageJSON)
        street=message.data.get("street")
        try:
            #if you want dynamic responses: check the pdf "Abfallkalendar" and fix the data! (DB maybe?)
            for streetObj in garbageData["streets"]:
                streetObj["name"]=streetObj["name"].lower()
                if streetObj["name"] == street:
                    brownNextWeek = ["F", "G", "H", "I", "J"]
                    yellowNextWeek = ["3", "4", "5", "6", "7", "8", "9", "10", "11", "12"]
                    blueNextWeek = ["2", "3", "4", "5", "6"]

                    #counter to check for garbage pickups -> helps with concatenation below
                    garbagecount = 0
                    garbageTypes = ""

                    if streetObj["brown"] in brownNextWeek:
                        garbageTypes += "braun"
                        garbagecount += 1

                    if streetObj["blue"] in brownNextWeek:
                        if garbagecount > 0:
                            garbageTypes += " und blau"
                        elif garbagecount == 0:
                            garbageTypes += "blau"
                        garbagecount += 1

                    if streetObj["yellow"] in yellowNextWeek:
                        if garbagecount > 0:
                            garbageTypes += " und gelb"
                        elif garbagecount == 0:
                            garbageTypes += "gelb"
                        garbagecount += 1

                    if garbagecount == 0:
                        self.speak_dialog('nopickup.kreta')

                    if garbagecount > 0:
                        self.speak_dialog('garbage.kreta', {"garbagetype" : garbageTypes, "day": "naechste woche"})

                    return

            #raises exception if for-loop above can not find provided street
            raise ValueError('Does not exist')


        except Exception as e:
            self.speak_dialog('404.kreta', {"street" : street})

def create_skill():
    return KretaGarbage()
