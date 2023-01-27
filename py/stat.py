#!/usr/bin/env python
import re
import string

def str2dict( s ):
   """ La string s tiene la forma a:-n, c:-m, d:-o,.. """
   dict = {}
   vvv = string.split(s, "," )
   for vv in vvv:
      v = map( string.strip, string.split( vv,":") )
   dict[v[0]] = v[1]
   return dict

class DefDatos:
   def __init__(self, limites = ["",""], patron = { "*":-1 } ):
       self.dentro = 0
       self.limites = limites
       self.patron = patron
       self.values = {}

   def getValues(self, lineas):
      for li in lineas:
         if re.compile(self.limites[0]).search(li): self.dentro = 1
         if self.dentro:
            for k in self.patron.keys():
                if re.compile(k).search(li):
                   self.values[k] = re.split(" +",li)[self.patron[k]]
         if re.compile(self.limites[1]).search(li): self.dentro = 0

   def showValues(self):
      for i in self.values.keys():
         print i, repr( self.values[i] )

class DefGraf:
   def __init__(self, num, titulo, tpo="3DBAR",
                etiquetas=[], 
                datos1="", 
                datos2="" ):
      self.num = num
      self.titulo = titulo
      self.tpo = tpo
      self.etiquetas = etiquetas
      self.datos1 = datos1
      self.datos2 = datos2

   def show(self):
      print self.num, self.titulo, self.tpo,
      print self.etiquetas,

class CDefGrafs:
   def __init__(self):
      self.grafs = []

   def loadDefiniciones(self, filename ):
      try:
         f = open(filename)
         lines = f.readlines()
         for li in lines:
            print li[:-1]
         f.close()
      except:
         print "No existe el archivo de definiciones %s\n" % filename
         return
      # paso 2. crea las definiciones para las graficas 
      try:
         print "paso 2. crea las definiciones para las graficas "
         flg_new = 0
         flg_old = 1
         for li in lines:
            if re.compila("GRAF=").match(li):
               if flg_old < flg_new:
                  x = DefGraf(num, titulo, tpo, etiquetas, datos1, datos2)
                  self.grafs.append(x)
                  datos1 = {}
                  datos2 = {}
                  flg_old = flg_new 
            if re.compila("DATOS=").match(li):         datos=li[6:]
            if re.compila("ETIQUETAS=").match(li): etiquetas=li[10:]
            if re.compila("GRAF=").match(li):            
               num=li[5:]
               flg_new = flg_new + 1
            if re.compila("TITULO=").match(li):       titulo=li[7:]
            if re.compila("TPO=").match(li):             tpo=li[4:]
            if re.compila("LIMITES=").match(li):     
               limites= string.split(li[8:], ",")
            if re.compila("DATOS1=").match(li): 
               dict1 = str2dict( li[7:] )
               if len(dict1): 
                  datos1 = DefDatos( limites, dict1 )
            if re.compila("DATOS2=").match(li): 
               dict2 = str2dict( li[7:] )
               if len(dict2): 
                  datos2 = DefDatos( limites, dict2 )
            
            #self.grafs.append( c1 )
         else:
            x = DefGraf(num, titulo, tpo, etiquetas, datos1, datos2)
            self.grafs.append(x)
      except:
         pass

#gr = DefGraf(2, "Title", "3DBAR", ["Label1","Label2"] )
#gr.show()

grafs = CDefGrafs()
grafs.loadDefiniciones("FORMATOS/stat.grf")
print "3. CDefGrafs....for g in ... "
print repr(len(grafs.grafs))
for g in grafs.grafs:
   g.show()


#d = DefDatos( ["TOTAL:", "PEDIDOS"],
#    {"Comedor": -3, "Entrega": -3, "Llevar": -3, "Otros": -3 } )
#d.getValues(lineas)
#d.show()
