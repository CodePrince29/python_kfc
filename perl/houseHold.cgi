#!/usr/bin/perl -w
use CGI;

$cgi= new CGI;
@llaves = $cgi->param();
foreach $key (@llaves) {
  $parametros{$key}= $cgi->param($key);
}

printf ("Content-type: text/html\n\n");

$radio_flag="FALSE";
$radio_error="";
$radio_msg="";
$FILE="/usr/bin/ph/ml/dat/houseHold.dat";
if (defined ($parametros{"recarga"}) && ($parametros{"recarga"} =~ /^TRUE$/)) {
  if ($parametros{"radio1"} =~ /^Salvar$/) {
    
    system (("cp","$FILE","$FILE.bak")) == 0 or die "No pudo respardarse el archivo $FILE: $!";
    $FILE=">$FILE";
    open FILE or die "No puede abrirse el archivo $FILE: $!";
    $radio_error="";
    foreach $key (sort (keys(%parametros))) {
      if ($key !~ /radio1/ && $key !~ /recarga/) {
        if ($parametros{$key}!~ /^[0-9]*$/ || ($key=~ "" && $parametros{$key}!=0)) {
  		$radio_error="$radio_error Secci&oacute;n '$key' => '$parametros{$key}' => se guard&oacute; 0 en su lugar.<br>";
          $parametros{$key}=0;
  	    }
        printf (FILE "%s|%s\n",$key,$parametros{$key});
  	  }
    }
    if ($radio_error =~ /[^0-9]/) {
      $radio_error=" ERROR: <br> Por favor, revise estas secciones: <br> $radio_error";
    }
    close FILE or $radio_error="No puede cerrarse el archivo $FILE: $!";
    $comando=". /usr/bin/ph/sysshell.new SUS >/dev/null;/usr/bin/ph/ml/bin/houseHold.s";
    system ($comando) == 0 or $radio_error="No pudo ejecutarse $comando: $!";
	$radio_msg="Archivo de House Hold Guardado y Actualizado";
    $radio_flag="TRUE";
  }
#  if ($parametros{"radio1"} =~ /^HouseHold$/) {
#    $comando="/usr/bin/ph/ml/bin/houseHold.s";
#    system ($comando) == 0 or $radio_error="No pudo ejecutarse $comando: $!";
#	$radio_msg="Archivo de House Hold Actualizado";
#    $radio_flag="TRUE";
#  }
  if ($parametros{"radio1"} =~ /^Historia$/) {
    $comando="/usr/bin/ph/ml/bin/phgenHis_grid.s";
    system ($comando) == 256 or $radio_error="No pudo ejecutarse $comando: $!";
    $comando="rm /usr/bin/ph/phgrid_semanal/*";
    system ($comando);
	$radio_msg="Archivos de Historia Generados";
	$radio_flag="TRUE";
  }
} else {
    $comando=". /usr/bin/ph/sysshell.new SUS >/dev/null;/usr/bin/ph/ml/bin/houseHold.s";
    system ($comando) == 0 or $radio_error="No pudo ejecutarse $comando: $!";
	$radio_msg="Archivo de House Hold Actualizado";
}
  $FILE="/usr/bin/ph/ml/dat/houseHold.dat";
  open FILE or die "No puede abrirse el archivo $FILE: $!";
  @registros=<FILE>;
  close FILE or die "No puede cerrarse el archivo $FILE: $!";

print <<EOF;
  <HTML>
    <HEAD>
      <TITLE> Captura de House Hold </TITLE>
    </HEAD>
    <BODY BGCOLOR=WHITE>
    <center><br> <font color=>  <u><h2> Captura de House Hold </h2></u></font></center>
EOF
#if ($radio_flag =~ "TRUE") {
  print <<EOF;
  <CENTER> <FONT size=12 color=green>$radio_msg</FONT><br>
           <FONT size=14 color=RED> $radio_error </FONT>
  </CENTER>
EOF
#}
print <<EOF;
      <FORM action="houseHold.cgi" method=post>
      <input type=hidden name=recarga value=TRUE>
      <CENTER>
    <TABLE widht=100%>
    <TR>
    <TD width=40%>
      <TABLE Border=1 bordercolor=black bgcolor="#CDCDCD">
        <TR>
	  <TH> COORD </TH>
	  <TH> HOUSE HOLD </TH>
        </TR>
EOF
chomp(@registros);
for ($i=0;$i<=$#registros;$i++) {
  ($coordenadas[$i],$hh[$i])= split /\|/,$registros[$i];
  $reng_coord="<TD> $coordenadas[$i] </TD>";
  if ($coordenadas[$i] =~ /^$/) {
    $reng_coord="<TD> Sin Coord. </TD>";
  }
  print <<EOF;
    <TR>
      $reng_coord
      <TD align=center> <input name="$coordenadas[$i]" value="$hh[$i]" maxlength=4 size=4> </TD>
    </TR>
EOF
}
print <<EOF;
  </TABLE>
  </TD>
  <TD valign=top widht=30%>
	  La Historia debe regenerarse cada vez que haya terminado el proceso de
      captura de House Hold. (El proceso tarda un poco)
<!--	  <p> El House Hold debe regenerarse cada vez que se haya aumentado una nueva
	  secci&oacute;n. -->
	  <CENTER>
      <TABLE BORDER=1>
        <TR>
        <TD>
      <p><input type=radio name=radio1 value="Historia" >Regenera Historia <br>
	    <!--<input type=radio name=radio1 value="HouseHold" >Regenera House Hold <br>-->
	    <input type=radio name=radio1 value="Salvar" CHECKED> Salvar <br>
		<CENTER>
        <input type=submit value="Aceptar"> <br>
		</CENTER>
		</TD>
		</TR>
      </TABLE>
      <p><input type=reset value="Restaurar">
	  </CENTER>
  </TD>
  <TR>
  </TABLE>
  </CENTER>
  </FORM>
</HTML>
EOF
