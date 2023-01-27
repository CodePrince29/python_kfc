#! /usr/bin/env python
#  Ya no pide nombre del usuario. Simplemente procesa los mensajes
#	7/31/96	  J. Strout		http://www.strout.net/
#   2/28/2000 Miguel Angel Zavaleta

# import needed modules:

from socket import *		# get sockets, for well, sockets
import string				# string functions
import time					# for sleep(1) function
import os
import scan
import fmt

# define global variables
REPDIR="/usr/fms/op/rpts/"
REPFTP="/home/httpd/html/rpts/"
HOST = 'localhost' # Symbolic name meaning the local host
PORT = 4000				# Arbitrary non-privileged server
endl = "\r\n"			# standard terminal line ending

done = 0				# set to 1 to shut this down

kAskName = 0			# some constants used to flag
kOK = 2


def procesa_file( filename, fecha ):
   fmtfile  = REPDIR + filename + "/" + filename + ".fmt"
   datafile = REPDIR + filename + "/" + fecha
   csvfile  = REPFTP + filename + "/" + fecha + ".csv"
   
   print fmtfile
   print datafile
   print csvfile
   fmts = fmt.leer_fileFmt(fmtfile)
   datos = scan.scan_file( datafile, fmts )
   scan.datos_tofile( csvfile, datos )
   msg = "excel sales/00-03-06"
   newname = msg[6:]
   #newname = "sales/00-03-04"
   filename, p_dia =  string.split(newname,'/')
   print filename, p_dia
   
   

procesa_file("sales" , "00-03-06")
