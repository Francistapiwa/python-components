#####
# 
# This class is part of the Programming the Internet of Things project.
# 
# It is provided as a simple shell to guide the student and assist with
# implementation for the Programming the Internet of Things exercises,
# and designed to be modified by the student as needed.
#
import logging
from programmingtheiot.data.SensorData import SensorData
from programmingtheiot.cda.sim.BaseSensorSimTask import BaseSensorSimTask
import programmingtheiot.common.ConfigConst as ConfigConst

class HumiditySensorEmulatorTask(BaseSensorSimTask):
    def __init__(self):
        super(HumiditySensorEmulatorTask, self).__init__(
            name=ConfigConst.HUMIDITY_SENSOR_NAME,
            typeID=ConfigConst.HUMIDITY_SENSOR_TYPE
        )

    def generateTelemetry(self):
        sensorData = SensorData()
        try:
            sensorVal = self.get_humidity()  # Replace with your method to get humidity
            sensorData.set_value(sensorVal)  # Use set_value instead of setValue
            sensorData.setTypeID(ConfigConst.HUMIDITY_SENSOR_TYPE)
        except Exception as e:
            logging.error(f"Error retrieving humidity: {e}")
            sensorData.set_value(0)  # Use set_value here as well

        return sensorData

    def get_humidity(self):
        return 50.0  # Replace with actual logic to get humidity
