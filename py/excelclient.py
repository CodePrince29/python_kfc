#! /usr/bin/env python
# excelclient.py      cliente para ejecutar comandos
#
from socket import *
import os
import cgi
import string
import phdates

# define global variables
HOST = 'localhost'
PORT = 4000

def header():
   print "Content-type: text/html\n"
   print """
   <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2//EN">
   <HTML> <HEAD>
   <!-- This file generated using Python -->
   <TITLE>MENU DE REPORTES!</TITLE>
   <META NAME="GENERATOR" CONTENT="HTMLgen 2.2.2">
   <link rel=stylesheet href="/tricon/HTMLrpts.css" 
     type=text/css title="reports.css">
   </HEAD><BODY background="/tricon/book.jpg">
    """

def footer():
   print "</BODY></HTML>"


def exe_excel( filename, p_year, p_periodo, p_semana, p_dia):
   if ( len(p_dia) <= 2 ):
      n_year = int(p_year)
      if ( n_year < 70 ) :
         n_year = n_year + 2000
      else :
         n_year = n_year + 1900
      fechas = phdates.yps( n_year,int(p_periodo),int(p_semana))
      p_dia = phdates.y_m_d(fechas[1])
   newname = filename + "/" + p_dia
   try: 
      print '<h4>Intentara abrir una hoja de calculo para ' + newname + '</h4>'
      h = os.fork()
      if ( h == 0 ):
         s = socket(AF_INET, SOCK_STREAM)
         s.connect(HOST, PORT)
         s.send('excel ' + newname)
         data = s.recv(1024)
         s.close()
   except:
      print '<h4>No hay datos para ' + newname + '</h4>'

def genera_html( lista, p_year, p_periodo, p_semana, p_dia):
   header()
   for j in lista :
      exe_excel(j, p_year, p_periodo, p_semana, p_dia)
   footer()



#
# MAIN
#
def main():
   form = cgi.FieldStorage()
   p_dia     = form["txtDia"].value
   p_periodo = form["txtPeriodo"].value
   p_semana  = form["txtSemana"].value
   p_year    = form["txtYear"].value
   strReportes = form["txtReporte"].value
   if p_dia     == 'N': p_dia = ""
   if p_semana  == 'N': p_semana = ""
   if p_periodo == 'N': p_periodo = ""
   if p_year    == 'N': p_year = ""

   lista = string.split(strReportes,':') 
   if len(lista):
      genera_html(lista, p_year, p_periodo, p_semana, p_dia)

if ( __name__ == "__main__" ) :
   main()
