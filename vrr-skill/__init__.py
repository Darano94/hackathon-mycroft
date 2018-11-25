from mycroft import MycroftSkill, intent_file_handler, intent_handler
from adapt.intent import IntentBuilder
from .VRRRequester import VRRRequester
import os

#https://mycroft.ai/documentation/skills/introduction-developing-skills/


class Vrr(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)
        self.requester=VRRRequester()
        
    #def initialize(self):
     #   self.requester=VRRRequester()
        
    #handles how can i get {to} request,
    #assuming VRRRRequester.home is already set
    
    def handle_route(self,origin,destination):
        query_response=self.requester.originToDestination(origin,destination)
        if (query_response == 0):
            self.speak_dialog('problem',{'origin':origin,'destination':destination})
        else:
            self.speak_dialog('vrr',query_response)
       
    
    @intent_file_handler('to.intent')
    def handle_smallquery(self,message):
        b = message.data.get("b")
        if self.requester.hasAHome() :
            #home is set, return route from home
            self.handle_route(self.requester.home,b)
        else:
            #home is not set, request home address
            self.speak('where do you live')
            
    @intent_file_handler('gethome.intent')
    def handle_get_street(self,message):
        #todo make more flexible
        street = message.data.get('street')
        success = self.requester.setHome(street)
        if success == False:
            self.speak('no such station '+street)
        else:
            self.speak('set home to '+self.requester.home)
        
    #handles how can i get {from} {to} request
    @intent_file_handler('how.intent')
    def handle_query(self,message):
        #print(os.getcwd())
        a = message.data.get("a")
        b = message.data.get("b")
        self.handle_route(a,b)
       


def create_skill():
    return Vrr()

