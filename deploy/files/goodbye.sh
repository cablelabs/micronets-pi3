#!/bin/bash
counter=0

if [ -f "/tmp/rebooting" ]; then
    file='/usr/local/images/reboot.png'
else
    file='/usr/local/images/goodbye.png'
fi

while [ $counter -lt 100 ]

do
  /usr/bin/fbi -T 2 -d /dev/fb1 -noverbose -a $file  2> /dev/null
  sleep .1s
  counter=$(expr $counter + 1)
done
