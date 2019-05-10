rm -rf ~/sirilive/scan/*.fits

for i in `ls -d -1  ~/sirilive/sample/Light_*.fits`
#for i in `ls -d -1  /home/berylius/20190329/Light/*.fits`
#for i in `ls -d -1  /home/gilles/ekos/20180622/Light/M27*.fits`
  do
 
  echo "$i"
  cp "$i" ~/sirilive/scan
  sleep 1
 
done

