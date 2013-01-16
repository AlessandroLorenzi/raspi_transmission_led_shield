raspi\_transmission\_led\_shield
=============================

An easy project to test RaspberryPI GPIO. 

Thanks to this program is possible to see transmission status
giving a look to 3 leds:
  * first led: transmission ko.
  * second led: transmission downloading
  * third led: seeding

In connections.png there is a (horrible) schema of connections.


put raspi\_transmission\_led\_shield.service in /usr/lib/systemd/system/

then
systemctl enable  raspi\_transmission\_led\_shield.service
