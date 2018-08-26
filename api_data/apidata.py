import requests
from bs4 import BeautifulSoup
from sys import argv

class tfl:
    """This class it is perform to retrieve information from the tfl api."""

    def __init__(self,api_id,api_key):
        self.api_id = api_id
        self.api_key = api_key
        self.session = requests.session()
        self.session.headers = {'api_id':self.api_id,'api_key':self.api_key}
        self.resource = {'stations_facilites': 'stations-facilities', 
                         'step_free_tube_guide': 'step-free-tube-guide'}


    def get_resource(self,search):
        if self.resource.get(search,None) is None:
            raise Exception("Recurso no encontrado")
        else:
            return self.session.get(f'https://data.tfl.gov.uk/tfl/syndication/feeds/'
                                    f'{self.resource[search]}.xml').text