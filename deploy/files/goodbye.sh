#!/bin/bash
counter=0
while [ $counter -lt 10 ]
do
  /usr/bin/fbi -T 2 -d /dev/fb1 -noverbose -a /usr/local/images/goodbye.png  2> /dev/null
  sleep 1s
  counter=$(expr $counter + 1)
done
