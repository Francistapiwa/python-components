import logging
import os
import unittest
import json

import programmingtheiot.common.ConfigConst as ConfigConst

from pathlib import Path

from programmingtheiot.common.ConfigUtil import ConfigUtil
from programmingtheiot.data.DataUtil import DataUtil

from programmingtheiot.data.ActuatorData import ActuatorData
from programmingtheiot.data.SensorData import SensorData
from programmingtheiot.data.SystemPerformanceData import SystemPerformanceData

class DataIntegrationTest(unittest.TestCase):
    """
    This test case class contains basic integration tests for
    DataUtil and data container classes for use between the CDA and
    GDA to verify JSON compatibility.
    """
    
    @classmethod
    def setUpClass(cls):
        logging.basicConfig(format='%(asctime)s:%(module)s:%(levelname)s:%(message)s', level=logging.DEBUG)
        logging.info("Running DataIntegrationTest test cases...")
        
        encodeToUtf8 = False
        
        cls.dataUtil = DataUtil(encodeToUtf8)

        cls.cdaDataPath = ConfigUtil().getProperty(ConfigConst.CONSTRAINED_DEVICE, ConfigConst.TEST_CDA_DATA_PATH_KEY)
        cls.gdaDataPath = ConfigUtil().getProperty(ConfigConst.CONSTRAINED_DEVICE, ConfigConst.TEST_GDA_DATA_PATH_KEY)

        # Check if paths were retrieved successfully
        if cls.cdaDataPath is None or cls.gdaDataPath is None:
            logging.error("One or more configuration paths are missing.")
            raise RuntimeError("Configuration paths not found. Ensure PiotConfig.props exists and is valid.")
        
        # Create CDA and GDA data paths
        for path in [cls.cdaDataPath, cls.gdaDataPath]:
            if not os.path.exists(path):
                logging.info("Creating data path: " + path)
                os.makedirs(path, exist_ok=True)
        
        # Create sample data for GDA
        cls.create_sample_data_for_gda()

    @classmethod
    def create_sample_data_for_gda(cls):
        actuator_data = {
            "timeStamp": "2020-09-07 23:56:35.480928",
            "name": "Not Set",
            "hasError": False,
            "statusCode": 0,
            "isResponse": False,
            "actuatorType": 0,
            "command": 0,
            "stateData": None,
            "curValue": 0.0
        }

        sensor_data = {
            "timeStamp": "2020-09-07 23:56:35.486912",
            "name": "Not Set",
            "hasError": False,
            "statusCode": 0,
            "curValue": 0.0,
            "sensorType": 0
        }

        system_performance_data = {
            "timeStamp": "2020-09-07 23:56:35.491898",
            "name": "Not Set",
            "hasError": False,
            "statusCode": 0,
            "cpuUtil": 0.0,
            "diskUtil": 0.0,
            "memUtil": 0.0
        }

        # Write sample data to GDA files
        with open(os.path.join(cls.gdaDataPath, 'ActuatorData.dat'), 'w') as f:
            json.dump(actuator_data, f)

        with open(os.path.join(cls.gdaDataPath, 'SensorData.dat'), 'w') as f:
            json.dump(sensor_data, f)

        with open(os.path.join(cls.gdaDataPath, 'SystemPerformanceData.dat'), 'w') as f:
            json.dump(system_performance_data, f)

    def setUp(self):
        logging.info("================================================")
        logging.info("DataIntegrationTest test execution...")
        logging.info("================================================")
        
        pass

    def tearDown(self):
        pass

    def testWriteActuatorDataToCdaDataPath(self):
        logging.info("\n\n----- [ActuatorData to JSON to file] -----")
        
        dataObj = ActuatorData()
        dataStr = self.dataUtil.actuatorDataToJson(dataObj)
        fileName = os.path.join(self.cdaDataPath, 'ActuatorData.dat')

        logging.info("Sample ActuatorData JSON (validated): " + str(dataStr))
        logging.info("Writing ActuatorData JSON to CDA data path: " + fileName)
        
        fileRef = Path(fileName)
        fileRef.write_text(dataStr, encoding='utf-8')

    def testWriteSensorDataToCdaDataPath(self):
        logging.info("\n\n----- [SensorData to JSON to file] -----")
        
        dataObj = SensorData()
        dataStr = self.dataUtil.sensorDataToJson(dataObj)
        fileName = os.path.join(self.cdaDataPath, 'SensorData.dat')

        logging.info("Sample SensorData JSON (validated): " + str(dataStr))
        logging.info("Writing SensorData JSON to CDA data path: " + fileName)
        
        fileRef = Path(fileName)
        fileRef.write_text(dataStr, encoding='utf-8')

    def testWriteSystemPerformanceDataToCdaDataPath(self):
        logging.info("\n\n----- [SystemPerformanceData to JSON to file] -----")
        
        dataObj = SystemPerformanceData()
        dataStr = self.dataUtil.systemPerformanceDataToJson(dataObj)
        fileName = os.path.join(self.cdaDataPath, 'SystemPerformanceData.dat')

        logging.info("Sample SystemPerformanceData JSON (validated): " + str(dataStr))
        logging.info("Writing SystemPerformanceData JSON to CDA data path: " + fileName)
        
        fileRef = Path(fileName)
        fileRef.write_text(dataStr, encoding='utf-8')

    def testReadActuatorDataFromGdaDataPath(self):
        logging.info("\n\n----- [ActuatorData JSON from file to object] -----")
        
        fileName = os.path.join(self.gdaDataPath, 'ActuatorData.dat')
        fileRef = Path(fileName)
        dataStr = fileRef.read_text(encoding='utf-8')

        dataObj = self.dataUtil.jsonToActuatorData(dataStr)

        logging.info("ActuatorData JSON from GDA: " + dataStr)
        logging.info("ActuatorData object: " + str(dataObj))

    def testReadSensorDataFromGdaDataPath(self):
        logging.info("\n\n----- [SensorData JSON from file to object] -----")
        
        fileName = os.path.join(self.gdaDataPath, 'SensorData.dat')
        fileRef = Path(fileName)
        dataStr = fileRef.read_text(encoding='utf-8')

        dataObj = self.dataUtil.jsonToSensorData(dataStr)

        logging.info("SensorData JSON from GDA: " + dataStr)
        logging.info("SensorData object: " + str(dataObj))

    def testReadSystemPerformanceDataFromGdaDataPath(self):
        logging.info("\n\n----- [SystemPerformanceData JSON from file to object] -----")
        
        fileName = os.path.join(self.gdaDataPath, 'SystemPerformanceData.dat')
        fileRef = Path(fileName)
        dataStr = fileRef.read_text(encoding='utf-8')

        dataObj = self.dataUtil.jsonToSystemPerformanceData(dataStr)

        logging.info("SystemPerformanceData JSON from GDA: " + dataStr)
        logging.info("SystemPerformanceData object: " + str(dataObj))

if __name__ == "__main__":
    unittest.main()
