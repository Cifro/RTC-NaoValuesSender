OpenRTM-aist Component
======================

Two components:

* NaoValuesSender - sends values of all joints from robot Nao
* ConsoleOut - recieves all values and prints it out

Requirements
============

* Python 2.6+
* OpenRTM-aist
* Naoqi SDK

Usage
======

1. Set IP address of Nao in NaoValuesSender

2. Set IP adress of nameserver in rtc.conf and Connector.py

3. Start CORBA nameserver on server (see OpenRTM-aist documentation)

4. Run NaoValuesSender.py on local computer
 `$ python NaoValuesSender.py`

5. Run ConsoleOut.py on server
 `$ python ConsoleOut.py`

6. Run Connector.py on local computer
 `$ python Connector.py`

7. Hit any key in NaoValuesSender console window if prompt

8. See results in ConsoleOut console window

About
======

Author:  Cifro Nix
Version: 1.0