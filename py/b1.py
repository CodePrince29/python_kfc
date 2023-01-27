# !/usr/bin/python
#Define un encabezado
#Define el cuerpo del reporte
#123456789012345678901234567890123456789012345678901234567890123456789012345678
#      xxxxxxxxxxxxxxxxxxxxxxxx NNNNNNNNNN NNNNNNNNNN
#        Ingresos Depositables     9719.60  120630.85 
import string

def main():
   print "Content-type: text/html\n"
   print """<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2//EN">
<HTML>

<!-- This file generated using Python -->
<HEAD>
  <META NAME="GENERATOR" CONTENT="HTMLgen 2.2.2">
        <TITLE>Hello, Word!</TITLE>
</HEAD>"""
   print "<BODY>Hello, Word!</BODY></HTML>"

if ( __name__ == "__main__" ) :
   main()

"""
class Campo:
   tipos = ["string", "float", "integer" ]
   
   def __init__(self, t, s, l, o):
      self.tipo  = t
      self.start = s
      self.len   = l
      self.ord   = o

if __name__ == '__main__' :
   print "Hola"
#c1 = Campo("xxxxxx", 2, 15, 1)
#print c1

class Campos:
   def __init__(self):
      self.campos = []   # la lista de campos es vacia inicialmente
      self.nCampos = 0   # inicializa en 0 el numero de campos

   def leeDefinicion(self, file):
      # Lee la definicion de los campos
      f = open(file,'r')
      i = 0
      while 1 :
         s = f.readline()
         if len(s) <= 0: break
         tokens = split(s)
         for k in tokens:
            i = index(s, k, i)
            field = new Campo(k, i, len(k), ++self.nCampos )
            i += len(k)
            campos.addItem( field )
      print campos

   def leeDatos(self, file):
      f = open(file,'r')
      while 1 :
         s = f.readline()
         if len(s) <= 0: break

print "Voy a fields = new Campos..."
print "1 Voy a fields = new Campos..."
print "2 Voy a fields = new Campos..."
print "3 Voy a fields = new Campos..."
#fields = new Campos
print fields
print "Voyn a lee_definicion.."
#fields.leeDefinicion("canx.def")
print "Termine lee_definicion.."
print "Regrese ......."

"""
