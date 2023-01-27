#!/usr/bin/env python
#
# Devuelve un nombre unico
#
from whrandom import randint
from time     import time

def getUniqueName(pref, subfijo):
   if len(pref) == 0:
      return repr(time()) + "."+ subfijo
   else: 
      return pref + "_"  + repr(time()) + "."+ subfijo

def getRandomName(pref, subfijo):
   if len(pref) == 0:
      return repr(randint(1,10000)) + "."+ subfijo
   else:
      return pref + "_"  + repr(randint(1,10000)) + "."+ subfijo

#print getUniqueName("99-03-20","gif")
#print getUniqueName("","gif")
#print getRandomName("99-03-20","gif")
#print getRandomName("","gif")

