import programmingtheiot.common.ConfigConst as ConfigConst
from programmingtheiot.data.BaseIotData import BaseIotData

class SensorData(BaseIotData):
    """
    Represents simple sensor data with support for float values.
    """

    def __init__(self, typeID: int = ConfigConst.DEFAULT_SENSOR_TYPE, name=ConfigConst.NOT_SET, d=None):
        super(SensorData, self).__init__(name=name, typeID=typeID, d=d)
        self.value = ConfigConst.DEFAULT_VAL  # Initialize the value with a default

    def get_value(self) -> float:
        """Return the current value of the sensor."""
        return self.value

    def set_value(self, new_val: float):
        """Set a new value for the sensor and update the timestamp."""
        if isinstance(new_val, (int, float)):  # Check if the value is a number
            self.value = new_val
            self.updateTimeStamp()  # Update the timestamp when the value changes
        else:
            raise ValueError("New value must be a number.")

    def _handle_update_data(self, data):
        """Update the sensor data from another SensorData instance."""
        if data and isinstance(data, SensorData):
            self.value = data.get_value()  # Update the value
            self.setName(data.getName())  # Update the name
            self.updateTimeStamp()  # Update the timestamp when data is updated
