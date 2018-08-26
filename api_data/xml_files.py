import os
import apidata
from bs4 import BeautifulSoup
from dotenv import load_dotenv,find_dotenv

load_dotenv(find_dotenv())

#we extract the data from the tfl api.
tflobject = apidata.tfl(os.getenv("APPLICATION_ID"), os.getenv("APPLICATION_KEY"))
station_facilites = tflobject.get_resource('stations_facilites')
step_free_tube_guide = tflobject.get_resource('step_free_tube_guide')

#we parse the response from each response and we create each xml.
station_facilites_parser = BeautifulSoup(station_facilites,'lxml')

for station in station_facilites_parser.find_all('openinghours'):
    station.replaceWith('')

with open('StationFacilitiesNOH.xml', 'w') as sf:
     sf.write(station_facilites_parser.prettify())

step_free_tube_guide = BeautifulSoup(step_free_tube_guide,'lxml')


for accessibilitytype in step_free_tube_guide.find_all('accessibilitytype'):
    if accessibilitytype:
        accessibilitytype.clear()
    else:
        accessibilitytype.replaceWith('')

with open('cosa.xml', 'w') as sft:
    sft.write(step_free_tube_guide.prettify())

