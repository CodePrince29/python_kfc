#!/usr/bin/env python
#
# exists.py
#
import os.path
import time
import datetime

def get_pqdate():
   find, fout = os.popen2("(. /usr/bin/ph/sysshell.new FMS > /dev/null 2>&1; /usr/fms/op/bin/phpqdate)")
   return fout.readline()

def distance( f1, f2 ):
   if f1 > f2:
      return -1
   d1 = int( f1[4:6])
   m1 = int( f1[2:4])
   y1 = 2000 + int( f1[0:2])
   d2 = int( f2[4:6])
   m2 = int( f2[2:4])
   y2 = 2000 + int( f2[0:2])
   fdif = datetime.date(y2,m2,d2) - datetime.date(y1,m1,d1)  
   return fdif.days

def newerThan( f, p_dias ):
   fname = os.path.basename(f)
   fname2 = fname[0:2] +  fname[3:5] + fname[6:8] 
   pqdate = get_pqdate()
   days = distance(fname2, pqdate )
   if days <= p_dias:
      return 1
   elif days < 0:
      return 0
   else:
      return 0

def exists( f ):
   try:
      n = os.path.getsize( f )
      if n > 0 :
         return 1
      else:
         return 0
   except:
      return 0


#while 1 :
#   filename = raw_input("File: ")
#   print filename
#   if len(filename) == 0: break
#   if exists(filename) > 0:
#      print "Ok existe"
#      if newerThan( filename, 1 ):
#         print "modificado hoy"
#      else:
#         print "modificado antes de hoy "
#   else:
#      print "No existe"
#
