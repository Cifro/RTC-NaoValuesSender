#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- Python -*-

import sys
import time

import RTC
import OpenRTM_aist
import naoqi
from naoqi import ALProxy

# Naoqi stuff

NAO_IP = "127.0.0.1"
PORT = 9559


NaoValuesSender_spec = ["implementation_id", "NaoValuesSender",
                  "type_name",         "NaoValuesSender",
                  "description",       "Component for sending data from Nao with Naoqi framework",
                  "version",           "1.0",
                  "vendor",            "Cifro Nix",
                  "category",          "Simple example",
                  "activity_type",     "DataFlowComponent",
                  "max_instance",      "10",
                  "language",          "Python",
                  "lang_type",         "script",
                  ""]


class DataListener(OpenRTM_aist.ConnectorDataListenerT):
  def __init__(self, name):
    self._name = name

  def __del__(self):
    print "dtor of ", self._name

  def __call__(self, info, cdrdata):
    data = OpenRTM_aist.ConnectorDataListenerT.__call__(self, info, cdrdata, RTC.TimedDouble(RTC.Time(0,0),0))
    print "------------------------------"
    print "Listener:       ", self._name
    print "Profile::name:  ", info.name
    print "Profile::id:    ", info.id
    print "Data:           ", data.data
    print "------------------------------"



class ConnectorListener(OpenRTM_aist.ConnectorListener):
  def __init__(self, name):
    self._name = name

  def __del__(self):
    print "dtor of ", self._name

  def __call__(self, info):
    print "------------------------------"
    print "Listener:       ", self._name
    print "Profile::name:  ", info.name
    print "Profile::id:    ", info.id
    print "------------------------------"



class NaoValuesSender(OpenRTM_aist.DataFlowComponentBase):
  def __init__(self, manager):
    OpenRTM_aist.DataFlowComponentBase.__init__(self, manager)
    return

  def onInitialize(self):
    self.naoMotionProxy = ALProxy('ALMotion', NAO_IP, PORT)

    self._data = RTC.TimedDouble(RTC.Time(0,0),0)
    self._outport = OpenRTM_aist.OutPort("out", self._data)
    # Set OutPort buffer
    self.addOutPort("out", self._outport)
    self._outport.addConnectorDataListener(OpenRTM_aist.ConnectorDataListenerType.ON_BUFFER_WRITE, DataListener("ON_BUFFER_WRITE"))
    self._outport.addConnectorDataListener(OpenRTM_aist.ConnectorDataListenerType.ON_BUFFER_FULL, DataListener("ON_BUFFER_FULL"))
    self._outport.addConnectorDataListener(OpenRTM_aist.ConnectorDataListenerType.ON_BUFFER_WRITE_TIMEOUT, DataListener("ON_BUFFER_WRITE_TIMEOUT"))
    self._outport.addConnectorDataListener(OpenRTM_aist.ConnectorDataListenerType.ON_BUFFER_OVERWRITE, DataListener("ON_BUFFER_OVERWRITE"))
    self._outport.addConnectorDataListener(OpenRTM_aist.ConnectorDataListenerType.ON_BUFFER_READ, DataListener("ON_BUFFER_READ"))
    self._outport.addConnectorDataListener(OpenRTM_aist.ConnectorDataListenerType.ON_SEND, DataListener("ON_SEND"))
    self._outport.addConnectorDataListener(OpenRTM_aist.ConnectorDataListenerType.ON_RECEIVED, DataListener("ON_RECEIVED"))
    self._outport.addConnectorDataListener(OpenRTM_aist.ConnectorDataListenerType.ON_RECEIVER_FULL, DataListener("ON_RECEIVER_FULL"))
    self._outport.addConnectorDataListener(OpenRTM_aist.ConnectorDataListenerType.ON_RECEIVER_TIMEOUT, DataListener("ON_RECEIVER_TIMEOUT"))
    self._outport.addConnectorDataListener(OpenRTM_aist.ConnectorDataListenerType.ON_RECEIVER_ERROR, DataListener("ON_RECEIVER_ERROR"))

    self._outport.addConnectorListener(OpenRTM_aist.ConnectorListenerType.ON_CONNECT, ConnectorListener("ON_CONNECT"))
    self._outport.addConnectorListener(OpenRTM_aist.ConnectorListenerType.ON_DISCONNECT, ConnectorListener("ON_DISCONNECT"))

    return RTC.RTC_OK


  def onExecute(self, ec_id):
    print "Hit any key...",
    sys.stdin.readline()

    names  = "Body"
    useSensors  = True
    sensorAngles = self.naoMotionProxy.getAngles(names, useSensors)
    print "Sleep before sending data....\n"
    time.sleep(2)
    print "Go \n"

    #TODO: use TimedDoubleSeq data port type
    for i in range(0, len(sensorAngles)):
        time.sleep(0.5)
        self._data.data = sensorAngles[i]
        OpenRTM_aist.setTimestamp(self._data)
        print "Sending to subscriber: ", self._data.data
        self._outport.write()
        return RTC.RTC_OK # Hit any key... for all values
    return RTC.RTC_OK


def NaoValuesSenderInit(manager):
  profile = OpenRTM_aist.Properties(defaults_str=NaoValuesSender_spec)
  manager.registerFactory(profile,
                          NaoValuesSender,
                          OpenRTM_aist.Delete)


def MyModuleInit(manager):
  NaoValuesSenderInit(manager)

  # Create a component
  comp = manager.createComponent("NaoValuesSender")

def main():
  # Initialize manager
  mgr = OpenRTM_aist.Manager.init(sys.argv)

  # Set module initialization proceduer
  # This procedure will be invoked in activateManager() function.
  mgr.setModuleInitProc(MyModuleInit)

  # Activate manager and register to naming service
  mgr.activateManager()

  # run the manager in blocking mode
  # runManager(False) is the default
  mgr.runManager()

  # If you want to run the manager in non-blocking mode, do like this
  # mgr.runManager(True)

if __name__ == "__main__":
  main()
