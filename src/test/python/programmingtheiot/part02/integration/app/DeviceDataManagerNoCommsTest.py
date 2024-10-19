#####
# 
# This class is part of the Programming the Internet of Things
# project, and is available via the MIT License, which can be
# found in the LICENSE file at the top level of this repository.
# 
# Copyright (c) 2020 by Andrew D. King
# 

import logging
import unittest
from time import sleep
from programmingtheiot.cda.app.DeviceDataManager import DeviceDataManager

class DeviceDataManagerNoCommsTest(unittest.TestCase):
    """
    Test case for DeviceDataManager with no communications.
    """

    @classmethod
    def setUpClass(cls):
        logging.basicConfig(format='%(asctime)s:%(module)s:%(levelname)s:%(message)s', level=logging.DEBUG)
        logging.info("Testing DeviceDataManager class...")

    def setUp(self):
        self.ddMgr = DeviceDataManager()
    
    def tearDown(self):
        self.ddMgr.stopManager()  # Ensure the manager stops after each test
    
    def testStartAndStopManagerNoComms(self):
        """
        Test starting and stopping the DeviceDataManager with communications disabled.
        Ensure that appropriate logging occurs.
        """
        self.ddMgr.startManager()
        
        sleep(120)  # Let it run for a while to generate logs
        
        self.ddMgr.stopManager()

if __name__ == "__main__":
    unittest.main()
