#! /usr/bin/env python
#
#
from socket import *
import os
import cgi
import string

HOST = 'localhost'
PORT = 4000

def exe_excel( p_dia, filename):
	newname = '/home/ftp/pub/rpts/' + filename + "/" + p_dia + ".xls"
	try: 
		f = open(newname)  # checa si existe
		f.close() 
		# 
		# intenta abrirlo utilizando un proceso hijo
		# 
		h = os.fork()
		if ( h == 0 ):
			s = socket(AF_INET, SOCK_STREAM)
			s.connect(HOST, PORT)
			s.send('excel ' + newname)
			data = s.recv(1024)
			s.close()
	except:
		print 'No hay datos para (' + newname + ')   '
def doc_vacio():
   print "Content-type: text/html\n"
   print """<html><head></head><body><h1>Documento vacio</h1></body></html>"""


#form = cgi.FieldStorage()
#p_dia = form["diaActual"].value
#exe_excel( p_dia, j )
exe_excel( "99-03-15", "dsales" )
