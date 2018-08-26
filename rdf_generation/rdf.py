import sys
import os 
from rdflib import Graph, Literal, URIRef,BNode
from rdflib.namespace import FOAF,RDF
from rdflib.plugin import register, Parser
from bs4 import BeautifulSoup
from namespaces import namespaces

def format_string(string):
	if type(string) is str:
		return string.replace('\n','').replace(' ','')

def get_text(string):
	if string:
		return string.get_text()

def parse_xml_tag(string):
	if hasattr(string,'text'):
		string.text

def station_general_charateristics(station_graph,station_node,
								  stationtype,stationid,stationname):
	station_graph.add((station_node,namespaces['station_namespace'], 
						Literal(format_string(stationname))))
	station_graph.add((station_node, namespaces['station_type'], 
						Literal(format_string(stationtype))))
	station_graph.add((station_node, namespaces['station_id'], 
						Literal(format_string(stationid))))

def station_general_information(station_graph, station_node, contact_node, 
								address,phone, serviceline):
	station_graph.add((station_node,namespaces['contactdetails'],contact_node))
	station_graph.add((contact_node,namespaces['contactdetailsphone'],
						Literal(format_string(phone))))
	station_graph.add((contact_node,namespaces['contactdetailsaddress'],
						Literal(format_string(address))))
	for line in serviceline:
		if format_string(line.text):
			station_graph.add((contact_node,namespaces['serviceline'],
								Literal(format_string(line.text))))

def station_facilities(station_graph,facilities_node,facility_iterator):
	facility_node = BNode()
	station_graph.add((facilities_node,namespaces['facilities'],
							  facility_node))
	for facility in facility_iterator:
		facility_name = facility.attrs['name']
		facility_description = format_string(facility.get_text())
		station_graph.add((facility_node,namespaces[facility_name],
						  Literal(facility_description)))

def station_zone(station_graph,station_node, zone_object):
	if zone_object:
		zones_node = BNode()
		station_graph.add((station_node,namespaces['zones'],zones_node))
		for zone_node in zone_object.findAll('zone'):
			station_graph.add((zones_node,namespaces['zone'], 
							   Literal(format_string(zone_node.text))))

def station_entrance_booking_hall(station_graph,entrance_object, entrance_node):
	if entrance_object.findAll('bookingHallToPlatform'):
		for bookinghall in entrance_object.findAll('bookingHallToPlatform'):
			bookingHallToPlatform = BNode()
			station_graph.add((entrance_node, namespaces['entrancebookingplatform'], 
							  bookingHallToPlatform))

			for pathXMLNode in bookinghall.findall('path'):
				heading = pathXMLNode.find('heading')
				pathDescription = pathXMLNode.find('pathDescription')
				pathBookingHallToPlatform = BNode()
				station_graph.add((bookingHallToPlatform, namespaces['path'], 
									pathBookingHallToPlatform))
				station_graph.add((pathBookingHallToPlatform,
								namespaces['heading'],Literal(heading.text)))
				station_graph.add((pathBookingHallToPlatform, 
				namespaces['pathdescription'],Literal(pathDescription.text)))

			if bookinghall.find('pointName'):
				for pointNameXMLNode in bookinghall.findall('pointName'):
					if pointNameXMLNode and pointNameXMLNode.text != '' :
						station_graph.add((bookingHallToPlatform,
						namespaces['pointname'],Literal(pointNameXMLNode.text)))
					if bookinghall.find('pathDescription'):
						for pathDescriptionXMLNode in bookinghall.findall('pathDescription'):
							station_graph.add((bookingHallToPlatform,
							namespaces['pathdescription'],
							Literal(pathDescriptionXMLNode.text)))

def station_entrance_platform_train(station_graph,entrance_object, entrance_node):
	if entrance_object:
		if entrance_object.findAll('platformtotrain'):
			for platform_train in entrance_object.findAll('platformtotrain'):
				platformToTrain = BNode()
				trainName = platform_train.find('trainname')
				platformToTrainSteps = platform_train.find('plaatformtotrainsteps')
				station_graph.add((entrance_node,namespaces['platform'], platformToTrain))
				station_graph.add((platformToTrain, namespaces['trainname'], 
								Literal(trainName.text)))
				if platformToTrainSteps:
					station_graph.add((platformToTrain, namespaces['platformtotrainsteps'], 
								Literal(platformToTrainSteps.text)))

def station_entrance(station_graph, station_node, entrances_object):
	if entrances_object:
		entrances_node = BNode()
		station_graph.add((station_node,namespaces['entrances'],entrances_node))
		for entrance in entrances_object.findAll('entrance'):
			entranceToBookingHall = entrance.find('entranceToBookingHall')
			entrance_node = BNode()
			entrance_name = entrance.find('name').text
			station_graph.add((entrances_node, namespaces['entrance'],
							   entrance_node))
			station_graph.add((entrance_node, namespaces['entrancename'],
									Literal(format_string(entrance_name))))
			station_graph.add((entrance_node, namespaces['entrancetobookhall'],
								Literal(format_string(entranceToBookingHall))))
			station_entrance_booking_hall(station_graph=station_graph,
										entrance_object=entrance,
										entrance_node=entrance_node)
			station_entrance_platform_train(station_graph=station_graph,
											entrance_object=entrance,
											entrance_node=entrance_node)

