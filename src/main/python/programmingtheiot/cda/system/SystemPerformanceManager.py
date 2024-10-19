import logging
from apscheduler.schedulers.background import BackgroundScheduler
import programmingtheiot.common.ConfigConst as ConfigConst
from programmingtheiot.common.ConfigUtil import ConfigUtil
from programmingtheiot.common.IDataMessageListener import IDataMessageListener
from programmingtheiot.cda.system.SystemCpuUtilTask import SystemCpuUtilTask
from programmingtheiot.cda.system.SystemMemUtilTask import SystemMemUtilTask
from programmingtheiot.data.SystemPerformanceData import SystemPerformanceData

class SystemPerformanceManager(object):
    """
    SystemPerformanceManager collects and manages system performance data.
    """

    def __init__(self):
        configUtil = ConfigUtil()
        
        # Get the poll rate from the configuration
        self.pollRate = configUtil.getInteger(
            section=ConfigConst.CONSTRAINED_DEVICE,
            key=ConfigConst.POLL_CYCLES_KEY,
            defaultVal=ConfigConst.DEFAULT_POLL_CYCLES
        )
        
        # Get the location ID from the configuration
        self.locationID = configUtil.getProperty(
            section=ConfigConst.CONSTRAINED_DEVICE,
            key=ConfigConst.DEVICE_LOCATION_ID_KEY,
            defaultVal=ConfigConst.NOT_SET
        )
        
        # Validate pollRate
        if self.pollRate <= 0:
            self.pollRate = ConfigConst.DEFAULT_POLL_CYCLES
        
        self.dataMsgListener = None
        self.scheduler = BackgroundScheduler()
        self.scheduler.add_job(self.handleTelemetry, 'interval', seconds=self.pollRate)
        
        self.cpuUtilTask = SystemCpuUtilTask()
        self.memUtilTask = SystemMemUtilTask()

    def handleTelemetry(self):
        cpuUtilPct = self.cpuUtilTask.getTelemetryValue()
        memUtilPct = self.memUtilTask.getTelemetryValue()
        
        logging.debug('CPU utilization is %s percent, and memory utilization is %s percent.', 
                      str(cpuUtilPct), str(memUtilPct))
        
        # Create an instance of SystemPerformanceData and set the values
        sysPerfData = SystemPerformanceData()
        sysPerfData.setLocationID(self.locationID)
        sysPerfData.set_cpu_utilization(cpuUtilPct)  # Updated method name
        sysPerfData.set_memory_utilization(memUtilPct)  # Updated method name

        # Invoke the callback method if a listener is set
        if self.dataMsgListener:
            self.dataMsgListener.handleSystemPerformanceMessage(data=sysPerfData)

    def setDataMessageListener(self, listener: IDataMessageListener) -> bool:
        if listener:
            self.dataMsgListener = listener
            logging.info("Data message listener set.")
            return True
        else:
            logging.warning("Attempted to set a None listener.")
            return False

    def startManager(self):
        logging.info("Starting SystemPerformanceManager.")
        if not self.scheduler.running:
            self.scheduler.start()
            logging.info("SystemPerformanceManager started.")
        else:
            logging.warning("SystemPerformanceManager scheduler already started. Ignoring.")

    def stopManager(self):
        logging.info("Stopping SystemPerformanceManager.")
        try:
            self.scheduler.shutdown()
            logging.info("SystemPerformanceManager stopped.")
        except Exception as e:
            logging.warning("Error stopping SystemPerformanceManager scheduler: %s", str(e))

