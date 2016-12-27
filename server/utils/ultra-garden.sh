#!/bin/sh -e
### BEGIN INIT INFO
# Provides:          garden
# Required-Start:    mountkernfs $local_fs
# Required-Stop:     
# Default-Start:     S
# Default-Stop:      0 6
# Short-Description: Raise garden.
# Description:       Raise balkony garden.
### END INIT INFO

case "$1" in
start)
   python /home/pi/ultraGarden/server/utils/ultraGarden.py &
   ;;  

stop)
   killall python
   ;;  

*)
   echo "Usage: /etc/init.d/ultra-garden {start|stop}"
   exit 1
   ;;  
esac

exit 0

