import programmingtheiot.common.ConfigConst as ConfigConst
from programmingtheiot.data.BaseIotData import BaseIotData

class ActuatorData(BaseIotData):
    """
    Represents data for an actuator, including its command, state, and response status.
    """

    def __init__(self, typeID: int = ConfigConst.DEFAULT_ACTUATOR_TYPE, name=ConfigConst.NOT_SET, d=None):
        super(ActuatorData, self).__init__(name=name, typeID=typeID, d=d)
        self.value = ConfigConst.DEFAULT_VAL
        self.command = ConfigConst.DEFAULT_COMMAND  # Ensure this is correct
        self.state_data = ""
        self.is_response = False

    def get_command(self) -> int:
        return self.command

    def get_state_data(self) -> str:
        return self.state_data

    def get_value(self) -> float:
        return self.value

    def is_response_flag_enabled(self) -> bool:
        return self.is_response

    def set_command(self, command: int):
        self.command = command
        self.updateTimeStamp()

    def set_as_response(self):
        self.is_response = True
        self.updateTimeStamp()

    def set_state_data(self, state_data: str):
        if state_data:
            self.state_data = state_data
            self.updateTimeStamp()

    def set_value(self, val: float):
        self.value = val
        self.updateTimeStamp()

    def updateData(self, data):
        if data and isinstance(data, ActuatorData):
            self.command = data.get_command()
            self.state_data = data.get_state_data()
            self.value = data.get_value()
            self.is_response = data.is_response_flag_enabled()
