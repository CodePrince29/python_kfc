#! /usr/bin/env python
# 
#   7/31/96     J. Strout      http://www.strout.net/
#   2/28/2000 Miguel Angel Zavaleta
#
from socket import *      # get sockets, for well, sockets
import string            # string functions
import time               # for sleep(1) function
import os
import scan                 # rutinas para convertir de .txt a .csv
import fmt                  # escanea archivo de formatos (.fmt)

#
# Definicion de los comandos aceptados entre el servidor y el cliente
# shutdown           ; darse de baja
# excel file/fecha   ; escanear el archivo txt y convertirlo a csv
#                       dejar el archivo en el directorio /tmp/rpts/
#                       El archivo txt debe existir bajo /usr/fms/op/rpts
# cddata directorio  ; Nombre del nuevo directorio de datos (/usr/fms/op/rpts)
# cdcsv  directorio  ; Nombre del nuevo directorio html (/home/httpd/html/rpts)
# cdfmt  directorio  ; Nombre del nuevo directorio de formatos
#
# editfmt file       ; Editar con el vi el archivo de formatos del file.
# subcmd  newcmd     ; Sustituye el comando anterior de ejecucion.
# cmd     cmd:parms  ; Ejecuta en un proceso hijo el comando pedido
#
# reset              ;
# show               ; muestra los parametros actuales
# loggon file        ; new logfile
# help               
# quit               
#
   
class Config:
   def __init__(self, dir_data, dir_csv, dir_fmt, cmd, logfile):
      self.DIR_DATA = dir_data
      self.DIR_CSV  = dir_csv
      self.DIR_FMT  = dir_fmt
      self.CMD      = cmd
      self.LOGFILE  = logfile

   def setDirData(self, dirname): self.DIR_DATA = dirname
   def setDirCsv (self, dirname): self.DIR_CSV  = dirname
   def setDirFmt (self, dirname): self.DIR_FMT  = dirname
   def setCmd    (self, dirname): self.CMD      = dirname
   def setLog    (self, dirname): self.LOGFILE  = dirname
      
   def getDirData(self ): return self.DIR_DATA
   def getDirCsv (self ): return self.DIR_CSV 
   def getDirFmt (self ): return self.DIR_FMT 
   def getCmd    (self ): return self.CMD     
   def getLog    (self ): return self.LOGFILE 

   def show( self ):
      s = """DIR_DATA = %s
DIR_CSV  = %s
DIR_FMT  = %s
CMD..... = %s
LOGFILE  = %s
      """ % (self.DIR_DATA, self.DIR_CSV, self.DIR_FMT, self.CMD, self.LOGFILE)
      return s
       
def tolog(s, c):
   f = open(c.getLog(),"a")
   f.write(s) 
   f.write("\n")
   f.close()

def procesa_file( filename, fecha , myconf ):
   datafile = myconf.getDirData() + filename + "/" + fecha
   csvfile  = myconf.getDirCsv()  + filename + "/" + fecha + ".csv"
   fmtfile  = myconf.getDirFmt()  + filename + "/" + filename + ".fmt"
   
   fmts = fmt.leer_fileFmt(fmtfile)
   datos = scan.scan_file( datafile, fmts )
   scan.datos_tofile( csvfile, datos )
   return csvfile
   
def edit_fmt( filename ):
   filefmt = DIR_FMT + filename + "/" + filename + ".fmt"
   os.system("vi " + filefmt)

def help(conn):
   s = """
  Definicion de los comandos aceptados entre el servidor y el cliente
  --------------------------------------------------------------------
  shutdown           ; darse de baja
  excel file/fecha   ; escanear el archivo txt y convertirlo a csv
                        dejar el archivo en el directorio /tmp/rpts/
                        El archivo txt debe existir bajo /usr/fms/op/rpts
  cddata directorio  ; Nombre del nuevo directorio de datos (/usr/fms/op/rpts)
  cdcsv  directorio  ; Nombre del nuevo directorio html (/home/httpd/html/rpts)
  cdfmt  directorio  ; Nombre del nuevo directorio de formatos
 
  editfmt file       ; Editar con el vi el archivo de formatos del file.
  subcmd  newcmd     ; Sustituye el comando anterior de ejecucion.
  cmd     cmd:parms  ; Ejecuta el comando pedido en un subproceso
 
  reset              ;
  show               ; muestra los parametros actuales
  loggon file        ; new logfile
  help               
  quit               
   """
   conn.send(s)

