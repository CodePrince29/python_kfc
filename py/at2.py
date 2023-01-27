#!/usr/bin/env python
#
# Programa para formatear las tablas html automaticamente
#
import string
import sys

TABLA="/home/httpd/cgi-bin/py/repmapa.txt"

f = open(TABLA,"r")
lineas = f.readlines()   
f.close()

i = 0
for l in lineas:
   v = map( string.strip, string.split(l,",") )
   if len(v) > 4:
      categoria    = v[0]
      nombre       = v[1]
      directorio   = v[2]
      periodicidad = v[3]
      prioridad    = v[4]
      programa     = v[5]
      if categoria == sys.argv[1]:
         if ( periodicidad == "W" ): periodicidad = "S"
         print '   reps[%2d]=new Rep("%s","%s","%s","%s","%s","%s");' % ( i, categoria, nombre, directorio, periodicidad, prioridad, programa )
         i = i + 1
print "   reps = new Array(%s);" % (i)
