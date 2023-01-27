#!/usr/bin/env python
#
# Programa para escanear datos, 
# Uso: scan.py fmt archivo.txt
#
import fmt
import sys
import re
import string

def divide_line( linea, formato ):
   flg_ok = 1 
   valores = []
   r = re.compile(" *[+-]*[0-9/]*\.[0-9]*$| *[+-]*[0-9/]+$")
   for k in formato.campos :
      token = linea[k.ini: k.fin+1]
      if len(token) == 0:    # ..... VALIDA QUE EL TOKEN NO SEA NULO ...
         if ( k.getTipo() == "X" or k.getTipo() == "N" ):
            flg_ok = 0
            #valores = [ linea ]
            valores = []
            break
      else:                  # ...... VALIDA QUE SEA UN NUMERO ........
         if k.getTipo() == "N" or k.getTipo == "n":
            if not r.match(token):
               flg_ok = 0
               #valores = [ linea ]
               valores = []
               break
      valores.append( token )

   return valores
   

def scan_line( linea, fmts ):
   """ examina una linea y regresa una lista con sus valores  """
   for i_fmt in fmts:
      listval = divide_line( linea[:-1], i_fmt )
      if len( listval ): 
         break
   if len( linea ) and len( listval ) == 0:
      listval = [ linea[:-1] ]
   return listval
    
def datos_dotabla( datos ):
   r = re.compile("[A-z]+")
   for d in datos:
      for i in range(0, len(d) ):
         if r.search(d[i]):
            print '"%s"' % d[i],
         else:
            print '%s' % d[i],
         if i < len(d) - 1: print ",",
      print 

def datos_tofile( filename,  datos ):
   f = open(filename,"w")
   r = re.compile("[A-z]+")
   for d in datos:
      for i in range(0, len(d) ):
         if r.search(d[i]):
            f.write('"%s"' % d[i])
         else:
            f.write( '%s' % d[i])
         if i < len(d) - 1: f.write(",")
      f.write("\n")
   f.close
   



def scan_file( filename, fmts ):
   texto = fmt.leer_file( filename )
   
   datos = []
   for l in texto:
      if len(l):
         valores = scan_line(l, fmts )
         if len(valores):
            datos.append( valores )
   return datos

#if len(sys.argv) < 2:
#   print """
#   Uso: scan.py fmt archivo.txt
#"""
#else:
#   #
#   # Leer el archivo de formatos
#   #
#   fmts = fmt.leer_fileFmt(sys.argv[1])
#   if len(sys.argv) >= 3:
#      datos = scan_file( sys.argv[2], fmts )
#      datos_dotabla( datos )
#      datos_tofile("cosa", datos)
