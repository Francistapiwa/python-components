#####
# 
# This class is part of the Programming the Internet of Things project.
# 
# It is provided as a simple shell to guide the student and assist with
# implementation for the Programming the Internet of Things exercises,
# and designed to be modified by the student as needed.
#

import logging
from importlib import import_module
import programmingtheiot.common.ConfigConst as ConfigConst
from programmingtheiot.common.ConfigUtil import ConfigUtil
from programmingtheiot.common.IDataMessageListener import IDataMessageListener
from programmingtheiot.data.ActuatorData import ActuatorData
from programmingtheiot.cda.sim.HvacActuatorSimTask import HvacActuatorSimTask
from programmingtheiot.cda.sim.HumidifierActuatorSimTask import HumidifierActuatorSimTask

class ActuatorAdapterManager(object):
    """
    Shell representation of class for student implementation.
    """
    
    def __init__(self, dataMsgListener: IDataMessageListener = None):
        self.dataMsgListener = dataMsgListener
        
        self.configUtil = ConfigUtil()
        
        self.useSimulator = self.configUtil.getBoolean(
            section=ConfigConst.CONSTRAINED_DEVICE, 
            key=ConfigConst.ENABLE_SIMULATOR_KEY
        )
        self.useEmulator = self.configUtil.getBoolean(
            section=ConfigConst.CONSTRAINED_DEVICE, 
            key=ConfigConst.ENABLE_EMULATOR_KEY
        )
        self.deviceID = self.configUtil.getProperty(
            section=ConfigConst.CONSTRAINED_DEVICE, 
            key=ConfigConst.DEVICE_LOCATION_ID_KEY, 
            defaultVal=ConfigConst.NOT_SET
        )
        self.locationID = self.configUtil.getProperty(
            section=ConfigConst.CONSTRAINED_DEVICE, 
            key=ConfigConst.DEVICE_LOCATION_ID_KEY, 
            defaultVal=ConfigConst.NOT_SET
        )
        
        # Initialize the humidifier actuator
        self.humidifi = HumidifierActuatorSimTask(deviceID=self.deviceID)
        
        # Initialize any other necessary actuators if needed
        self.hvacActuator = HvacActuatorSimTask(deviceID=self.deviceID)
        
        # Add logging for initialization
        logging.info("ActuatorAdapterManager initialized with deviceID: %s", self.deviceID)

    def processActuatorCommand(self, actuatorData: ActuatorData):
        """Process an actuator command."""
        # Example command handling
        if actuatorData.typeID == 1:  # Humidifier
            self.humidifi.activate(actuatorData)
            logging.info("Activated humidifier with data: %s", actuatorData)
        elif actuatorData.typeID == 2:  # HVAC
            self.hvacActuator.activate(actuatorData)
            logging.info("Activated HVAC with data: %s", actuatorData)
        else:
            logging.warning("Unknown actuator type ID: %d", actuatorData.typeID)
