import logging
import redis
from programmingtheiot.data.SensorData import SensorData  # Ensure this import is correct
from programmingtheiot.common.ConfigUtil import ConfigUtil
from programmingtheiot.common.ResourceNameEnum import ResourceNameEnum
import programmingtheiot.common.ConfigConst as ConfigConst

# Constants
DATA_GATEWAY_SERVICE = 'Data.GatewayService'

class RedisPersistenceAdapter:
    def __init__(self):
        self.config = ConfigUtil.getInstance()  # Should work if Singleton is set up correctly
        self.host = self.config.getProperty(DATA_GATEWAY_SERVICE, 'host')
        self.port = int(self.config.getProperty(DATA_GATEWAY_SERVICE, 'port'))
        self.redis_client = None
        self.connected = False

        logging.info("Initialized RedisPersistenceAdapter with host: %s and port: %d", self.host, self.port)

    def connectClient(self) -> bool:
        if self.connected:
            logging.warning("Redis client is already connected.")
            return True

        try:
            self.redis_client = redis.StrictRedis(host=self.host, port=self.port, decode_responses=True)
            self.redis_client.ping()  # Test the connection
            self.connected = True
            logging.info("Successfully connected to Redis.")
            return True
        except Exception as e:
            logging.error("Failed to connect to Redis: %s", e)
            return False

    def disconnectClient(self) -> bool:
        if not self.connected:
            logging.warning("Redis client is already disconnected.")
            return True

        try:
            self.redis_client = None
            self.connected = False
            logging.info("Successfully disconnected from Redis.")
            return True
        except Exception as e:
            logging.error("Failed to disconnect from Redis: %s", e)
            return False

    def storeData(self, resource: ResourceNameEnum, data: SensorData) -> bool:
        if not self.connected:
            logging.error("Cannot store data. Redis client is not connected.")
            return False

        try:
            topic = str(resource)
            data_dict = data.__dict__  # Convert SensorData to dict
            self.redis_client.hmset(topic, data_dict)  # Store the data
            logging.info("Stored data for topic '%s': %s", topic, data_dict)
            return True
        except Exception as e:
            logging.error("Failed to store data: %s", e)
            return False
