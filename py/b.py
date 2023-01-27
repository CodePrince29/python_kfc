def list2sec(lista):
   b = ()
   for x in range(len(lista) ):
      b = b + ( lista[x], )
   return b

mylist = [ 1.5, 2.5, 3, 4 ]
print list2sec( mylist )
