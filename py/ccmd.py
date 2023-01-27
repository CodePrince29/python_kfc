#!/usr/bin/env python
#
# ccmd.py
#
import os
import mapa
import string
import exists
import myhtml
import cgiparms 

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

   def genera(self, fecha, year, periodo, semana):
      fecha = string.join( string.split( fecha, "-" ) , "") # quita guiones
      if  self.periodicidad == "D":
         os.system("%s 01 %s" % (self.prog, fecha))           # siempre pone 01
      elif self.periodicidad == "S":
         os.system("%s 01 %s %s %s" % (self.prog, year, periodo, semana))# siempre pone 01
      else :
         os.system("%s 01 %s %s" % (self.prog, year, semana)) # siempre pone 01
     
   def show(self):
      s = "%2s %-21s %-10s %1s %d %3s %s %s" % ( self.categoria , self.nombre,
         self.directorio, self.periodicidad,
         self.prio      , self.ambiente    ,
         self.prog      , self.parametros  )
      return s

   def toCSV(  self, path, fecha , csv_path, fmt_path ):
      datafile = path + self.directorio + '/' + fecha
      csvfile  = csv_path + self.directorio + '/' + fecha + ".csv"
      fmtfile  = fmt_path + self.directorio + ".fmt"
      ls_fmts = fmt.leer_fileFmt( fmtfile )
      datos = scan.scan_file( datafile, ls_fmts )
      scan.datos_tofile( csvfile, datos )
      return csvfile

   def excel( self, path, fecha ):
      fullname = path + self.directorio + '/' + fecha
      if exists.exists( fullname ):
         try: 
            csvfile = toCSV( self, path, fecha, 
                         "/home/httpd/home/rpts/",
                         "/home/httpd/cgi-bin/py/FORMATOS/" )
            f = open( csvfile )
            lines = f.readlines()
            f.close()


         except:
            print '<h2>Fallo en la genaracion de %s </h2>' % fullname
      else:
            print '<h2>No hay datos para %s </h2>' % fullname
            return

   def toHTML( self, path, fecha ):
      fullname = path + self.directorio + '/' + fecha
      if exists.exists( fullname ):
         try: 
            f = open( fullname )
            lines = f.readlines()
            f.close()
            myhtml.common_header( self.categoria, self.nombre )
            print "<pre>"
            for li in lines:
               print li[:-1]
            print "</pre>"
         except:
            print '<h2>Fallo en la genaracion de %s </h2>' % fullname
      else:
            print '<h2>No hay datos para %s </h2>' % fullname
            return

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

   def toExcel(self, fecha, year, periodo, semana, lista): 
      myhtml.header()
      for reporte in lista :
         if self.dict.has_key(reporte):
            fullname = self.path + reporte + '/' + fecha
            if not exists.exists( fullname ) or exists.newerThan(fullname, 7):
               self.dict[reporte].genera( fecha, year, periodo, semana) # generar el reporte
            self.dict[reporte].excel( self.path, fecha )
      myhtml.footer()

def main():
   ctgRpts = CReports()     # crea el catalogo de reportes
   k = cgiparms.CCGIparms()
   k.getCGIparms()
   if len( k.reports ):
      ctgRpts.toExcel( k.dia, k.year, k.periodo, k.semana, k.reports )

#if ( __name__ == "__main__" ) :
#   main()

##########################################
os.environ["PATH"]=os.environ["PATH"]+":/usr/bin/ph:/usr/fms/bin:/usr/fms/op/bin"
ctgRpts = CReports()
#k = cgiparms.CCGiparms()
#k.dia = "99-03-08"
#k.reports = [ "splan" ]
ctgRpts.toExcel( "99-03-09", "99", "04","01", [ "sales" ] )
##########################################

