#! /usr/bin/env python
#
# cgiparms.py
#
import cgi
import string
import phdates

class CCGIparms:
   def __init__(self):
      self.dia     = "N"
      self.semana  = "01"
      self.periodo = "01"
      self.year    = "00"
      self.nav     = ""
      self.ver     = ""
      self.strParms = ""
      self.cbTipo  = "false"
      self.reports = []

   def getCGIparms(self):
      form           = cgi.FieldStorage()
      self.dia       = form["txtDia"].value
      self.semana    = form["txtSemana"].value
      self.periodo   = form["txtPeriodo"].value
      self.year      = form["txtYear"].value
      self.nav       = form["txtNav"].value
      self.ver       = form["txtVer"].value
      try:
         self.strParms  = form["txtParms"].value
      except:
         self.strParms  = ""
        
      self.cbTipo    = form["cbTipo"].value
      
      # OJO: "
      #fp = open("/tmp/cgiparms.log","w")
      #fp.write( '1o.########################################## \n' )
      #fp.write( '   ### dia....=[ %s ] ###\n'  % (self.dia    )    )
      #fp.write( '   ### semana =[ %s ] ###\n'  % (self.semana )    )
      #fp.write( '   ### periodo=[ %s ] ###\n'  % (self.periodo)    )
      #fp.write( '   ### year   =[ %s ] ###\n'  % (self.year   )    )
      #fp.write( '   ### strParms=[%s]  ###\n'  % (self.strParms)   )
      #fp.write( '2o.####################### ################## \n' )
      #fp.close()
      # 
      if self.dia     == 'N': self.dia     = ""
      if self.semana  == 'N': self.semana  = ""
      if self.periodo == 'N': self.periodo = ""
      if self.year    == 'N': self.year    = ""
      #
      # generalmente toma la fecha de p_dia, al faltar la definicion de p_dia
      # debe crear una nueva definicion
      #
      if ( len(self.dia) <= 2 ):     
         n_year = int(self.year)      # reconstruye la fecha a partir
         if ( n_year < 70 ) :         # del a&o, periodo, semana
            n_year = n_year + 2000
         else :
            n_year = n_year + 1900
         vecfechas = phdates.yps( n_year, int(self.periodo), int(self.semana) )
         self.dia = phdates.y_m_d(vecfechas[1])
      self.reports = string.split( form["txtReporte"].value,':')


