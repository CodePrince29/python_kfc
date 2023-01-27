#!/usr/bin/env python
#
# mapa.py
#
import string

tabla="/home/httpd/cgi-bin/py/repmapa.txt"

def getMapa(mapafile=tabla):
   f = open(mapafile)
   lineas = f.readlines()
   f.close
   mapa = []
   for k in lineas:
      if len(k) > 10 and k[0] != "#" :
         mapa.append( map(string.strip, string.split(k,",") ) )
   return mapa
         
#mymap = getMapa("repmapa.txt")
#for j in mymap:
#   print j
