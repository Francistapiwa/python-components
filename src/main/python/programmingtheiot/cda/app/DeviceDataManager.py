import logging
from programmingtheiot.cda.connection.CoapClientConnector import CoapClientConnector
from programmingtheiot.cda.connection.MqttClientConnector import MqttClientConnector
from programmingtheiot.cda.system.ActuatorAdapterManager import ActuatorAdapterManager
from programmingtheiot.cda.system.SensorAdapterManager import SensorAdapterManager
from programmingtheiot.cda.system.SystemPerformanceManager import SystemPerformanceManager
from programmingtheiot.common.IDataMessageListener import IDataMessageListener
from programmingtheiot.common.ResourceNameEnum import ResourceNameEnum
from programmingtheiot.data.ActuatorData import ActuatorData
from programmingtheiot.data.SensorData import SensorData
from programmingtheiot.data.SystemPerformanceData import SystemPerformanceData
from programmingtheiot.common.ConfigUtil import ConfigUtil
import programmingtheiot.common.ConfigConst as ConfigConst
from programmingtheiot.data.DataUtil import DataUtil  # Import DataUtil

class DeviceDataManager(IDataMessageListener):
    """
    Manages the data processing and actuation commands within the application.
    """

    def __init__(self):
        self.configUtil = ConfigUtil()
        
        self.enableSystemPerf = self.configUtil.getBoolean(
            section=ConfigConst.CONSTRAINED_DEVICE, 
            key=ConfigConst.ENABLE_SYSTEM_PERF_KEY)
        
        self.enableSensing = self.configUtil.getBoolean(
            section=ConfigConst.CONSTRAINED_DEVICE, 
            key=ConfigConst.ENABLE_SENSING_KEY)
        
        self.enableActuation = True  # Can be set based on config or other logic
        
        self.sysPerfMgr = None
        self.sensorAdapterMgr = None
        self.actuatorAdapterMgr = None

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
            key=ConfigConst.HANDLE_TEMP_CHANGE_ON_DEVICE_KEY)
        
        self.triggerHvacTempFloor = self.configUtil.getFloat(
            ConfigConst.CONSTRAINED_DEVICE, 
            key=ConfigConst.TRIGGER_HVAC_TEMP_FLOOR_KEY)
        
        self.triggerHvacTempCeiling = self.configUtil.getFloat(
            ConfigConst.CONSTRAINED_DEVICE, 
            key=ConfigConst.TRIGGER_HVAC_TEMP_CEILING_KEY)

        self.actuatorResponseCache = {}

    def getLatestActuatorDataResponseFromCache(self, name: str = None) -> ActuatorData:
        """Retrieves the named actuator data (response) item from the internal data cache."""
        return self.actuatorResponseCache.get(name)

    def getLatestSensorDataFromCache(self, name: str = None) -> SensorData:
        """Retrieves the named sensor data item from the internal data cache."""
        # Assuming there's a method to cache sensor data similarly
        pass

    def startManager(self):
        logging.info("Starting DeviceDataManager...")
        
        if self.sysPerfMgr:
            self.sysPerfMgr.startManager()
        
        if self.sensorAdapterMgr:
            self.sensorAdapterMgr.startManager()
        
        logging.info("Started DeviceDataManager.")

    def stopManager(self):
        logging.info("Stopping DeviceDataManager...")
        
        if self.sysPerfMgr:
            self.sysPerfMgr.stopManager()
        
        if self.sensorAdapterMgr:    
            self.sensorAdapterMgr.stopManager()
        
        logging.info("Stopped DeviceDataManager.")

    def handleActuatorCommandMessage(self, data: ActuatorData = None) -> ActuatorData:
        logging.info("Actuator command message received: %s", str(data))
        
        if data:
            logging.info("Processing actuator command message.")
            return self.actuatorAdapterMgr.sendActuatorCommand(data)
        else:
            logging.warning("Incoming actuator command is invalid (null). Ignoring.")
            return None 

    def handleActuatorCommandResponse(self, data: ActuatorData = None) -> bool:
        if data:
            logging.debug("Incoming actuator response received: %s", str(data))
            self.actuatorResponseCache[data.getName()] = data
            
            actuatorMsg = DataUtil().actuatorDataToJson(data)  # Using DataUtil
            resourceName = ResourceNameEnum.CDA_ACTUATOR_RESPONSE_RESOURCE
            
            self._handleUpstreamTransmission(resource=resourceName, msg=actuatorMsg)
            return True
        else:
            logging.warning("Incoming actuator response is invalid (null). Ignoring.")
            return False 

    def handleIncomingMessage(self, resourceEnum: ResourceNameEnum, msg: str) -> bool:
        logging.info("Incoming message received for resource: %s", str(resourceEnum))
        # Add logic to handle incoming message based on its resource type
        return True

    def handleSensorMessage(self, data: SensorData = None) -> bool:
        if data:
            logging.debug("Incoming sensor data received: %s", str(data))
            self._handleSensorDataAnalysis(data)
            return True
        else:
            logging.warning("Incoming sensor data is invalid (null). Ignoring.")
            return False 

    def handleSystemPerformanceMessage(self, data: SystemPerformanceData = None) -> bool:
        if data:
            logging.debug("Incoming system performance message received: %s", str(data))
            return True
        else:
            logging.warning("Incoming system performance data is invalid (null). Ignoring.")
            return False 

    def _handleSensorDataAnalysis(self, data: SensorData):
        logging.debug("Analyzing sensor data: %s", str(data))
        if self.handleTempChangeOnDevice and data.getTypeID() == ConfigConst.TEMP_SENSOR_TYPE:
            logging.info("Handling temperature change: %s - type ID: %s", str(data.getValue()), str(data.getTypeID()))
            ad = ActuatorData(typeID=ConfigConst.HVAC_ACTUATOR_TYPE)
            
            if data.getValue() > self.triggerHvacTempCeiling:
                ad.setCommand(ConfigConst.COMMAND_ON)
                ad.setValue(self.triggerHvacTempCeiling)
            elif data.getValue() < self.triggerHvacTempFloor:
                ad.setCommand(ConfigConst.COMMAND_ON)
                ad.setValue(self.triggerHvacTempFloor)
            else:
                ad.setCommand(ConfigConst.COMMAND_OFF)

            self.handleActuatorCommandMessage(ad)

    def _handleUpstreamTransmission(self, resourceName: ResourceNameEnum, msg: str):
        logging.debug("Preparing to transmit upstream: %s", str(resourceName))
        # Logic for upstream transmission here
        pass


