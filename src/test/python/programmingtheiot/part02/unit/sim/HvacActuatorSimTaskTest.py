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
        ad.set_command(ConfigConst.COMMAND_ON)  # Correct method name
        ad.set_value(self.DEFAULT_VAL_A)  # Correct method name

        adr = self.hSimTask.updateActuator(ad)
        self.assertIsNotNone(adr)
        self.assertEqual(adr.get_value(), self.DEFAULT_VAL_A)  # Correct method name
        logging.info("ActuatorData: " + str(adr))

    # Additional tests can go here...

if __name__ == "__main__":
    unittest.main()

