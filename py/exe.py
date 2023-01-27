#! /usr/bin/env python
# Recibe de la linea de comandos los programas a ejecutar
#
# DIRECTORIO=/usr/fms/op/rpts
#
#
#
import cgi
import string
import posix


def main():
   print "Content-type: text/html\n"
   print """<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2//EN">
<HTML>
</HEAD>"""
   print '<BODY background="/tricon/book.jpg">'
   print 'nada que ver'      
   print "</BODY></HTML>"

   form = cgi.FieldStorage()
   p_dia = form["diaActual"].value
   for k in form.keys() :
      if k == "txtReporte" :
         lista = string.split(form[k].value,';') 
         for j in lista :
            posix.system(j)
      else :
         pass # print "<p>%s </p>" % k


if ( __name__ == "__main__" ) :
   main()
