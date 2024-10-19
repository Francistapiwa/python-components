import logging
import programmingtheiot.common.ConfigConst as ConfigConst
from programmingtheiot.common.ConfigUtil import ConfigUtil
from programmingtheiot.common.IDataMessageListener import IDataMessageListener
from importlib import import_module
from programmingtheiot.data.ActuatorData import ActuatorData

class ActuatorAdapterManager:
    """
    Manages actuator commands and the actuation of devices in the system.
    """

    def __init__(self, dataMsgListener: IDataMessageListener = None):
        self.dataMsgListener = dataMsgListener
        self.configUtil = ConfigUtil()

        self.useSimulator = self.configUtil.getBoolean(
            section=ConfigConst.CONSTRAINED_DEVICE,
            key=ConfigConst.ENABLE_SIMULATOR_KEY
        )
        self.useEmulator = self.configUtil.getBoolean(
            section=ConfigConst.CONSTRAINED_DEVICE,
            key=ConfigConst.ENABLE_EMULATOR_KEY
        )
        self.deviceID = self.configUtil.getProperty(
            section=ConfigConst.CONSTRAINED_DEVICE,
            key=ConfigConst.DEVICE_LOCATION_ID_KEY,
            defaultVal=ConfigConst.NOT_SET
        )
        self.locationID = self.deviceID  # Use the deviceID as locationID

        self.humidifierActuator = None
        self.hvacActuator = None
        self.ledDisplayActuator = None

        # Initialize environmental actuation tasks
        self._initEnvironmentalActuationTasks()

        # Log emulator/simulator usage
        if self.useEmulator:
            logging.info("Emulators will be used.")
        else:
            logging.info("Simulators will be used.")

    def _initEnvironmentalActuationTasks(self):
        try:
            if not self.useEmulator:
                # Initialize simulated actuator tasks
                from programmingtheiot.cda.sim.HumidifierActuatorSimTask import HumidifierActuatorSimTask
                from programmingtheiot.cda.sim.HvacActuatorSimTask import HvacActuatorSimTask
                self.humidifierActuator = HumidifierActuatorSimTask()
                self.hvacActuator = HvacActuatorSimTask()
            else:
                # Load environmental actuator emulators dynamically
                try:
                    humidifierModule = import_module('programmingtheiot.cda.emulated.HumidifierEmulatorTask')
                    humidifierClazz = getattr(humidifierModule, 'HumidifierEmulatorTask')
                    self.humidifierActuator = humidifierClazz()
                except AttributeError as e:
                    logging.error("HumidifierEmulatorTask not found: %s. Check the class name.", e)

                try:
                    hvacModule = import_module('programmingtheiot.cda.emulated.HvacEmulatorTask')
                    hvacClazz = getattr(hvacModule, 'HvacEmulatorTask')
                    self.hvacActuator = hvacClazz()
                except AttributeError as e:
                    logging.error("HvacEmulatorTask not found: %s. Check the class name.", e)

                try:
                    ledDisplayModule = import_module('programmingtheiot.cda.emulated.LedDisplayEmulatorTask')
                    ledDisplayClazz = getattr(ledDisplayModule, 'LedDisplayEmulatorTask')
                    self.ledDisplayActuator = ledDisplayClazz()
                except AttributeError as e:
                    logging.error("LedDisplayEmulatorTask not found: %s. Check the class name.", e)
        except Exception as e:
            logging.error("Unexpected error while initializing actuators: %s", e)
            raise

    def setDataMessageListener(self, listener: IDataMessageListener) -> bool:
        if listener:
            self.dataMsgListener = listener
            return True
        return False

    def sendActuatorCommand(self, data: ActuatorData) -> ActuatorData:
        if data and not data.is_response_flag_enabled():
            if data.getLocationID() == self.locationID:
                logging.info("Actuator command received for location ID %s. Processing...", str(data.getLocationID()))

                aType = data.getTypeID()
                responseData = None

                if aType == ConfigConst.HUMIDIFIER_ACTUATOR_TYPE and self.humidifierActuator:
                    responseData = self.humidifierActuator.updateActuator(data)
                elif aType == ConfigConst.HVAC_ACTUATOR_TYPE and self.hvacActuator:
                    responseData = self.hvacActuator.updateActuator(data)
                elif aType == ConfigConst.LED_DISPLAY_ACTUATOR_TYPE and self.ledDisplayActuator:
                    responseData = self.ledDisplayActuator.updateActuator(data)
                else:
                    logging.warning("No valid actuator type. Ignoring actuation for type: %s", data.getTypeID())

                return responseData
            else:
                logging.warning("Location ID doesn't match. Ignoring actuation: (me) %s != (you) %s",
                                str(self.locationID), str(data.getLocationID()))
        else:
            logging.warning("Actuator request received. Message is empty or response. Ignoring.")

        return None

