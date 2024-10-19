import logging
import unittest
import programmingtheiot.common.ConfigConst as ConfigConst
from programmingtheiot.data.ActuatorData import ActuatorData
from programmingtheiot.cda.sim.HumidifierActuatorSimTask import HumidifierActuatorSimTask

class HumidifierActuatorSimTaskTest(unittest.TestCase):
    """
    This test case class contains very basic unit tests for
    HumidifierActuatorSimTask. It should not be considered complete,
    but serve as a starting point for the student implementing
    additional functionality within their Programming the IoT
    environment.
    """
    DEFAULT_VAL_A = 18.2
    DEFAULT_VAL_B = 21.4
    
    @classmethod
    def setUpClass(cls):
        logging.basicConfig(format='%(asctime)s:%(module)s:%(levelname)s:%(message)s', level=logging.DEBUG)
        logging.info("Testing HumidifierActuatorSimTask class...")
        cls.hSimTask = HumidifierActuatorSimTask()
        
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_update_actuator(self):
        ad = ActuatorData(typeID=ConfigConst.HUMIDIFIER_ACTUATOR_TYPE)
        ad.set_command(ConfigConst.COMMAND_ON)  # Changed from setCommand to set_command
 

