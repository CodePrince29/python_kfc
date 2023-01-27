#!/usr/bin/env python
#
# CReport.py
#
import re
import os
import mapa
import string
import exists
import myhtml
import cgiparms 
#import chart
import fmt
import scan
from socket import *

# define global variables
HOST = 'localhost'
PORT = 4000
DIR_FORMATOS="/home/httpd/cgi-bin/py/FORMATOS/"
DIR_CSV     ="/home/httpd/html/rpts/"
REL_CSV     ="http://localhost/rpts/"
DIR_DATOS   ="/usr/fms/op/rpts/"
TO_POSTSCRIPT = "/usr/bin/pstext"


class CReport:
   def __init__(self, categoria, nombre, directorio, 
            periodicidad = "D", 
            prio         = 0, 
            prog         = "", 
            anchura      = "80",
            parametros   = "" ,
            ambiente     = "SUS"):
      self.categoria    = categoria
      self.nombre       = nombre
      self.directorio   = directorio      # este es llave unica
      self.periodicidad = periodicidad
      self.prio         = int(prio)
      self.ambiente     = ambiente
      self.prog         = prog
      self.anchura      = anchura
      self.parametros   = parametros

   def filename(self, fecha): 
      return DIR_DATOS + self.directorio + "/" + fecha
   def csv_filename(self, fecha): 
      return DIR_CSV + self.directorio + '/' + fecha + ".csv"
   def fmt_filename(self): 
      return  DIR_FORMATOS + self.directorio + ".fmt"
   def csvrel(self, fecha):
      return REL_CSV + self.directorio + '/' + fecha + ".csv"
   #
   # Se realiza la ejecuccion del programa generador del reporte
   #
   def genera(self, fecha, year, periodo, semana):
      fecha = string.join( string.split( fecha, "-" ) , "") # quita guiones
      if len(self.prog) <= 0: return
      if   self.periodicidad == "D":
         os.system("%s 01 %s" % (self.prog, fecha))         # siempre pone 01
      elif self.periodicidad == "S":
         os.system("%s 01 %s %s %s" % (self.prog, year, periodo, semana))
      else:
         os.system("%s 01 %s %s" % (self.prog, year, periodo))
     
   #
   # Muestar el contenido de cada definicion de reporte
   #
   def show(self):
      s = "%2s %-21s %-10s %1s %d %3s %s %s" % ( self.categoria , self.nombre,
         self.directorio, self.periodicidad,
         self.prio      , self.ambiente    ,
         self.prog      , self.parametros  )
      return s


   #
   # Convierte el reporte de txt a csv
   #
   def toCSV(  self, fecha ):
      csv_datos = []  
      
      #
      # En caso de que exista el archivo csv lo lee.
      #
      if exists.exists( self.csv_filename(fecha) ) :
            f = open( self.filename(fecha) )
            csv_datos = f.readlines()
            f.close()
      else:
         if exists.exists( self.filename(fecha) ):
            try: 
               # lee formatos ls_fmts
               # escanea archivo y deja el contenido en datos
               # datos -> csvfile
               #
               ls_fmts   = fmt.leer_fileFmt( self.fmt_filename() )  
               csv_datos = scan.scan_file( self.filename( fecha ), ls_fmts ) 
               scan.datos_tofile( self.csv_filename(fecha) , csv_datos )
            except:
               csv_datos = []  
      return csv_datos

   def ExceltoExplorer( self, fecha ):
      csv_datos = self.toCSV( fecha )
      if len(csv_datos):
         print '''<h2>Presione <a href="%s">aqu&iacute;</a>
               para ver los datos</h2>''' % self.csvrel(fecha)
      else:
         print '''<h2>Excel2Explorer:No hay datos o no esta definida esta
               operacion para %s </h2>''' % self.filename(fecha)

   def ExceltoNavigator( self, fecha ):
      csv_datos = self.toCSV( fecha )
      if len(csv_datos):
         print '<h4>Abriendo StarOffice para %s</h4>' % csv_filename(fecha)
         h = os.fork()
         if ( h == 0 ):
            s = socket(AF_INET, SOCK_STREAM)
            s.connect(HOST, PORT)
            s.send('soffice ' + csv_filename(fecha) )
            data = s.recv(1024)
            s.close()
            os._exit(0)
      else:
         print '''<h2>Excel2Navigator:No hay datos o no esta definida esta
               operacion para %s </h2>''' % self.filename(fecha)
    
   def armaHojaConGraficas( self, fecha ):
      csv_datos = self.toCSV( fecha )
      if len(csv_datos):
         cc = chart.CCharts()
         cc.loadDefiniciones( DIR_FORMATOS + self.directorio + ".grf" )
         cc.getLabels( self, csv_datos )
         cc.getDatos(self,  csv_datos )
         for k in cc.grafs:
            cc.generaGifs()
      else:
         print '''<h2>No hay datos o no esta definida esta
               operacion para %s </h2>''' % self.filename(fecha)
    
   def toPrint( self, fecha):
      ''' Imprime un reporte pasandolo primero x filtro postscript '''
      if exists.exists( self.filename(fecha) ):
         try: 
            if self.anchura == "80" :
               sCmd = "%s -s 10 -yt 40 -yb 40 -xl 25 -xr 25 %s | lpr"
               os.system(sCmd % (TO_POSTSCRIPT,  self.filename(fecha)))
            elif self.anchura == "132" :
               sCmd = "%s -s 6 -yt 40 -yb 40 -xl 25 -xr 25 %s | lpr"
               os.system(sCmd % (TO_POSTSCRIPT, self.filename(fecha)))
            else:
               sCmd = "%s -l -s 6 -yt 40 -yb 40 -xl 25 -xr 25 %s | lpr"
               os.system(sCmd % (TO_POSTSCRIPT, self.filename(fecha)))
            print '<h2>Reporte %s enviado a impresora</h2>' % self.filename(fecha)
         except:
            print '<h2>Fallo generacion de %s </h2>' % self.filename(fecha)
      else:
            print '<h2>No hay datos para %s </h2>' % self.filename(fecha)
            return

   def toHTML( self, fecha ):
      if exists.exists( self.filename(fecha) ):
         try: 
            f = open( self.filename(fecha) )
            lines = f.readlines()
            f.close()
            myhtml.common_header( self.categoria, self.nombre )
            print "<pre>"
            for li in lines:
               li = re.sub('[^ -~]', '', li)
               print li
               #print li[:-1]
            print "</pre>"
         except:
            print '<h2>Fallo generacion de %s </h2>' % self.filename(fecha)
      else:
            print '<h2>No hay datos para %s </h2>' % self.filename(fecha)
            return


