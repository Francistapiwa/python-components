import logging
import unittest
import programmingtheiot.common.ConfigConst as ConfigConst
from programmingtheiot.data.ActuatorData import ActuatorData

class ActuatorDataTest(unittest.TestCase):
    DEFAULT_NAME = "ActuatorDataFooBar"
    DEFAULT_STATE_DATA = "{state: None}"
    DEFAULT_VALUE = 15.2
    
    @classmethod
    def setUpClass(cls):
        logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s', level=logging.DEBUG)
        logging.info("Testing ActuatorData class...")

    def testDefaultValues(self):
        ad = ActuatorData()
        
        self.assertEqual(ad.get_command(), ConfigConst.DEFAULT_COMMAND)  # Check default command
        self.assertEqual(ad.getStatusCode(), ConfigConst.DEFAULT_STATUS)  # Corrected method name
        
        logging.info("Actuator data as string: " + str(ad))

    def testParameterUpdates(self):
        ad = self._createTestActuatorData()
        
        self.assertEqual(ad.getName(), self.DEFAULT_NAME)  # Ensure name is set
        self.assertEqual(ad.get_command(), ConfigConst.COMMAND_ON)  # Ensure command is set
        self.assertEqual(ad.get_state_data(), self.DEFAULT_STATE_DATA)  # Ensure state data is set
        self.assertEqual(ad.get_value(), self.DEFAULT_VALUE)  # Ensure value is set

    def testFullUpdate(self):
        ad = ActuatorData()
        ad2 = self._createTestActuatorData()
        
        ad.updateData(ad2)  # Ensure this matches your update method
        
        self.assertEqual(ad.get_command(), ConfigConst.COMMAND_ON)  # Ensure command is updated
        self.assertEqual(ad.get_state_data(), self.DEFAULT_STATE_DATA)  # Ensure state data is updated
        self.assertEqual(ad.get_value(), self.DEFAULT_VALUE)  # Ensure value is updated

    def _createTestActuatorData(self):
        ad = ActuatorData()
        
        ad.setName(self.DEFAULT_NAME)  # Set the name
        ad.set_command(ConfigConst.COMMAND_ON)  # Set command to COMMAND_ON
        ad.set_state_data(self.DEFAULT_STATE_DATA)  # Set state data
        ad.set_value(self.DEFAULT_VALUE)  # Set value

        logging.info("Actuator data as string: " + str(ad))
        
        return ad

if __name__ == "__main__":
    unittest.main()



