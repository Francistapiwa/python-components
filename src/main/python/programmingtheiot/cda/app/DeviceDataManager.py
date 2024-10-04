#####
# 
# This class is part of the Programming the Internet of Things project.
# 
# It is provided as a simple shell to guide the student and assist with
# implementation for the Programming the Internet of Things exercises,
# and designed to be modified by the student as needed.
#

import logging

from programmingtheiot.cda.connection.CoapClientConnector import CoapClientConnector
from programmingtheiot.cda.connection.MqttClientConnector import MqttClientConnector

from programmingtheiot.cda.system.ActuatorAdapterManager import ActuatorAdapterManager
from programmingtheiot.cda.system.SensorAdapterManager import SensorAdapterManager
from programmingtheiot.cda.system.SystemPerformanceManager import SystemPerformanceManager

from programmingtheiot.common.IDataMessageListener import IDataMessageListener
from programmingtheiot.common.ISystemPerformanceDataListener import ISystemPerformanceDataListener
from programmingtheiot.common.ITelemetryDataListener import ITelemetryDataListener
from programmingtheiot.common.ResourceNameEnum import ResourceNameEnum

from programmingtheiot.data.ActuatorData import ActuatorData
from programmingtheiot.data.SensorData import SensorData
from programmingtheiot.data.SystemPerformanceData import SystemPerformanceData
from programmingtheiot.common.ConfigUtil import ConfigUtil
import programmingtheiot.common.ConfigConst as ConfigConst

class DeviceDataManager(IDataMessageListener):
    """
    Shell representation of class for student implementation.
    """

    def __init__(self):
        self.configUtil = ConfigUtil()
        
        self.enableSystemPerf = self.configUtil.getBoolean(
            section=ConfigConst.CONSTRAINED_DEVICE, 
            key=ConfigConst.ENABLE_SYSTEM_PERF_KEY)
        
        self.enableSensing = self.configUtil.getBoolean(
            section=ConfigConst.CONSTRAINED_DEVICE, 
            key=ConfigConst.ENABLE_SENSING_KEY)
        
        self.enableActuation = True  # This can be set based on config or other logic
        
        self.sysPerfMgr = None
        self.sensorAdapterMgr = None
        self.actuatorAdapterMgr = None

        # Initialize managers based on configuration
        if self.enableSystemPerf:
            self.sysPerfMgr = SystemPerformanceManager()
            self.sysPerfMgr.setDataMessageListener(self)
            logging.info("Local system performance tracking enabled")
        
        if self.enableSensing:
            self.sensorAdapterMgr = SensorAdapterManager()
            self.sensorAdapterMgr.setDataMessageListener(self)
            logging.info("Local sensor tracking enabled")
        
        if self.enableActuation:
            self.actuatorAdapterMgr = ActuatorAdapterManager(dataMsgListener=self)
            logging.info("Local actuation capabilities enabled")

        self.handleTempChangeOnDevice = self.configUtil.getBoolean(
            ConfigConst.CONSTRAINED_DEVICE, 
            ConfigConst.HANDLE_TEMP_CHANGE_ON_DEVICE_KEY)
        
        self.triggerHvacTempFloor = self.configUtil.getFloat(
            ConfigConst.CONSTRAINED_DEVICE, 
            ConfigConst.TRIGGER_HVAC_TEMP_FLOOR_KEY)
        
        self.triggerHvacTempCeiling = self.configUtil.getFloat(
            ConfigConst.CONSTRAINED_DEVICE, 
            ConfigConst.TRIGGER_HVAC_TEMP_CEILING_KEY)

        self.actuatorResponseCache = {}

    def getLatestActuatorDataResponseFromCache(self, name: str = None) -> ActuatorData:
        """Retrieves the named actuator data (response) item from the internal data cache."""
        return self.actuatorResponseCache.get(name)

    def getLatestSensorDataFromCache(self, name: str = None) -> SensorData:
        """Retrieves the named sensor data item from the internal data cache."""
     
