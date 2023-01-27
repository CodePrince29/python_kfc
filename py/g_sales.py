#!/usr/bin/env python
#
# Programa para formatear las tablas html automaticamente
#
import string
import re
import sys

GRAFILE="/home/httpd/html/devtricon/graf1.php3"

def list2sec(lista):
   """ Convierte una lista a una tupla, es necesario para poder utilizar
       el operador % ( formatos tipo printf )
   """
   b = ()
   for x in range(len(lista) ):
      b = b + ( lista[x], )
   return b


def write_header(f, store):
   s = """<HTML>
<HEAD> 
<TITLE>WebTricon Graphs vers. 0.1</TITLE> 
</HEAD>
<BODY  LINK="#800000" VLINK="#008040" bgcolor="FFFFFF">
<h1>%s</h1>
<?
require("./html_graphs.php3");
?>
"""
   f.write(s % store)


def write_footer(f): f.write("\n</BODY></HTML>")


def write_graf(f, supertitulo, names, valores, hlabel, vlabel, tipo, imagen ):
   s = """
<CENTER>
<!--- begin of graph ---> 
<H2 ALIGN=CENTER>%s</H2>
<?
    $names  = array("%s","%s","%s","%s","%s","%s","%s");
    $values = array(%d, %d, %d, %d, %d, %d, %d);
    $largest = max($values);

   """
   sec_val = map( float, valores)
   parametros = ( supertitulo, ) + list2sec(names) + list2sec(sec_val)
   f.write(s % parametros)

   s = """
    // Asigna el gif a utilizar para la barra de la grafica
    $bars  = array();
    for( $i=0;$i<SizeOf($values);$i++ ) {
        $bars[$i] = "%s";
    }

    // inicializacion del array
    $graph_vals = html_graph_init();

    // Notice I stick HTML tags in the vlabel to lay it out narrowly.
    // Also note that the "type" element denotes this to be a vertical
    // graph.
    $graph_vals["hlabel"] = "%s";
    $graph_vals["vlabel"] = "%s";
    $graph_vals["type"] = %d;
    $graph_vals["vfcolor"] = "#FFFFFF";
    $graph_vals["hfcolor"] = "#FFFFFF";
    $graph_vals["vbgcolor"] = "#000000";
    $graph_vals["hbgcolor"] = "#000000";
    $graph_vals["width"] = 350;
    $graph_vals["cellspacing"] = "1";
    $graph_vals["scale"] = 250 / $largest;
    $graph_vals["namefcolor"] = "#000000";
    $graph_vals["namebgcolor"] = "#F7EFDE";

    html_graph($names, $values, $bars, $graph_vals);
   """
   s = s % ( imagen, hlabel, vlabel, tipo )
   f.write(s)
   f.write('?>\n')
   f.write('<!--- End of Graph ---> </CENTER>\n')


def write_graf2(f, supertitulo, names, vals1, vals2, hlabel, vlabel, tipo,
image1, image2 ):
   s = """
<!--- Seventh Graph --->
<center> 

<H2 ALIGN=CENTER>%s</H2> 

<?
    // This is a double vertical graph where each entry has TWO value arrays and
    // TWO bars arrays.  
    $names   = array("%s","%s","%s","%s","%s","%s","%s");
    $values  = array(%d,%d,%d,%d,%d,%d,%d);
    $dvalues  = array(%d,%d,%d,%d,%d,%d,%d);
    $largest =  max($values);

    // You cannot use color codes in the vertical charts. For this 
    // reason we use only graphics in the bars and dbars array.
    $bars  = array();
    for( $i=0;$i<SizeOf($values);$i++ )
       {
        $bars[$i] = "%s";
       }
    $dbars  = array();
    for( $i=0;$i<SizeOf($values);$i++ )
       {
        $dbars[$i] = "%s";
       }

    $graph_vals = array("vlabel"=>"%s",
                        "hlabel"=>"%s",
                        "type"=>%d,
                        "cellpadding"=>"1",
                        "cellspacing"=>"1",
                        "border"=>"",
                        "width"=>"",
                        "vfcolor"=>"#FFF3FF",
                        "hfcolor"=>"#FFF3FF",
                        "vbgcolor"=>"#FF3339",
                        "hbgcolor"=>"#FF3339",
                        "vfstyle"=>"Verdana, Arial, Helvetica",
                        "hfstyle"=>"Verdana, Arial, Helvetica",
                        "scale"=>200/$largest,
                        "namebgcolor"=>"#F73FDE",
                        "namefcolor"=>"",
                        "valuefcolor"=>"#000000",
                        "namefstyle"=>"Verdana, Arial, Helvetica",
                        "valuefstyle"=>"",
                        "doublefcolor"=>"#0000000");

    html_graph($names, $values, $bars, $graph_vals, $dvalues, $dbars);

?>

<!--- Legend --->

<IMG SRC="%s" HEIGHT=10 WIDTH=10> - Ventas
<BR>
<IMG SRC="%s" HEIGHT=10 WIDTH=10> - Gastos

</center> 
<!--- End of Seventh Graph --->
"""
   sec_val1 = map( float, vals1)
   sec_val2 = map( float, vals2)
   parametros = ( supertitulo, )+ list2sec(names)+ list2sec(sec_val1)+ list2sec(sec_val2)+ (image1, image2, vlabel, hlabel, tipo, image1, image2)
   f.write(s % parametros )

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
         if v[0] == "Total" and v[1] == "Gastos" and v[2] == "Netos":
            gastosNetos = v[3:10]
      
   f = open(GRAFILE,"w")
   write_header(f, "Felix Cuevas" )
   write_graf(f, "Ventas netas por semana", 
              etiquetas, ventasNetas, "Ventas Netas","F<BR>e<BR>c<BR>h<BR>a",
              2, "images/hbar_blue.gif")
   write_graf(f, "Gastos netos por semana",
              etiquetas, gastosNetos, "Gastos Netos","F<BR>e<BR>c<BR>h<BR>a",
              2, "images/hbar_red.gif")
   write_graf2(f," Ventas netas vs Gastos netos ",
               etiquetas, ventasNetas, gastosNetos,
               "Fechas", "P<BR>e<BR>s<BR>o<BR>s",
               3, "images/hbar_blue.gif", "images/hbar_red.gif")

   write_footer( f )
   f.close()
#grafica_sales("/usr/fms/op/rpts/sales/00-03-02")