class CReports:
   def __init__(self, mapatxt="repmapa.txt", path="/usr/fms/op/rpts/"):
      self.mapa = mapa.getMapa(mapatxt)
      self.dict = {}
      for m in self.mapa:
         r = CReport(m[0],m[1],m[2],m[3],m[4],m[5], m[6])
         self.dict[ r.directorio ] = r
      self.path = path

   def show(self):
      for r in self.dict.values():
         print r.show()

   def toExcel(self, fecha, year, periodo, semana, lista): 
      myhtml.header()
      for reporte in lista :
         if self.dict.has_key(reporte):
            r = self.dict[reporte]
            fullname = r.filename(fecha)
            if not exists.exists( fullname ) or exists.newerThan(fullname, 7):
               r.genera( fecha, year, periodo, semana) # generar el reporte
            r.excel( self.path, fecha )
      myhtml.footer()

   def toHTML(self, k): 
      myhtml.header()
      for reporte in k.reports :
         if self.dict.has_key(reporte):
            r = self.dict[reporte]
            fullname = r.filename( k.dia )
            if not exists.exists( fullname ) or exists.newerThan(fullname, 7):
               r.genera( k.dia, k.year, k.periodo, k.semana) 
            if k.cbTipo == "Text" : r.toHTML( k.dia )
            if k.cbTipo == "Print": r.toPrint( k.dia )
            if k.cbTipo == "Graf" : r.armaHojaConGraficas( k.dia )
            if k.cbTipo == "Excel":
               if k.nav == "Netscape":
                  r.ExceltoNavigator( k.dia )
               else:
                  r.ExceltoExplorer( k.dia )
      myhtml.footer()


#def main():
#   ctgRpts = CReports()     # crea el catalogo de reportes
#   k = cgiparms.CCGIparms()
#   k.getCGIparms()
#   if len( k.reports ):
#      ctgRpts.toHTML(k) 
#
#if ( __name__ == "__main__" ) :
#   main()

#cr = CReports()
#k = cgiparms.CCGIparms()
#k.dia     = "99-03-09"
#k.semana  = "N"
#k.periodo = "N"
#k.year    = "N"
#k.nav     = "Explorer"
#k.ver     = ""
#k.cbTipo  = "Excel"
#k.reports = [ "remp" ]
#cr.toHTML(k) 

