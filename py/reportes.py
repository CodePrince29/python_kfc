#!/usr/bin/env python
#
# reportes.py
#
from CReport import CReports
import cgiparms 

def main():
   ctgRpts = CReports()     # crea el catalogo de reportes
   k = cgiparms.CCGIparms()
   k.getCGIparms()
   if len( k.reports ):
      ctgRpts.toHTML(k) 

if ( __name__ == "__main__" ) :
   main()

# para probar el shell desde la linea de comando debe de quitar los 
# comentarios de las lineas de abajo y poner comentarios a las lineas
# de arriba. 
#cr = CReports()
#k = cgiparms.CCGIparms()
#k.dia     = "01-06-04"
#k.semana  = "02"
#k.periodo = "07"
#k.year    = "01"
#k.nav     = "Microsoft Internet Explorer"
#k.ver     = ""
#k.cbTipo  = "Print"
#k.reports = [ "sales" ]
#cr.toHTML(k) 

