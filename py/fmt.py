#!/usr/bin/env python
#
# Programa para cargar los formatos a partir de un archivo de formatos
# Uso: fmts = leer_fileFmt( "fmt.txt" ):
#
# Formatos validos: xxxx XXXX Xxxxxx  campos alfanumericos
#                   nnnn NNNN Nnnnnn  campos numericos
#
import sys
import re
import string

TIPO_NUMERICO     = "N"    # campo obligado no puede ser blanco
TIPO_ALFANUMERICO = "X"    # campo obligado no puede ser blanco
TIPO_NUMERICO     = "n"    # campo opcional    puede ser blanco
TIPO_ALFANUMERICO = "x"    # campo opcional    puede ser blanco

class DefCampo:

   def __init__(self, ini,fin, tipo = "X" ):
      self.ini = ini
      self.fin = fin
      self.tipo = tipo

   def getTipo(self):
      return self.tipo[0:1]

   def show(self):
      return ( self.ini, self.fin, self.tipo )

class DefCampos:
   def __init__(self):
      self.campos = []

   def add(self, i, f, campo ):
      self.campos.append( DefCampo( i, f, campo ) )

   def show(self):
      for k in self.campos:
         print k.show()
   

def scan_fmt_line( linea ):
   """ examina una linea y regresa la definicion de esta en base a campos """
   campos = DefCampos()
   i = 0
   j = len(linea) - 1
   v = re.split("  *", string.strip(linea))
   for e in v:
      n = string.find(linea, e, i, j)
      if 0 <= n:
         k = n + len(e) - 1
         campos.add( n, k, e ) 
         i = n + len(e) 
   return campos
     
def leer_file( filename ):
   try:
      f = open( filename )
      lineas = f.readlines()
      f.close()
   except:
      lineas = []
   return lineas
 

def leer_fileFmt( fmtFileName ):
   lineas = leer_file( fmtFileName )

   formatos = []
   for l in lineas:
      if len(l):
         campos = scan_fmt_line(l)
         formatos.append( campos )
   #for j in formatos:
   #    j.show()
   return formatos


#fmts = leer_fileFmt("/home/httpd/cgi-bin/py/FORMATOS/remp.fmt")
#for j in fmts:
#    j.show()
#
