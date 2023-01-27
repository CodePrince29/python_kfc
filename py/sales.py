#! /usr/bin/env python
#
import unique
import chart
import string
import re

# Todos los gifs se pondran en este directorio
RTMPDIR="/tmp/"

HTMLFILE = unique.getUniqueName("" ,"html")
GRAFILE = "/home/httpd/html/tmp/" + HTMLFILE
GIF1    = unique.getUniqueName("1","gif" )
GIF2    = unique.getUniqueName("2","gif" )
GIF3    = unique.getUniqueName("3","gif" )


def list2sec(lista):
   """ Convierte una lista a una tupla, es necesario para poder utilizar
       el operador % ( formatos tipo printf )
   """
   b = ()
   for x in range( len(lista) ):
      b = b + ( lista[x], )
   return b
    

def write_header(f, store, reportName, unidad, fecha):
   s = """<HTML>
<HEAD> 
<TITLE>WebTricon Graphs vers. 0.1</TITLE> 
<META HTTP-EQUIV="EXPIRES" CONTENT="0">
</HEAD>
<BODY  LINK="#800000" VLINK="#008040" bgcolor="FFFFFF">
<table width="100%%" >
<tr>
<td align="left" ><h3>Unidad %s %s </h3></td>
<td align="right"><h3> Fecha: %s </h3></td>
</tr>
<tr>
<td colspan=2 align=center ><h1> %s </h1></td>
</tr>
</table>
<hr width=450>
"""
   f.write(s % (unidad, store, fecha, reportName) )


def write_footer(f): f.write("\n</BODY></HTML>")


def write_graf(f, supertitulo, imagen ):
   s = """
<!--- begin of graph ---> 
<CENTER> <H2 ALIGN=CENTER>%s</H2> <img src="%s"> <hr width=450> </CENTER>
<!--- end of graph ---> 
   """
   f.write(s % (supertitulo, imagen))


def grafica_sales(filename):
   f = open(filename,"r")
   lineas = f.readlines()   
   f.close()

   i = 0
   
   for l in lineas:
      v = re.split("  *", string.strip(l))
      if len(v) > 7:
         if v[2] == "Cuenta":
            etiquetas = v[3:10]
         if v[0] == "Total" and v[1] == "Ventas" and v[2] == "Netas":
            ventasNetas = v[3:10]
            datos1 = map( float, ventasNetas )
         if v[0] == "Total" and v[1] == "Gastos" and v[2] == "Netos":
            gastosNetos = v[3:10]
            datos2 = map( float, gastosNetos )
      
   f = open(GRAFILE,"w")
   v = re.split("  *", string.strip(lineas[3]))
   p_unidad = v[2]
   v = re.split("  *", string.strip(lineas[2]))
   p_fecha  = v[len(v) - 1] 
   write_header(f, string.strip(lineas[0]), string.strip(lineas[1]),
        p_unidad, p_fecha)

   n = chart.Chart( GIF1, "Ventas netas\npor semana",
              "Pesos", "Dias de la semana",
               tupla(etiquetas), 
               tupla(datos1), tupla(datos2) )
   n.size = (250, 200)
   n.gif_datos1()
   n.setGifName(GIF2)
   n.title = "Gastos netos\npor semana"
   n.setColors( (chart.BLANCO, chart.ROJO) )
   n.gif_datos2()
   n.setGifName(GIF3)
   n.title = "Ventas vs Gastos\npor semana"
   n.size = (500, 400)
   n.gif_datos_2y1()

   write_graf(f,"Ventas netas por semana"    , RTMPDIR+GIF1)
   write_graf(f,"Gastos netos por semana"    , RTMPDIR+GIF2)
   write_graf(f,"Ventas vs Gastos por semana", RTMPDIR+GIF3)
   write_footer( f )
   f.close()
   return "/tmp/" + HTMLFILE
#print grafica_sales("/usr/fms/op/rpts/sales/00-03-06")
