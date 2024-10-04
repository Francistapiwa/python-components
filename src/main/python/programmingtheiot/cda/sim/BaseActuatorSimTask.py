#####
# 
# This class is part of the Programming the Internet of Things project.
# 
# It is provided as a simple shell to guide the student and assist with
# implementation for the Programming the Internet of Things exercises,
# and designed to be modified by the student as needed.
#

import logging
import programmingtheiot.common.ConfigConst as ConfigConst
from programmingtheiot.data.ActuatorData import ActuatorData

class BaseActuatorSimTask:
    """
    Shell representation of class for student implementation.
    """

    def __init__(self, name: str = ConfigConst.NOT_SET, typeID: int = ConfigConst.DEFAULT_ACTUATOR_TYPE, simpleName: str = "Actuator"):
        self.latestActuatorResponse = ActuatorData(typeID=typeID, name=name)
        self.latestActuatorResponse.setAsResponse()
        
        self.name = name
        self.typeID = typeID
        self.simpleName = simpleName
        self.lastKnownCommand = ConfigConst.DEFAULT_COMMAND
        self.lastKnownValue = ConfigConst.DEFAULT_VAL

    def getLatestActuatorResponse(self) -> ActuatorData:
        """
        This can return the current ActuatorData response instance or a copy.
        """
        return self.latestActuatorResponse  # Add logic to return a copy if necessary

    def getSimpleName(self) -> str:
        return self.simpleName  # Return the simple name

    def updateActuator(self, data: ActuatorData) -> ActuatorData:
        if data and self.typeID == data.getTypeID():
            statusCode = ConfigConst.DEFAULT_STATUS
            
            curCommand = data.getCommand()
            curVal     = data.getValue()
            
            # Check if the command or value is a repeat from previous
            # If so, ignore the command and return None to caller
            #
            # But - whether ON or OFF - allow a new value to be set
            if curCommand == self.lastKnownCommand and curVal == self.lastKnownValue:
                logging.debug(
                    "New actuator command and value is a repeat. Ignoring: %s %s",
                    str(curCommand), str(curVal))
            else:
                logging.debug(
                    "New actuator command and value to be applied: %s %s",
                    str(curCommand), str(curVal))
                
                if curCommand == ConfigConst.COMMAND_ON:
                    logging.info("Activating actuator...")
                    statusCode = self._activateActuator(val=data.getValue(), stateData=data.getStateData())
                elif curCommand == ConfigConst.COMMAND_OFF:
                    logging.info("Deactivating actuator...")
                    statusCode = self._deactivateActuator(val=data.getValue(), stateData=data.getStateData())
                else:
                    logging.warning("ActuatorData command is unknown. Ignoring: %s", str(curCommand))
                    statusCode = -1
                
                # Update the last known actuator command and value
                self.lastKnownCommand = curCommand
                self.lastKnownValue = curVal
                
                # Create the ActuatorData response from the original command
                actuatorResponse = ActuatorData()
                actuatorResponse.updateData(data)
                actuatorResponse.setStatusCode(statusCode)
                actuatorResponse.setAsResponse()
                
                self.latestActuatorResponse.updateData(actuatorResponse)
                
                return actuatorResponse
            
        return None
