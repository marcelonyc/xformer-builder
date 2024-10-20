from functools import lru_cache
import yaml
import os
import configparser
from configparser import ConfigParser
import sys
from vaultprovider import vaultprovider as vp


class AppConfig:

    def __init__(self) -> None:
        # Set Root before importing project modules
        os.environ["DASH_APP_ROOT"] = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "../../"
        )
        os.environ["APP_ROOT"] = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "../../../"
        )

        self.APP_ROOT = os.getenv("APP_ROOT")
        self.DASH_APP_ROOT = os.getenv("DASH_APP_ROOT")

        self.APP_CONFIG_FILE = os.getenv("APP_CONFIG_FILE")

        if self.APP_CONFIG_FILE is None or self.APP_CONFIG_FILE == "":
            self.APP_CONFIG_FILE = os.path.join(self.APP_ROOT, "config.ini")

        config = configparser.ConfigParser()
        config.sections()
        config.read(self.APP_CONFIG_FILE)

        # Providers need the full config to be passed
        self.vaultprovider = vp.VaultProviderFactory.get_provider(config)
        # After vault provider is initialized, we can parse the secrets in config
        # These are values like ${vault:secret_name} in config.ini
        self.parse_vault_secrets(config)

        self.APP_TITLE = config.get("appcfg", "title")
        self.db_url = config.get("appcfg", "db_url")
        self.debug = config.getboolean("appcfg", "debug")
        self.dataplane_url = config.get("dataplane", "url")
        self.max_file_size = config.getint("appcfg", "max_file_size")
        self.max_storage_size = config.getint("appcfg", "max_storage_size")
        self.enable_announcements = config.get(
            "appcfg", "enable_announcements"
        )
        self.webhook_domain_whitelist = config.get(
            "appcfg", "webhook_domain_whitelist"
        ).split(",")

        self.dataplane_token = self.vaultprovider.get_secret("dataplane_token")
        self.controlplane_url = config.get("controlplane", "url")
        self.smtp_enabled =  config.getboolean("smtp", "enabled")


    def parse_vault_secrets(self, config: ConfigParser) -> ConfigParser:
        for section in config.sections():
            for key in config[section]:
                if "${vault:" in config[section][key]:
                    secret_name = (
                        config[section][key].split("${vault:")[1].split("}")[0]
                    )
                    config[section][key] = self.vaultprovider.get_secret(
                        secret_name
                    )
        return config


@lru_cache
def get_settings() -> AppConfig:
    return AppConfig()
