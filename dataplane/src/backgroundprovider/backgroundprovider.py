import configparser
from fastapi import BackgroundTasks
from backgroundprovider.base import BackgroundProvider


class BackgroundProviderFactory:

    @staticmethod
    def get_provider(config: configparser.ConfigParser) -> BackgroundProvider:
        if config["backgroundprovider"]["type"] == "fastapi":
            return BackgroundTasks
        else:
            return None
