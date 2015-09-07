import xml.etree.ElementTree as ET
import urllib2
#response = urllib2.urlopen('http://www.trafikoa.net/servicios/IncidenciasTDT/IncidenciasTrafikoTDTGeo')
#xml = response.read()
#tree = ET.parse(xml)
tree = ET.parse('sample.xml')
root = tree.getroot()
for child in root.findall('incidenciaGeolocalizada'):
    print child.find('carretera').text