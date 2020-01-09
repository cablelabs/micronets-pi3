#!/bin/bash

/usr/bin/fbi -T 2 -d /dev/fb1 -noverbose -a /usr/local/images/splash.png  2> /dev/null

# without the sleep, the service/script exits before the frame buffer is written to.
sleep 2
