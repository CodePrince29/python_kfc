#!/usr/bin/env python
# muestra la fecha equivalente al periodo pasado
import phdates
import sys

v = map( int , sys.argv[1:] )
if len(v) == 3:
   fechas = phdates.yps( v[0], v[1], v[2] )
   print phdates.y_m_d(fechas[1])
