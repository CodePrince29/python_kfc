echo -n "De la direccion IP del equipo : "; read dirip
echo -n "Hacer la sustitucion por la ip $dirip (S/N) : "; read ans
case $ans in
  s*|S*|y*|Y*)
    cd /home/httpd/html/tricon
    pwd
    for i in *.html
    do
    echo $i
        sed "s/192.168.101.254/$dirip/g" $i > tmp.$$
        mv tmp.$$ $i
    done
    cd /home/httpd/cgi-bin/py
    pwd
    for i in *.py
    do
    echo $i
        sed "s/192.168.101.254/$dirip/g" $i > tmp.$$
        mv tmp.$$ $i
    done
    ;;
  *)
    echo "No se hizo nada"
    ;;
esac

