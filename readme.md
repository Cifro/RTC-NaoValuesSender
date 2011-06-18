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

2. Start CORBA name server (see OpenRTM-aist documentation)

3. Run NaoValuesSender.py
 `$ python NaoValuesSender.py`

4. Run ConsoleOut.py
 `$ python ConsoleOut.py`

5. Run Connector.py
 `$ python Connector.py`

6. Hit any key in NaoValuesSender console window if prompt

7. See results in ConsoleOut console window

About
======

Author:  Cifro Nix
Version: 1.0