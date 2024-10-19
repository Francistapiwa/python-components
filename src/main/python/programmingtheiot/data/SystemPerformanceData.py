import programmingtheiot.common.ConfigConst as ConfigConst
from programmingtheiot.data.BaseIotData import BaseIotData

class SystemPerformanceData(BaseIotData):
    """
    Represents system performance data including CPU and memory utilization.
    """
    
    def __init__(self, d=None):
        super(SystemPerformanceData, self).__init__(name=ConfigConst.SYSTEM_PERF_MSG, typeID=ConfigConst.SYSTEM_PERF_TYPE, d=d)
        self.cpu_util = ConfigConst.DEFAULT_VAL
        self.mem_util = ConfigConst.DEFAULT_VAL

    def get_cpu_utilization(self):
        return self.cpu_util

    def get_memory_utilization(self):
        return self.mem_util

    def set_cpu_utilization(self, cpu_util: float):
        self.cpu_util = cpu_util
        self.updateTimeStamp()

    def set_memory_utilization(self, mem_util: float):
        self.mem_util = mem_util
        self.updateTimeStamp()

    def _handle_update_data(self, data):
        if data and isinstance(data, SystemPerformanceData):
            self.cpu_util = data.get_cpu_utilization()
            self.mem_util = data.get_memory_utilization()

