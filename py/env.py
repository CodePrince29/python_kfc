#!/usr/bin/env python
#
# env.py
#
import os
import string

fms_env="/usr/fms/.xenv"
sus_env="/usr/fms/op/bin/.xenv"

def put_env(env_file):
   f = open(env_file)
   lineas = f.readlines()
   f.close
   for li in lineas:
      v = map(string.strip, string.split(li,"=") ) 
      if len(v) == 2:
         os.environ[v[0]] =  v[1]

def put_sus(): put_env(sus_env)
def put_fms(): put_env(fms_env)

