#!/usr/bin/python
# -*- coding: utf-8 -*-

import xml.etree.ElementTree as ET
import urllib2
from jinja2 import Template,FileSystemLoader,Environment

class Incidence:
	carretera = ''
	fecha = ''
	km = ''
	sentido = ''
	nivel = ''
	def __init__(self,carretera,fecha,km,sentido,nivel):
		self.carretera = carretera
		self.fecha = fecha
		self.km = km
		self.sentido = sentido
		self.nivel = nivel

	def is_printable(self):
		if (self.nivel != 'T: Abierto C: Abierto A: Abierto' and self.nivel != None):
			return True
		else:
			return False

	def print_as_dictionary(self):
	  return {'carretera':carretera, 'fecha':fecha, 'km':km, 'sentido':sentido, 'nivel':nivel}


#tree = ET.parse('sample.xml')
tree = ET.parse(urllib2.urlopen('http://www.trafikoa.net/servicios/IncidenciasTDT/IncidenciasTrafikoTDTGeo'))
root = tree.getroot()
incidences = []
for child in root.findall('incidenciaGeolocalizada'):
  carretera = child.find('carretera').text
  fecha = child.find('fechahora_ini').text
  km = child.find('pk_inicial').text
  sentido = child.find('sentido').text
  nivel = child.find('nivel').text
  incidencia = Incidence(carretera, fecha, km, sentido, nivel)
  incidences.append(incidencia.print_as_dictionary())

templateLoader = FileSystemLoader( searchpath="templates" )
templateEnv = Environment( loader=templateLoader )
template = templateEnv.get_template( 'index.html' )

index = open('index.html', 'w')
index.write(template.render(incidencias=incidences).encode('utf-8'))  
index.close()
