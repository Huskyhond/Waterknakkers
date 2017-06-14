### GPS
De GPS python module is onderdeel van een Tinkerforge GPS brick.

#### Tinkerforge
Meer info over BrickD (Daemon die nodig is om GPS en IMU te gebruiken):
https://www.tinkerforge.com/en/doc/Software/Brickd_Install_Linux.html#brickd-install-linux

#### Requirements
```bash
# Raspberry
apt-get install libusb-1.0-0 libudev0 pm-utils
wget http://download.tinkerforge.com/tools/brickd/linux/brickd_linux_latest_armhf.deb
pip install tinkerforge
```

#### De UID achterhalen
Om de UID van de brick te achterhalen dien je de BrickV en BrickD te installeren op een Windows, Linux (Niet Raspberry PI), Mac OSX machine.
Bekijk dan in de BrickV de UID's. Dit zullen de zelfde UID's worden op andere devices.

#### Gebruiken
De get_gps.py wordt aangeroepen door de client in de APIConnection. Elke keer als er een input wordt verstuurd naar dit script wordt er een GPS coordinaat terug gegeven. Er wordt nu 10x per seconden een locatie gevraagd.