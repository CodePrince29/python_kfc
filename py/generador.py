#!/usr/bin/env python
#
# generador.py
#
import os
import mapa
import string
import exists
import myhtml

class CReport:
   def __init__(self, categoria, nombre, directorio, 
            periodicidad = "D", 
            prio         = 0, 
            prog         = "", 
            ambiente     = "SUS",
            parametros   = "" ):
     self.categoria    = categoria
     self.nombre       = nombre
     self.directorio   = directorio      # este es llave unica
     self.periodicidad = periodicidad
     self.prio         = int(prio)
     self.ambiente     = ambiente
     self.prog         = prog
     self.parametros   = parametros

   def genera(self, fecha):
     fecha = string.join( string.split( fecha, "-" ) , "")
     os.system("%s %s" % (self.prog, fecha))
     
   def show(self):
     s = "%2s %-21s %-10s %1s %d %3s %s %s" % ( self.categoria , self.nombre,
         self.directorio, self.periodicidad,
         self.prio      , self.ambiente    ,
         self.prog      , self.parametros  )
     return s

   def toHTML( self, path, fecha ):
      fullname = path + self.directorio + '/' + fecha
      if exists.exists( fullname ):
         try: 
            f = open(newname)
            lines = f.readlines()
            f.close()
            myhtml.common_header( self.categoria, self.nombre )
            print "<pre>"
            for li in lines:
               print li[:-1]
            print "</pre>"
         except:
            print '<h2>No hay datos para %s </h2>' % fullname

    
class CReports:
   def __init__(self, mapatxt="repmapa.txt", path="/usr/fms/op/rpts/"):
     self.mapa = mapa.getMapa(mapatxt)
     self.dict = {}
     for m in self.mapa:
        r = CReport(m[0],m[1],m[2],m[3],m[4],m[5])
        self.dict[ r.directorio ] = r
     self.path = path

   def show(self):
     for r in self.dict.values():
        print r.show()

   def genera(self, report, fecha ):
     if self.dict.has_key(report):
        self.dict[report].genera(fecha)

   def toHTML(self, fecha, lista): 
      myhtml.header()
      for li in lista :
         if self.dict.has_key(li):
            self.dict[li].toHTML(self.path, fecha )
      myhtml.footer()


def main():
   ctgRpts = CReports()     # crea el catalogo de reportes
   k = CCGIparms()
   k.getCGIparms()
   if len( k.reports ):
      # ctgRpts.genera("splan", "99-03-06")
      ctgRpts.toHTML( k.dia, k.reports  )

if ( __name__ == "__main__" ) :
   main()
            
