import yaml
import os
import configparser
import sys


class AppConfig:

    def __init__(self) -> None:
        # Set Root before importing project modules
        os.environ["DASH_APP_ROOT"] = os.path.dirname(
            os.path.abspath(__file__)
        )
        os.environ["APP_ROOT"] = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "../../../"
        )
        self.APP_ROOT = os.getenv("APP_ROOT")
        self.DASH_APP_ROOT = os.getenv("DASH_APP_ROOT")
        if sys.argv[0] != "":
            self.APP_CONFIG_FILE = sys.argv[1]
        else:
            self.APP_CONFIG_FILE = os.path.join(self.APP_ROOT, "config.ini")

        config = configparser.ConfigParser()
        config.sections()
        config.read(self.APP_CONFIG_FILE)
        self.APP_TITLE = config["appcfg"]["title"]
        self.db_url = config["appcfg"]["db_url"]
        self.debug = config["appcfg"]["debug"]
        self.dataplane_url = config["dataplane"]["url"]
        self.max_file_size = int(config["appcfg"]["max_file_size"])
        self.max_storage_size = int(config["appcfg"]["max_storage_size"])
        self.enable_announcements = config["appcfg"]["enable_announcements"]
