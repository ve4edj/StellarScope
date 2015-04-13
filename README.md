# StellarScope
NASA Space Apps Challenge 2015 - Winnipeg, Canada

A Stellarium-powered Virtual Reality Telescope

Requires
--------
 - Stellarium
 - PySerial

To Run
------
python stellariumServer.py usbmodemfd121 5

Where: /dev/tty.usbmodemfd121 is your Arduino and your Stellarium clock is set 5 hours ahead of real-time

License
-------
MIT-licensed

ToDo
----
 - Refactor latitude and longitude to command-line arguments (optional, see below)
 - Add capability to the arduino code to send coordinates to the computer from the GPS
 - Refactor all the python code into a Stellarium Plugin
