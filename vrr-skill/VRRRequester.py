import requests
import time
import datetime
import json
import os
from difflib import SequenceMatcher

#z.B. print(originToDestination("Inrath", "Verberg"))

class VRRRequester:
    def __init__(self):
        self.home = ""  
    
    def similar(self,a,b):
        return SequenceMatcher(None,a,b).ratio()
    
    def originToDestination(self,origin, destination):
        if(origin == "" and self.home == ""):
            return "Es ist kein Home und kein Anfangspunkt gegeben."
        url = "http://pda.vrr.de/vrr_mobile/XSLT_TRIP_REQUEST2"
        
        now = datetime.datetime.now()
        hour = now.hour + 1
        minute = now.minute

        payload = 'language=de&sessionID=0&requestID=0&command=&execInst=&ptOptionsActive=1&itOptionsActive=1&imageFormat=PNG&imageWidth=400&imageHeight=300&imageOnly=1&imageNoTiles=1&itdLPxx_advancedOptions=0&itdLPxx_odvPPType=&itdLPxx_execInst=&itdDateDay=24&itdDateMonth=11&itdDateYear=2018&lineRestriction=403&placeState_origin=empty&placeState_origin=empty&nameState_origin=empty&nameState_origin=empty&placeInfo_origin=invalid&nameInfo_origin=invalid&typeInfo_origin=invalid&ANSIMacro=true&ANSIMacro=true&place_origin=Krefeld&type_origin=stop&name_origin=' + origin + '&placeState_destination=empty&placeState_destination=empty&nameState_destination=empty&nameState_destination=empty&placeInfo_destination=invalid&nameInfo_destination=invalid&typeInfo_destination=invalid&place_destination=Krefeld&type_destination=stop&name_destination=' + destination + '&itdTimeHour=' + str(hour) + '&itdTimeMinute=' + str(minute) + '&itdDate=20181124&itdTripDateTimeDepArr=dep'
        headers = {
            'Connection': "keep-alive",
            'Cache-Control': "max-age=0",
            'Origin': "http://pda.vrr.de",
            'Upgrade-Insecure-Requests': "1",
            'Content-Type': "application/x-www-form-urlencoded",
            'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36",
            'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            'Referer': "http://pda.vrr.de/vrr_mobile/XSLT_TRIP_REQUEST2?language=de",
            'Accept-Encoding': "gzip, deflate",
            'Accept-Language': "en-GB,en-US;q=0.9,en;q=0.8",
            'Cookie': "vrr-ef-lb=104310976.20480.0000",
            'cache-control': "no-cache",
            'Postman-Token': "b67849ab-1f1c-4366-820b-311bcc47a3cf"
            }

        try:
            response = requests.request("POST", url, data=payload, headers=headers)

            list_of_words = response.text.split()
            length = list_of_words[list_of_words.index("<b>Dauer:") + 1].split('<')
        
            index = 0
            for i in range(len(list_of_words)):
                if('&amp;requestID=1&amp;command=nop&amp;tripSelection=on&amp;itdLPxx_view=detail_2">' in list_of_words[i]):
                    index = i
                    break
                    raise ValueError('A very specific bad thing happened.')

            time = list_of_words[index]
            time = time[-5:]
            #return {"origin":"origin", "time":"time", "duration":"duration"}
            return {"origin":origin, "time":time, "duration":length[0]}
            
        except:
            return 0
    
    def setHome(self, stop):
        #Überprüfe ob Haltestelle existiert
        filename='/opt/mycroft/skills/vrr-skill/convertcsv.json'
        #return True
        with open(filename,'r') as f:
            data = json.load(f)
            for i in range(len(data)):
                haltestelle = data["Krefeld"][i]["Name ohne Ort"]
                ratio = self.similar(haltestelle,stop)
                if(ratio > 0.3):
                    print(stop)
                    
                if(ratio >0.4):
                    #Die Haltestelle ist vorhanden
                    self.home=haltestelle
                    return True
            return False   

    #test
    def hasAHome(self):
        if(self.home != ""):
            return True
        else:
            return False

    def setTimer(self,timeToWait):
        for i in range(len(timeToWait)):
            time.sleep(1)
        string = "Der Timer ist beendet!"
        return string

    #z.B. print(calcCosts("einfache"))
    def calcCosts(self,typeOfCard):
        typeOfCardDict = {
            "einfache": 1.60,
            "gruppen": 13.60,
            "semester": 132.72,
            "4er": 5.90,
            "Tages": 6.80
        }
        string = 'Eine {} Fahrkarte kostet {} Euro.'
        string = string.format(typeOfCard, typeOfCardDict[typeOfCard])
        return string
