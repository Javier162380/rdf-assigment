
import requests
from bs4 import BeautifulSoup
from sys import argv

class tfl(object):
    """This class it is perform to retrieve information from the tfl api."""

    def __init__(self,api_id,api_key):
        self.api_id = api_id
        self.api_key = api_key
        self.session = requests.session()
        self.session.headers = {'api_id':self.api_id,'api_key':self.api_key}
        self.resource = {'stations_facilites': 'stations-facilities', 'step_free_tube_guide': 'step-free-tube-guide'}


    def get_resource(self,search):
        if self.resource.get(search,None) is None:
            raise Exception("Recurso no encontrado")
        else:
            return self.session.get('https://data.tfl.gov.uk/tfl/syndication/feeds/'+self.resource.get(search, None) +
                                    '.xml').text


#we extract the data from the tfl api.
tflobject = tfl(argv1, argv2)
station_facilites = tflobject.get_resource('stations_facilites')
step_free_tube_guide = tflobject.get_resource('step_free_tube_guide')

#we parse the response from each response and we create each xml.
station_facilites_parser = BeautifulSoup(station_facilites,'lxml')

for i in station_facilites_parser.find_all('openinghours'):
    i.replaceWith('')

with open('StationFacilitiesNOH.xml', 'w') as sf:
     sf.write(station_facilites_parser.prettify())

step_free_tube_guide = BeautifulSoup(step_free_tube_guide,'lxml')


for i in step_free_tube_guide.find_all('accessibilitytype'):
    if i is None:
        i.replaceWith('')
    else:
        i.clear()

with open('StepFreeTubeNNone.xml', 'w') as sft:
    sft.write(step_free_tube_guide.prettify())

