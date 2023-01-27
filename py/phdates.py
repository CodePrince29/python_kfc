#!/usr/bin/env python
#
# phdates.py   Funciones para manejo de fechas y periodos 
#
import string
import time
import sys

def get_secsFrom70( sFecha ):
   ''' devuelve el numero de segundos desde la fecha origen 01011970 '''
   return time.mktime(time.strptime(sFecha+" 08:00:00","%y-%m-%d %H:%M:%S"))

def get_days(sFecha):
   ''' sFecha esta en formato yy-mm-dd '''
   segundos = time.mktime(time.strptime(sFecha+" 08:00:00","%y-%m-%d %H:%M:%S"))
   sxd = 60 * 60 * 24
   return int( segundos / sxd )

def get_periodo(sFecha):
   p_dias = get_days(sFecha)
   f = open("/usr/fms/data/invcaldr.txt","r")
   while 1:
      try:
         vec = string.split(f.readline(),' ')
         #print vec
      except EOFError:
         break
      if 5 <= len(vec):
         p_year = int(vec[2])
         p_per  = 0
         p_sem  = 0
      else:
         if int(vec[2]) <= 5:
            p_per = p_per + 1
            p_sem  = 0
         else:
            p_sem = p_sem + 1
            if int(vec[0]) <= p_dias and p_dias <= int(vec[1]): 
               break
   f.close()
   return ( p_year, p_per, p_sem )

def yps( parm_year, parm_per, parm_sem ):
   ''' el dia de inicio y fin del periodo dado '''
   f = open("/usr/fms/data/invcaldr.txt","r")
   flg_year = flg_per = flg_sem = 0   # inicializa las banderas
   while 1:
      try:
         vec = string.split(f.readline(),' ')
      except EOFError:
         break
      if 5 <= len(vec):
         if parm_year ==  int(vec[2]): 
            flg_year = 1
            flg_per = 0
         else:
            flg_year = 0
         p_per = 0
      else:
         if int(vec[2]) <= 5:
            p_per = p_per + 1
            p_sem  = 0
            if p_per == parm_per:
               flg_per = 1
               flg_sem = 0
         else:
            p_sem = p_sem + 1
            if p_sem == parm_sem:
               flg_sem = 1
            if flg_year and flg_per and flg_sem:
               break
   f.close()
   return ( int(vec[0]), int(vec[1]) )

def y_m_d( nDia ):
   return time.strftime( "%y-%m-%d", time.gmtime(nDia*60*60*24) )
   
#
#if len(sys.argv):
#   arr =  get_periodo(sys.argv[1])
#   print arr
#   print get_days(sys.argv[1])
#   print yps( arr[0], arr[1], arr[2] )
#   fechas =  yps( arr[0], arr[1], arr[2] )
#   print y_m_d(fechas[0]),  y_m_d(fechas[1]) 
#v = yps(1999, 4, 3)
#print v
#print y_m_d(v[1])

   


