#!/bin/bash

systemctl list-jobs | egrep -q 'reboot.target.*start'
if [ $?  -eq 0  ]; then
    file='/usr/local/images/reboot.png'
else
    file='/usr/local/images/goodbye.png'
fi

/usr/bin/fbi -T 2 -d /dev/fb1 -noverbose -a $file  2> /dev/null

# without the sleep, the service/script exits before the frame buffer is written to.
sleep 4
