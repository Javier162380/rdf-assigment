from bs4 import BeautifulSoup

stffile = BeautifulSoup(open('StationFacilitiesNOH.xml', 'r'),'lxml')

setfset = set()

for i in stffile.find_all('name'):
    try:
        station = i.get_text().replace('\n','').replace(' ','').upper()
        setfset.add(station)
    except:
        pass

sftnfile = BeautifulSoup(open('StepFreeTubeNNone.xml', 'r'),'lxml')

for i in sftnfile.find_all('station'):
    try:
        add_variable = i
        raw_data = i.find('stationname')
        print(raw_data)
        station = raw_data.get_text().replace('\n', '').replace(' ', '').upper()
        print(station)
        if station in setfset:
            stffile.append(add_variable)
            print('esta')
        else:
            print('noesta')
            pass
    except:
        pass

with open('final1.xml','w') as final:
    final.write(stffile.prettify())


