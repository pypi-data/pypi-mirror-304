from abc import ABC
import os
from navconfig import config


class EnvSupport(ABC):
    """EnvSupport.

    Support for Environment Variables
    """

    def __init__(self, *args, **kwargs):
        self._environment = config

    def get_env_value(self, key, default: str = None, expected_type: object = None):
        """
        Retrieves a value from the environment variables or the configuration.

        :param key: The key for the environment variable.
        :param default: The default value to return if the key is not found.
        :return: The value of the environment variable or the default value.
        """
        if key is None:
            return default
        if val := os.getenv(str(key)):
            return val
        elif expected_type is not None:
            if expected_type in (int, float):
                return self._environment.getint(key, default)
            elif expected_type == bool:
                return self._environment.getboolean(key, default)
            else:
                return self._environment.get(key, default)
        elif val := self._environment.get(key, default):
            return val
        else:
            return key
