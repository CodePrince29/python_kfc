#! /usr/bin/env python

def common_header(categoria, filename):
   """ imprime un header con un color para cada categoria """
   if categoria == "V"   : color="#006060"
   elif categoria == "I" : color="#006000"
   elif categoria == "M" : color="#600060"
   elif categoria == "E" : color="#000060"
   elif categoria == "P" : color="#600000"
   else                  : color="#606000"
   print """
<table bgcolor="#FFFFFF" >
<tr>
<td width=15%%>
   <img SRC="/reporteador/images/ph_small.gif" ALT="Logo Pizza Hut" align=BOTTOM>
</td> 
<td> 
   <br> 
   <table bgcolor="%s">
   <tr>
   <td align="center">
   <font size=+3 color="#FFFFFF">%s</font>
   </td>
   </tr>
   </table> 
   <br>
   <p><font size=-1>Copyright &copy; Tricon</font>
   <br><font size=-1>All Rights Reserved</font>
</td>
<td width=15%%>
   <img SRC="/reporteador/images/kfc.gif" ALT="Logo de Kentucky"  align=BOTTOM>
</td>
</tr>
</table>
   """ % (color, filename)

def header():
   print "Content-type: text/html\n"
   print """
   <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2//EN">
   <HTML> <HEAD>
   <!-- This file generated using Python -->
   <TITLE>TRIWEB REPORTES!</TITLE>
   <link rel=stylesheet href="/reporteador/HTMLrpts.css" 
     type=text/css title="reports.css">
   </HEAD><BODY background="/reporteador/book.jpg">
    """

def footer():
   print "</BODY></HTML>"

#common_header("V", "sales")
