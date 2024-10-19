import logging
import unittest
import programmingtheiot.common.ConfigConst as ConfigConst
from programmingtheiot.data.SensorData import SensorData

class SensorDataTest(unittest.TestCase):
    DEFAULT_NAME = "SensorDataFooBar"
    MIN_VALUE = 10.0

    @classmethod
    def setUpClass(cls):
        logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s', level=logging.DEBUG)
        logging.info("Testing SensorData class...")
        
    def testDefaultValues(self):
        sd = SensorData()
        
        self.assertEqual(sd.getName(), ConfigConst.NOT_SET)  # Check the default name
        self.assertEqual(sd.get_value(), ConfigConst.DEFAULT_VAL)  # Check the default value
        
        logging.info("Sensor data as string: " + str(sd))

    def testParameterUpdates(self):
        sd = self._createTestSensorData()
        
        self.assertEqual(sd.getName(), self.DEFAULT_NAME)  # Check the name
        self.assertEqual(sd.get_value(), self.MIN_VALUE)  # Check the value

    def testFullUpdate(self):
        sd = SensorData()
        sd2 = self._createTestSensorData()
        
        sd._handle_update_data(sd2)  # Update sd with sd2
        
        self.assertEqual(sd.getName(), self.DEFAULT_NAME)  # Check updated name
        self.assertEqual(sd.get_value(), self.MIN_VALUE)  # Check updated value
    
    def _createTestSensorData(self):
        sd = SensorData()
        
        sd.setName(self.DEFAULT_NAME)  # Set the name
        sd.set_value(self.MIN_VALUE)  # Set the value
        
        logging.info("Sensor data as string: " + str(sd))
        
        return sd

if __name__ == "__main__":
    unittest.main()
