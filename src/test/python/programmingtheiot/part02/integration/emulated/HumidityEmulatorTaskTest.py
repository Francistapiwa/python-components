import logging
import unittest
from time import sleep

import programmingtheiot.common.ConfigConst as ConfigConst
from programmingtheiot.data.SensorData import SensorData
from programmingtheiot.cda.emulated.HumiditySensorEmulatorTask import HumiditySensorEmulatorTask

class HumidityEmulatorTaskTest(unittest.TestCase):
    """
    Test case for the HumidityEmulatorTask class.
    """
    
    @classmethod
    def setUpClass(cls):
        logging.basicConfig(format='%(asctime)s:%(module)s:%(levelname)s:%(message)s', level=logging.DEBUG)
        logging.info("Testing HumidityEmulatorTask class [using SenseHAT emulator]...")
        cls.hEmuTask = HumiditySensorEmulatorTask()
        
    def testReadEmulator(self):
        sd1 = self.hEmuTask.generateTelemetry()
        
        if sd1:
            self.assertEqual(sd1.getTypeID(), ConfigConst.HUMIDITY_SENSOR_TYPE)
            logging.info("SensorData: %f - %s", sd1.get_value(), str(sd1))
            sleep(5)
        else:
            logging.warning("FAIL: SensorData is None.")
            
        sd2 = self.hEmuTask.generateTelemetry()
        
        if sd2:
            self.assertEqual(sd2.getTypeID(), ConfigConst.HUMIDITY_SENSOR_TYPE)
            logging.info("SensorData: %f - %s", sd2.get_value(), str(sd2))
            sleep(5)
        else:
            logging.warning("FAIL: SensorData is None.")

if __name__ == "__main__":
    unittest.main()
