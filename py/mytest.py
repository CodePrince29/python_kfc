#!/usr/bin/env python
#
# reportes.py
#
from CReport import CReports
import cgiparms 

#def main():
#   ctgRpts = CReports()     # crea el catalogo de reportes
#   k = cgiparms.CCGIparms()
#   k.getCGIparms()
#   if len( k.reports ):
#      ctgRpts.toHTML(k) 
#
#if ( __name__ == "__main__" ) :
#   main()

# para probar el shell desde la linea de comando debe de quitar los 
# comentarios de las lineas de abajo y poner comentarios a las lineas
# de arriba. 
cr = CReports()
k = cgiparms.CCGIparms()
k.dia     = "00-07-27"
k.semana  = "N"
k.periodo = "N"
#k.year    = "N"
k.nav     = "Microsoft Internet Explorer"
k.ver     = ""
k.cbTipo  = "Text"
k.reports = [ "cash" ]
cr.toHTML(k) 

