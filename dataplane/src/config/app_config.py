import yaml
import os
import configparser
import filestoreprovider.filestoreprovider as fsp
import vaultprovider.vaultprovider as vp
import backgroundprovider.backgroundprovider as bp


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
        self.APP_CONFIG_FILE = os.path.join(self.APP_ROOT, "config.ini")

        config = configparser.ConfigParser()
        config.sections()
        config.read(self.APP_CONFIG_FILE)
        self.APP_TITLE = config["appcfg"]["title"]
        self.db_url = config["appcfg"]["db_url"]
        self.allow_plus_in_email = config["appcfg"].getboolean(
            "allow_plus_in_email"
        )
        self.file_ttl = int(config["appcfg"]["file_ttl"])
        self.max_file_size = int(config["appcfg"]["max_file_size"])
        self.max_storage_size = int(config["appcfg"]["max_storage_size"])
        self.filestoreprovider = fsp.FileStoreProviderFactory.get_provider(
            config
        )
        self.vaultprovider = vp.VaultProviderFactory.get_provider(config)
        self.dataplane_url = config["dataplane"]["url"]
        self.backgroundprovider = bp.BackgroundProviderFactory.get_provider(
            config
        )


settings = AppConfig()
