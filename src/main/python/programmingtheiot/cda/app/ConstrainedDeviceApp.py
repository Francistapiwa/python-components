#####
# 
# This class is part of the Programming the Internet of Things
# project, and is available via the MIT License, which can be
# found in the LICENSE file at the top level of this repository.
# 
# You may find it more helpful to your design to adjust the
# functionality, constants and interfaces (if there are any)
# provided within in order to meet the needs of your specific
# Programming the Internet of Things project.
# 

import logging
from time import sleep

from programmingtheiot.cda.app.DeviceDataManager import DeviceDataManager
import programmingtheiot.common.ConfigConst as ConfigConst
from programmingtheiot.common.ConfigUtil import ConfigUtil

logging.basicConfig(format='%(asctime)s:%(name)s:%(levelname)s:%(message)s', level=logging.DEBUG)

class ConstrainedDeviceApp:
    """
    Definition of the ConstrainedDeviceApp class.
    """

    def __init__(self):
        """
        Initialization of class.
        """
        logging.info("Initializing CDA...")
        
        # Create an instance of DeviceDataManager
        self.devDataMgr = DeviceDataManager()

    def startApp(self):
        """
        Start the CDA. Calls startManager() on the device data manager instance.
        """
        logging.info("Starting CDA...")
        self.devDataMgr.startManager()  # Start the DeviceDataManager
        logging.info("CDA started.")

    def stopApp(self, code: int):
        """
        Stop the CDA. Calls stopManager() on the device data manager instance.
        """
        logging.info("CDA stopping...")
        self.devDataMgr.stopManager()  # Stop the DeviceDataManager
        logging.info("CDA stopped with exit code %s.", str(code))

    def parseArgs(self, args):
        """
        Parse command line args.
        
        @param args The arguments to parse.
        """
        logging.info("Parsing command line args...")
        # TODO: Implement argument parsing if needed

def main():
    """
    Main function definition for running client as application.
    """
    cda = ConstrainedDeviceApp()
    cda.startApp()
    
    # Check if the app should run forever
    runForever = ConfigUtil().getBoolean(ConfigConst.CONSTRAINED_DEVICE, ConfigConst.RUN_FOREVER_KEY)

    if runForever:
        while True:
            sleep(5)
    else:
        # Run for 65 seconds or any other configurable duration
        sleep(65)
    
    # Stop the app
    cda.stopApp(0)  # Provide a code for graceful exit

if __name__ == '__main__':
    """
    Attribute definition for when invoking as app via command line
    """
    main()
