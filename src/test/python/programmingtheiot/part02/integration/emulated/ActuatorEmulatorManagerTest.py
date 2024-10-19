#####
# 
# This class is part of the Programming the Internet of Things
# project, and is available via the MIT License, which can be
# found in the LICENSE file at the top level of this repository.
# 
# Copyright (c) 2020 by Andrew D. King
# 

import logging
import unittest

from time import sleep

import programmingtheiot.common.ConfigConst as ConfigConst

from programmingtheiot.cda.system.ActuatorAdapterManager import ActuatorAdapterManager
from programmingtheiot.common.DefaultDataMessageListener import DefaultDataMessageListener
from programmingtheiot.data.ActuatorData import ActuatorData

class ActuatorEmulatorManagerTest(unittest.TestCase):
    """
    This test case class contains very basic unit tests for
    ActuatorAdapterManager. It should not be considered complete,
    but serve as a starting point for the student implementing
    additional functionality within their Programming the IoT
    environment.
    
    NOTE: This test requires the sense_emu_gui to be running
    and must have access to the underlying libraries that
    support the pisense module. On Windows, one way to do
    this is by installing pisense and sense-emu within the
    Bash on Ubuntu on Windows environment and then execute this
    test case from the command line, as it will likely fail
    if run within an IDE in native Windows.
    """
    
    @classmethod
    def setUpClass(cls):
        logging.basicConfig(format='%(asctime)s:%(module)s:%(levelname)s:%(message)s', level=logging.DEBUG)
        logging.info("Testing ActuatorAdapterManager class [using SenseHAT emulator]...")
        
        cls.defaultMsgListener = DefaultDataMessageListener()
        cls.actuatorAdapterMgr = ActuatorAdapterManager()
        cls.actuatorAdapterMgr.setDataMessageListener(cls.defaultMsgListener)
        
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testHumidifierEmulation(self):
        ad = ActuatorData(typeID=ConfigConst.HUMIDIFIER_ACTUATOR_TYPE)
        ad.set_value(50.0)  # Updated method name
        
        ad.set_command(ConfigConst.COMMAND_ON)  # Updated method name
        self.actuatorAdapterMgr.sendActuatorCommand(ad)
        
        ad.set_command(ConfigConst.COMMAND_OFF)  # Updated method name
        self.actuatorAdapterMgr.sendActuatorCommand(ad)

    def testHvacEmulation(self):
        ad = ActuatorData(typeID=ConfigConst.HVAC_ACTUATOR_TYPE)
        ad.set_value(22.5)  # Updated method name
        
        ad.set_command(ConfigConst.COMMAND_ON)  # Updated method name
        self.actuatorAdapterMgr.sendActuatorCommand(ad)
        
        ad.set_command(ConfigConst.COMMAND_OFF)  # Updated method name
        self.actuatorAdapterMgr.sendActuatorCommand(ad)

    def testLedDisplayEmulation(self):
        ad = ActuatorData(typeID=ConfigConst.LED_DISPLAY_ACTUATOR_TYPE)
        ad.set_command(ConfigConst.COMMAND_ON)  # Updated method name
        ad.set_state_data("What's up?")  # Updated method name
        self.actuatorAdapterMgr.sendActuatorCommand(ad)
        
        ad.set_command(ConfigConst.COMMAND_OFF)  # Updated method name
        self.actuatorAdapterMgr.sendActuatorCommand(ad)

if __name__ == "__main__":
    unittest.main()
	