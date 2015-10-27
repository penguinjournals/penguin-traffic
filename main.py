#!/usr/bin/python
# -*- coding: utf-8 -*-

import xml.etree.ElementTree as ET
import urllib2
import ConfigParser
from datetime import datetime, timedelta
from jinja2 import Template,FileSystemLoader,Environment
from boto.s3.connection import S3Connection
from boto.s3.key import Key

class Incidence:
    carretera = ''
    fecha = ''
    km = ''
    sentido = ''
    nivel = ''
    def __init__(self,carretera,fecha,km,sentido,nivel,poblacion):
        self.carretera = carretera
        self.fecha = fecha
        self.km = km
        self.sentido = sentido
        self.nivel = nivel
        self.poblacion = poblacion

    def is_printable(self):
        return self.nivel != 'T: Abierto C: Abierto A: Abierto' and self.nivel != None

    def print_as_dictionary(self):
      return {'carretera':carretera, 'fecha':fecha, 'km':km, 'sentido':sentido, 'nivel':nivel, 'poblacion':poblacion}

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
  poblacion = child.find('poblacion').text
  incidencia = Incidence(carretera, fecha, km, sentido, nivel, poblacion)
  if incidencia.is_printable():
    incidences.append(incidencia.print_as_dictionary())

fecha = datetime.now()+ timedelta(hours=1)
#fecha = fecha.strftime('%m/%d/%Y')

templateLoader = FileSystemLoader( searchpath="templates" )
templateEnv = Environment( loader=templateLoader )
template = templateEnv.get_template( 'index.html' )

index = open('index.html', 'w')
index.write(template.render(incidencias=incidences, fecha=fecha).encode('utf-8'))  
index.close()

#UPLOAD TO S3
config = ConfigParser.ConfigParser()
config.read("config.ini")
AWS_ACCESS_KEY_ID=config.get("aws", "aws_access_key_id")
AWS_SECRET_ACCESS_KEY=config.get("aws","aws_secret_access_key")

conn = S3Connection(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
bucket = conn.get_bucket('traffic.penguinjournals.com')
key = Key(bucket)
key.key = 'index.html'
key.set_contents_from_filename('index.html')
