import logging
import random
import programmingtheiot.common.ConfigConst as ConfigConst
from programmingtheiot.data.SensorData import SensorData
from programmingtheiot.cda.sim.SensorDataGenerator import SensorDataSet

class BaseSensorSimTask:
    """
    Base class for simulating sensor behavior. This class handles
    random value generation and data retrieval from a dataset.
    """

    DEFAULT_MIN_VAL = ConfigConst.DEFAULT_VAL
    DEFAULT_MAX_VAL = 100.0

    def __init__(self, name: str = ConfigConst.NOT_SET, typeID: int = ConfigConst.DEFAULT_SENSOR_TYPE, 
                 dataSet: SensorDataSet = None, minVal: float = DEFAULT_MIN_VAL, 
                 maxVal: float = DEFAULT_MAX_VAL):
        self.name = name
        self.typeID = typeID
        self.dataSet = dataSet
        self.dataSetIndex = 0
        self.latestSensorData = None
        self.useRandomizer = dataSet is None

        if self.useRandomizer:
            self.minVal = minVal
            self.maxVal = maxVal

    def generateTelemetry(self) -> SensorData:
        """
        Generates a new SensorData instance based on either random values
        or a dataset, depending on the initialization parameters.
        """
        sensorData = SensorData(typeID=self.getTypeID(), name=self.getName())
        
        if self.useRandomizer:
            sensorVal = random.uniform(self.minVal, self.maxVal)
        else:
            sensorVal = self.dataSet.getDataEntry(index=self.dataSetIndex)
            self.dataSetIndex += 1
            
            if self.dataSetIndex >= self.dataSet.getDataEntryCount():
                self.dataSetIndex = 0

        # Update to use set_value instead of setValue
        sensorData.set_value(sensorVal)
        self.latestSensorData = sensorData
        
        return self.latestSensorData

    def getTelemetryValue(self) -> float:
        """
        Returns the current value of the latest SensorData, generating new data if necessary.
        """
        if not self.latestSensorData:
            self.generateTelemetry()
        
        # Update to use get_value instead of getValue
        return self.latestSensorData.get_value()

    def getName(self) -> str:
        return self.name

    def getTypeID(self) -> int:
        return self.typeID

