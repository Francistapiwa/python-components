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
from programmingtheiot.cda.system.ActuatorAdapterManager import ActuatorAdapterManager
from programmingtheiot.data.ActuatorData import ActuatorData
import programmingtheiot.common.ConfigConst as ConfigConst

class ActuatorAdapterManagerTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        logging.basicConfig(format='%(asctime)s:%(module)s:%(levelname)s:%(message)s', level=logging.DEBUG)
        logging.info("Testing ActuatorAdapterManager class...")
        cls.actuatorAdapterMgr = ActuatorAdapterManager()

    def testHumidifierOn(self):
        data = ActuatorData()
        data.setLocationID(self.actuatorAdapterMgr.locationID)
        data.setTypeID(ConfigConst.HUMIDIFIER_ACTUATOR_TYPE)
        data.setValue(1)  # Assume 1 means ON

        response = self.actuatorAdapterMgr.sendActuatorCommand(data)
        self.assertIsNotNone(response)

    def testHumidifierOff(self):
        data = ActuatorData()
        data.setLocationID(self.actuatorAdapterMgr.locationID)
        data.setTypeID(ConfigConst.HUMIDIFIER_ACTUATOR_TYPE)
        data.setValue(0)  # Assume 0 means OFF

        response = self.actuatorAdapterMgr.sendActuatorCommand(data)
        self.assertIsNotNone(response)

    def testHvacOn(self):
        data = ActuatorData()
        data.setLocationID(self.actuatorAdapterMgr.locationID)
        data.setTypeID(ConfigConst.HVAC_ACTUATOR_TYPE)
        data.setValue(1)  # Assume 1 means ON

        response = self.actuatorAdapterMgr.sendActuatorCommand(data)
        self.assertIsNotNone(response)

    def testHvacOff(self):
        data = ActuatorData()
        data.setLocationID(self.actuatorAdapterMgr.locationID)
        data.setTypeID(ConfigConst.HVAC_ACTUATOR_TYPE)
        data.setValue(0)  # Assume 0 means OFF

        response = self.actuatorAdapterMgr.sendActuatorCommand(data)
        self.assertIsNotNone(response)

if __name__ == "__main__":
    unittest.main()
	