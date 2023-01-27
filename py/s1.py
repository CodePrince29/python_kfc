#! /usr/bin/python

#Define un encabezado
#Define el cuerpo del reporte
#123456789012345678901234567890123456789012345678901234567890123456789012345678
#      xxxxxxxxxxxxxxxxxxxxxxxx NNNNNNNNNN NNNNNNNNNN
#        Ingresos Depositables     9719.60  120630.85 
import string

class Campo:
   tipos = ["string", "float", "integer" ]
   
   def __init__(self, t, s, l, o):
      self.tipo  = t
      self.start = s
      self.len   = l
      self.ord   = o


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
         tokens = string.split(s)
         for k in tokens:
            i = string.index(s, k, i)
            field = Campo(k, i, len(k), ++self.nCampos )
            i = i + len(k)
            self.campos.append( field )

   def leeDatos(self, file):
      f = open(file,'r')
      while 1 :
         s = f.readline()
         if len(s) <= 0: break
   def print(self)
      for x in self.campos:
         print x.tipo, x.start, x.len, x.ord

if __name__ == '__main__' :
   print "Voy a fields = Campos..."
   cmps = Campos()
   cmps.leeDefinicion('canx.def')
   cmps.print()

