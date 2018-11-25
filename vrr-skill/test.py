import os
import json

stop='inrath'
filename='/opt/mycroft/skills/vrr-skill/convertcsv.json'

def clean(str):
    return str.lstrip(' ').rstrip(' ').lower()

def similar(astr,bstr):
    a2=clean(astr)
    b2=clean(bstr)
    if(

with open(filename,'r') as f:
    data = json.load(f)
    print(data["Krefeld"][0])
    for i in range(len(data)):
        print(data["Krefeld"][i]["Name ohne Ort"])
        if(data["Krefeld"][i]["Name ohne Ort"] == stop):
            #Die Haltestelle ist vorhanden
            self.home=stop
            print('true')
    print('false')
