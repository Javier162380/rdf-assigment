from rdflib import Graph, Literal, URIRef,BNode
from bs4 import BeautifulSoup
from rdflib.namespace import FOAF,RDF
from rdflib.plugin import register, Parser

def format_string(string):
    try:
        return string.replace('\n','').replace(' ','')
    except:
        return None

def get_text(string):
    try:
        return string.get_text()
    except:
        return None


rdf = Graph()
xml = open('TFLfacilities.xml','r')
bsobject = BeautifulSoup(xml,'lxml')
namespaceline = URIRef('http://tfl.gov.uk/serviceline')
namespacezone = URIRef('http://tfl.gov.uk/zone')
contactdetails = URIRef('http://tfl.gov.uk/contactdetails')
facilities = URIRef('http://tfl.gov.uk/facilities')
naptans = URIRef('http://tfl.gov.uk/naptans')
lines = URIRef('http://tfl.gov.uk/lines')

for i in bsobject.find_all('station'):

    station_name = i.find('name').get_text()
    rdf.add((URIRef("https://tfl.gov.uk/tfl#" + format_string(station_name) + '.html'),
             FOAF['station_name'], Literal(format_string(station_name))))
    Lines = set()
    for i in i.find_all('linename'):
        Line = i.get_text()
        Lines.add(Line)
    Lines_Literal = ','.join(i for i in Lines)
    rdf.add((URIRef("https://tfl.gov.uk/tfl#"+format_string(station_name)+'.html'),
            namespaceline, Literal(format_string(Lines_Literal))))
    zone = i.find('zone')
    rdf.add((URIRef("https://tfl.gov.uk/tfl#" +format_string(station_name)+ '.html'),
             namespacezone, Literal(format_string(zone))))
    address_phone = BNode()
    address = format_string(get_text(i.find('address')))
    phone = format_string(get_text(i.find('phone')))
    rdf.add((URIRef("https://tfl.gov.uk/tfl#" + format_string(station_name) + '.html'),
             contactdetails, address_phone))
    rdf.add((address_phone,RDF.type,RDF.Seq))
    rdf.add((address_phone,FOAF['address'], Literal(address)))
    rdf.add((address_phone, FOAF['phone'], Literal(phone)))
    try:
        facilities_node = BNode()
        facilities_results = {i['name']: format_string(i.get_text()) for i in i.find_all('facility')}
        rdf.add((URIRef("https://tfl.gov.uk/tfl#" + format_string(station_name) + '.html'),
                 facilities, facilities_node))
        rdf.add((facilities_node,RDF.type,RDF.Bag))
        for i in facilities_results.keys():
            rdf.add((facilities_node,FOAF[str(i).replace(' ','_')], Literal(format_string(facilities_results[i]))))
    except:
        pass
    try:
        naptan_node = BNode()
        naptanid_results = [format_string(i.get_text()) for i in i.find_all('naptanid')]
        descriptions_results = [format_string(i.get_text()) for i in i.find_all('description')]
        rdf.add((URIRef("https://tfl.gov.uk/tfl#" + format_string(station_name) + '.html'),
                 naptans, naptan_node))
        rdf.add((naptan_node, RDF.type, RDF.Seq))
        for naptanid,description in zip(naptanid_results,descriptions_results):
            rdf.add((naptan_node,FOAF['naptan_id'], Literal((naptanid))))
            rdf.add((naptan_node, FOAF['description'], Literal((description))))

    except:
        pass
    


register('text/rdf+n3', Parser, 'rdflib.plugins.parsers.notation3', 'N3Parser')
rdf.serialize(destination="ficherofinal.xml",format="xml")
rdf.serialize(destination="ficherofinal.rdf",format='n3')