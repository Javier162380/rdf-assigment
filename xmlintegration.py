"""we are going to merge two xml by the key station"""
from bs4 import BeautifulSoup

stffile = BeautifulSoup(open('StationFacilitiesNOH.xml', 'r'),'lxml')
setfset = set()
#i read the xml and create a dict station name as a key raw info.
diccionaries = {i.find('name').get_text().replace('\n','').replace(' ','').upper(): i
                for i in stffile.find_all('station')}

sftnfile = BeautifulSoup(open('StepFreeTubeNNone.xml', 'r'),'lxml')
stations = []
# i create and xml and i merge the two xml
for i in sftnfile.find_all('station'):
    station_info = ''
    raw_station = i.find('stationname')
    raw_naptans = i.find('naptans')
    raw_lines = i.find('lines')
    raw_public_toilet = i.find('publictoilet')
    raw_accessible_interchanges = i.find('accessibleinterchanges')
    station = raw_station.get_text().replace('\n', '').replace(' ', '').upper()
    if station in diccionaries.keys():
        STFdata = str(diccionaries[station]).split('</station>')[0]
        station_info=STFdata+str(raw_naptans)+\
                   str(raw_lines)+str(raw_public_toilet)+str(raw_accessible_interchanges)+'\n'+'</station>'+'\n'
        stations.append(station_info)
    else:
        pass

xml_final=''.join(i for i in stations)
TFLfacilities=BeautifulSoup(xml_final,'lxml')
with open('TFLfacilities.xml','w') as final:
    final.write(TFLfacilities.prettify())


