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
import programmingtheiot.common.ConfigConst as ConfigConst
from programmingtheiot.data.ActuatorData import ActuatorData
from programmingtheiot.cda.sim.HumidifierActuatorSimTask import HumidifierActuatorSimTask

class TestHumidifierActuatorSimTask(unittest.TestCase):
    DEFAULT_VAL_A = 18.2
    DEFAULT_VAL_B = 21.4
    
    @classmethod
    def setUpClass(cls):
        logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s', level=logging.DEBUG)
        logging.info("Testing HumidifierActuatorSimTask class...")
        cls.hSimTask = HumidifierActuatorSimTask()

    def test_update_actuator(self):
        ad = ActuatorData(typeID=ConfigConst.HUMIDIFIER_ACTUATOR_TYPE)
        ad.setCommand(ConfigConst.COMMAND_ON)
        ad.setValue(self.DEFAULT_VAL_A)

        adr = self.hSimTask.updateActuator(ad)
        self.assertIsNotNone(adr)
        self.assertEqual(adr.getValue(), self.DEFAULT_VAL_A)
        logging.info("ActuatorData: " + str(adr))

    # Additional tests can go here...

if __name__ == "__main__":
    unittest.main()
