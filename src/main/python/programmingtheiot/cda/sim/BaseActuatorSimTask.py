import logging
import programmingtheiot.common.ConfigConst as ConfigConst
from programmingtheiot.data.ActuatorData import ActuatorData

class BaseActuatorSimTask:
    """
    Shell representation of class for student implementation.
    """

    def __init__(self, name: str = ConfigConst.NOT_SET, typeID: int = ConfigConst.DEFAULT_ACTUATOR_TYPE, simpleName: str = "Actuator"):
        # Initialize actuator response
        self.latestActuatorResponse = ActuatorData(typeID=typeID, name=name)
        self.latestActuatorResponse.set_as_response()
        
        # Set class-scoped variables
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

    def _activateActuator(self, val: float = ConfigConst.DEFAULT_VAL, stateData: str = None) -> int:
        msg = "\n*******"
        msg += "\n* O N *"
        msg += "\n*******"
        msg += f"\n{self.name} VALUE -> {val}\n======="
        
        logging.info("Simulating %s actuator ON: %s", self.name, msg)
        
        return 0

    def _deactivateActuator(self, val: float = ConfigConst.DEFAULT_VAL, stateData: str = None) -> int:
        msg = "\n*******"
        msg += "\n* OFF *"
        msg += "\n*******"
        
        logging.info("Simulating %s actuator OFF: %s", self.name, msg)
        
        return 0

    def updateActuator(self, data: ActuatorData) -> ActuatorData:
        if data and self.typeID == data.getTypeID():  # Use getTypeID()
            statusCode = ConfigConst.DEFAULT_STATUS
            
            curCommand = data.get_command()  # Use get_command()
            curVal = data.get_value()  # Use get_value()
            
            # Check if the command or value is a repeat from previous
            if curCommand == self.lastKnownCommand and curVal == self.lastKnownValue:
                logging.debug(
                    "New actuator command and value is a repeat. Ignoring: %s %s",
                    str(curCommand), str(curVal))
                return None
            
            logging.debug(
                "New actuator command and value to be applied: %s %s",
                str(curCommand), str(curVal))
                
            if curCommand == ConfigConst.COMMAND_ON:
                logging.info("Activating actuator...")
                statusCode = self._activateActuator(val=curVal, stateData=data.get_state_data())
            elif curCommand == ConfigConst.COMMAND_OFF:
                logging.info("Deactivating actuator...")
                statusCode = self._deactivateActuator(val=curVal, stateData=data.get_state_data())
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
            actuatorResponse.set_as_response()
            
            self.latestActuatorResponse.updateData(actuatorResponse)
            
            return actuatorResponse
            
        return None



