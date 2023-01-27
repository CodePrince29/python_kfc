#! /usr/bin/env python
# busque el modulo gdchart en :   http://www.boutell.com/gd
# Autor: Miguel A. Zavaleta
#
import string
import gdchart
import re
import unique

# Todos los gifs se pondran en este directorio
TMPDIR="/tmp"

colors = { "blanco":0xffffff,   "verde":0x80ff80,   "azul":0x80ffff,
           "morado":0x8080ff,   "magenta":0xff80ff, "rosa":0xff8080,
           "amarillo":0xffff80, "rojo":0xff3030 }
gif_tps = { "BAR":gdchart.GDC_BAR, "AREA":gdchart.GDC_AREA, "3DBAR":gdchart.GDC_3DBAR, "2DPIE":gdchart.GDC_2DPIE, "3DPIE":gdchart.GDC_3DPIE }

class Chart:
   def __init__(self, gifname        , 
      titulo, xtitulo, ytitulo       ,
      labels, datos1, datos2 = ()    ,
      tipo         = gif_tps["3DBAR"], 
      size         = (200, 200)      ,
      colores      = (colors["rojo"] , colors["blanco"], colors["morado"]),
      bg_color     = 0x202060        ,
      plot_color   = 0xC0C0C0        ,
      line_color   = colors["blanco"],
      xtitle_color = colors["blanco"],
      ytitle_color = colors["blanco"]  ):

      self.tipo    = tipo
      self.title   = titulo
      self.xtitle  = xtitulo
      self.ytitle  = ytitulo
      self.labels  = labels
      self.datos1  = datos1
      self.datos2  = datos2
      self.colores = colores
      self.size    = size
      self.gifname = gifname  
      self.bg_color     = bg_color
      self.plot_color   = plot_color
      self.line_color   = line_color
      self.xtitle_color = xtitle_color
      self.ytitle_color = ytitle_color
      self.opt          = gdchart.option
      
   def setGifName(self, gifname): self.gifname = gifname
   def setColors(self, colores ): self.colores = colores
   def setDatos1(self, datos )  : self.datos1  = datos
   def setDatos2(self, datos )  : self.datos2  = datos
   def setLabels(self, labels ) : self.labels  = labels
   def getGifName(self)         : return self.gifname
   def fullName(self)           : return TMPDIR + self.gifname

   def setOpciones(self):
      self.opt(title = self.title, xtitle = self.xtitle, ytitle = self.ytitle)
      self.opt(set_color = self.colores)
      self.opt(bg_color  = self.bg_color, plot_color=self.plot_color)
      self.opt(line_color = self.line_color)
      self.opt(xtitle_color=self.xtitle_color, ytitle_color=self.ytitle_color)
      self.opt(bg_transparent=0, border=1, 
               edge_color=0xA0A0A0, thumblabel="thumb label")

   def gif_datos1(self):   # gif con el primer grupo de datos
      self.setOpciones()
      gdchart.chart(self.tipo,self.size,self.fullName(),self.labels,self.datos1)

   def gif_datos2(self):   # gif con el segundo grupo de datos
      self.setOpciones()
      gdchart.chart(self.tipo,self.size,self.fullName(),self.labels,self.datos2)

   def gif_datos_1y2(self): # gif con el primer y segundo grupo de datos
      self.setOpciones()
      gdchart.chart(self.tipo, self.size, self.fullName(),
                    self.labels, self.datos1, self.datos2 )
   def gif_datos_2y1(self): # gif con el segundo y primer grupo de datos
      self.setOpciones()
      gdchart.chart(self.tipo, self.size, self.fullName(),
                    self.labels, self.datos2, self.datos1 )


class CChart:
   def __init__( self,
                 grf_tpo=  1 , 
                 titulo = "NADA" , 
                 p1     = "" , 
                 p2     = "" , 
                 xtit   = "" , 
                 ytit   = "" , 
                 xsz    = 200 , 
                 ysz    = 200 ):
      """ 
      Vea como este objeto mapea perfectamente con el archivo de definiciones
      para la grafica final se mapea este objeto a objetos Chart.
      """
      self.grf_tpo       = grf_tpo    
      self.titulo        = titulo    
      self.patternDatos1 = p1         
      self.patternDatos2 = p2         
      self.xtitulo       = xtit       
      self.ytitulo       = ytit       
      self.size          = ()
      self.size          = ( xsz , ysz )  
      self.gif_tpo       = gif_tps["3DBAR"]
      self.d1            = []
      self.d2            = []
      #print self.titulo, self.patternDatos1, self.patternDatos2


class CCharts:
   def __init__( self ):
      self.grafs         = []
      self.patternLabels = ""
      self.patternData   = ""
      self.labels        = []

   def loadDefiniciones(self, filename ):
      try:
         f = open(filename)
         lines = f.readlines()
         f.close()
      except:
         print "No existe el archivo de definiciones %s\n" % filename
         return
      # paso 2. crea las definiciones para las graficas 
      try:
         for li in lines:
            #print li
            v = map( string.strip, string.split( li , "," ))
            #print v
            if len(v) == 2 :
               self.patternLabels = v[0]
               self.patternData   = v[1]
            else:
               c1 = CChart(int(v[0]),v[1],v[2],v[3],v[4],v[5], int(v[6]),int(v[7]))
               self.grafs.append( c1 )
      except:
          pass

   def getLabels(self, datos):
      for d in datos:
         if re.compile(self.patternLabels).search(d[0]):
            self.labels = datos[1:]
            break

   def getDatos(self, datos):
      for d in datos:
         for c in self.grafs:
            if re.compile(c.patternDatos1).search(d[0]):
               c.d1 = map( self.patternData, d[1:] )
               if len(c.patternDatos2) <= 0: break
            if len(c.patternDatos2):
               if re.compile(c.patternDatos2).search(d[0]):
                  c.d2 = map( self.patternData, d[1:] )
                    
   def generaGifs( self ):
      for c in self.grafs:
         cg = Chart( unique.getUniqueName("","gif"), 
                     c.titulo, c.xtitulo, c.ytitulo, 
                     tuple(self.labels), tuple(c.d1), tuple(c.d2),
                     gif_tps["3DBAR"], c.size )
         if   c.grf_tpo == 1  : cg.gif_datos1()
         elif c.grf_tpo == 2  : cg.gif_datos2()
         elif c.grf_tpo == 12 : cg.gif_datos_1y2()
         else                 : cg.gif_datos_2y1()
         print '<p><img href="%s">%s</img>' % ( cg.fullName(), c.titulo )

#cc = CCharts()
#cc.loadDefiniciones( "FORMATOS/sales.grf" )
##cc.getLabels( datos)
##cc.getDatos( datos)
#cc.generaGifs()
      