def HandleMsg(conn, msg, myconf ):
   print "Handling message: ",msg
      
   # check for commands
   if msg[0:5] == "excel":
      conn.send(msg)
      conn.close()
      v = string.split(msg[6:],'/')
      if len(v) < 2:
         filename = v[0]
         p_dia = ""
      else:
         filename = v[0]
         p_dia = v[1]
         n = os.fork()
         if (n == 0 ): 
            csvfile = procesa_file( filename, p_dia, myconf )
            os.execl(myconf.getCmd(), myconf.getCmd(), csvfile)
      tolog(msg, myconf)
      return

   if msg[0:3] == "cmd":
      v  = string.split(msg[4:],':')
      if len(v) < 2:
         t_cmd = v[0]
         t_parms = ""
      else:
         t_cmd = v[0]
         t_parms = v[1]
      conn.send("Executing ... " + t_cmd + "\n")
      conn.close()
      n = os.fork()
      if (n == 0 ): 
         os.execl(t_cmd, t_cmd, t_parms)
      tolog(msg, myconf )
      return
   if msg == "quit":
      conn.close()
      return
   if msg == "help":
      help(conn)
      conn.close()
      tolog("help", myconf )
      return
   if msg == "reset" :
      myconf.setDirData("/usr/fms/op/rpts/")
      myconf.setDirCsv("/home/httpd/html/rpts/")
      myconf.setDirFmt("/usr/fms/op/rpts/")
      myconf.setCmd("/usr/local/Office51/bin/soffice")
      myconf.setLog("/home/httpd/cgi-bin/py/excelserver.log")
      conn.send( myconf.show() )
      conn.close()
      tolog("reset...", myconf )
      return
   if msg == "show"  :
      conn.send( myconf.show() )
      conn.close()
      tolog("show...", myconf )
      return

   if msg[0:6] == "cddata":
      myconf.setDirData( msg[7:] )
      conn.send("DIR_DATA = " + myconf.getDirData() )
      conn.close()
      tolog(msg, myconf )
      return
   if msg[0:5] == "cdcsv" :
      myconf.setDirCsv( msg[6:] )
      conn.send("DIR_CSV = " + myconf.getDirCsv() )
      conn.close()
      tolog(msg, myconf )
      return
   if msg[0:5] == "cdfmt" :
      myconf.setDirFmt( msg[6:] )
      conn.send("DIR_FMT = " + myconf.getDirFmt() )
      conn.close()
      tolog(msg, myconf )
      return
   if msg[0:6] == "subcmd":
      myconf.setCmd( msg[7:] )
      conn.send("CMD = " + myconf.getCmd() )
      conn.close()
      tolog(msg, myconf )
      return
   if msg[0:6] == "loggon":
      myconf.setLog( msg[7:] )
      conn.send("LOGFILE = " + myconf.getLog() )
      conn.close()
      tolog(msg, myconf )
      return
   if msg[0:7] == "editfmt":
      n = os.fork()
      if ( n == 0):
         edit_fmt( msg[8:] )
         tolog(msg, myconf )
      conn.close()
      return
   tolog("Unknown message : " + msg, myconf )
   print "Unknown message : " + msg
   conn.send(" comando no valido: " + msg+ endl )
   conn.close()

#
# MAIN PROGRAM
#
HOST = 'localhost' # Symbolic name meaning the local host
PORT = 4000              # Arbitrary non-privileged server

myconf = Config( "/usr/fms/op/rpts/"     ,
                 "/home/httpd/html/rpts/",
                 "/usr/fms/op/rpts/"     ,
                 "/usr/local/Office51/bin/soffice"        ,
                 "/home/httpd/cgi-bin/py/excelserver.log" )

# set up the server

s = socket(AF_INET, SOCK_STREAM)
s.bind(HOST, PORT)
s.setblocking(0)
s.listen(1)
print "Waiting for connection(s)..."

# loop until done, handling connections and incoming messages
endl = "\r\n"          # standard terminal line ending
done = 0             # set to 1 to shut this down

while not done:
   time.sleep(1)      # sleep to reduce processor usage
   try:
      conn, addr = s.accept()
      print "Connection from", addr
      data = conn.recv(1024)
      if not data: 
         break
      data = filter(lambda x: x>=' ' and x<='z', data) 
      data = string.strip(data)
      if data == "shutdown": 
         tolog("shutdown....", myconf )
         print "Recibi un shutdown, adios"
         done = 1
      else: 
         HandleMsg(conn, data, myconf) 
      conn.close()
   except:
      addr = ""
        
s.close()