def station_placemarket(placemarket_iterator, station_graph, station_node):
	if placemarket_iterator:
		for placemarket in placemarket_iterator:
			placemark_node = BNode()
			station_graph.add((station_node, namespaces['placemark'], placemark_node ))
			station_graph.add((placemark_node, namespaces['placemarkname'],  
								Literal(placemarket.find('name').text) ))
			station_graph.add((placemark_node, namespaces['placemarkdescription'], 
							Literal(str(placemarket.find('description').find_all))))
			point = BNode()
			station_graph.add((placemark_node, namespaces['placemarkpoint'], point))
			station_graph.add((point, namespaces['placemarkcoordinates'],
						Literal(str(placemarket.find('point').find('coordinates').text))))
			station_graph.add((placemark_node,  namespaces['styleurl'], 
						Literal(format_string(placemarket.find('styleurl').text))))

def station_toilet(station_graph, station_node, toilet_iterator):
	if toilet_iterator:
		for toilet in toilet_iterator:
			location = toilet.find('location')
			public_toilet_node = BNode()
			station_graph.add((station_node, namespaces['Toilets'], public_toilet_node))
			if location and location.text != '':
				station_graph.add((public_toilet_node, namespaces['ToiletsLocation'],
				 Literal(location.text)))
			paymentRequired = toilet.find('paymentrequired')
			station_graph.add((public_toilet_node,namespaces['Toiletspaymentrequired'], 
			Literal(paymentRequired.text)))

def station_lines(station_graph, station_node, lines_iterator):
	if lines_iterator:
		lines_nodes = BNode()
		station_graph.add((station_node, namespaces['lines'], lines_nodes ))
		for line in lines_iterator:
			line_node = BNode()
			linename = line.find('linename')
			platform = line.find('platform')
			direction = line.find('direction')
			directionTowards = line.find('directiontowards')
			stepMin = line.find('stepmin')
			stepMax = line.find('stepmax')
			gapMin = line.find('gapmin')
			gapMax = line.find('gapmax')
			levelAccessByManualRamp = line.find('levelaccessbymanualramp')
			locationOfLevelAccess = line.find('locationoflevelaccess')

			line = BNode()
			station_graph.add((lines_nodes, namespaces['lines'], line_node))
			station_graph.add((line, namespaces['lineName'], 
								Literal(parse_xml_tag(linename))))
			station_graph.add((line, namespaces['platform'], 
								Literal(parse_xml_tag(platform))))
			station_graph.add((line, namespaces['direction'], 
								Literal(parse_xml_tag(direction))))
			station_graph.add((line, namespaces['directionTowards'],
							 Literal(parse_xml_tag(directionTowards))))
			station_graph.add((line, namespaces['stepMin'], 
								Literal(parse_xml_tag(stepMin))))
			station_graph.add((line, namespaces['stepMax'], 
								Literal(parse_xml_tag(stepMax))))
			station_graph.add((line, namespaces['gapMin'], 
								Literal(parse_xml_tag(gapMin))))
			station_graph.add((line, namespaces['gapMax'], 
								Literal(parse_xml_tag(gapMax))))
			if levelAccessByManualRamp and levelAccessByManualRamp.text != '':
				station_graph.add((line, namespaces['levelAccessByManualRamp'], 
				Literal(levelAccessByManualRamp.text)))
			if locationOfLevelAccess and locationOfLevelAccess.text != '':
				station_graph.add((line, namespaces['locationOfLevelAccess'], 
				Literal(locationOfLevelAccess.text)))
			

if __name__ == '__main__':

	xml = open('TFLfacilities.xml','r')
	bsobject = BeautifulSoup(xml,'lxml')
	all_stations_graph = Graph()
	all_stations_node = BNode()

	for station in bsobject.find_all('station'):
		station_node = BNode()
		station_name = format_string(station.find('name').get_text())
		station_id = station.attrs['id'] if 'id' in station.attrs else None
		station_type = station.attrs['type'] if 'type' in station.attrs else None
		all_stations_graph.add((all_stations_node,namespaces['station_namespace'],
									station_node))
		station_general_charateristics(station_graph=all_stations_graph,
										station_node=station_node,
											stationtype=station_type,
											stationname=station_name,
											stationid=station_id)
		contact_node = BNode()
		address = station.find('address').get_text
		phone = station.find('phone').get_text
		serviceline = station.findAll('linename')
		station_general_information(station_graph=all_stations_graph,
									station_node=station_node,contact_node=contact_node, 
									address=address,phone=phone,serviceline=serviceline)
		facilities_node = BNode()
		all_stations_graph.add(((station_node,namespaces['facilities'],facilities_node)))
		facilities_iterator = station.find('facilities').findAll('facility')
		station_facilities(station_graph=all_stations_graph, facilities_node=facilities_node,
						facility_iterator=facilities_iterator)
		zone = station.find('zones')
		station_zone(station_graph=all_stations_graph, station_node=station_node,
					zone_object=zone)
		entrances = station.find('entrances')
		station_entrance(station_graph=all_stations_graph,station_node=station_node,
						 entrances_object=entrances)
		placemark = station.findAll('placemark')
		station_placemarket(station_graph=all_stations_graph, station_node=station_node,
							placemarket_iterator=placemark)
		toilet = station.findAll('publictoilet')
		station_toilet(station_graph=all_stations_graph,station_node=station_node,
						toilet_iterator=toilet)
		lines = station.findAll('lines')
		station_lines(station_graph=all_stations_graph,station_node=station_node,
					 lines_iterator=lines)

register('text/rdf+n3', Parser, 'rdflib.plugins.parsers.notation3', 'N3Parser')
all_stations_graph.serialize(destination="ficherofinal.xml",format="xml")
all_stations_graph.serialize(destination="ficherofinal.rdf",format='n3')