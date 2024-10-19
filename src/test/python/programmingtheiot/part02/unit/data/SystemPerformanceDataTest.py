import logging
import unittest
from programmingtheiot.cda.system.ActuatorAdapterManager import ActuatorAdapterManager
from programmingtheiot.data.ActuatorData import ActuatorData
import programmingtheiot.common.ConfigConst as ConfigConst

class ActuatorAdapterManagerTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s', level=logging.DEBUG)
        logging.info("Testing ActuatorAdapterManager class...")
        cls.actuatorAdapterMgr = ActuatorAdapterManager()

    def testHumidifierOn(self):
        # Create an ActuatorData object for turning on the humidifier
        data = ActuatorData()
        data.setLocationID(self.actuatorAdapterMgr.locationID)
        data.setTypeID(ConfigConst.HUMIDIFIER_ACTUATOR_TYPE)
        data.setValue(1)  # Assuming setValue sets the state of the actuator to 'on'

        response = self.actuatorAdapterMgr.sendActuatorCommand(data)
        self.assertIsNotNone(response)

    def testHumidifierOff(self):
        # Create an ActuatorData object for turning off the humidifier
        data = ActuatorData()
        data.setLocationID(self.actuatorAdapterMgr.locationID)
        data.setTypeID(ConfigConst.HUMIDIFIER_ACTUATOR_TYPE)
        data.setValue(0)  # Assuming setValue sets the state of the actuator to 'off'

        response = self.actuatorAdapterMgr.sendActuatorCommand(data)
        self.assertIsNotNone(response)

if __name__ == "__main__":
    unittest.main()





