import yaml
import os
import configparser
import filestoreprovider.filestoreprovider as fsp
import vaultprovider.vaultprovider as vp
import backgroundprovider.backgroundprovider as bp
import logging
from functools import lru_cache


class AppConfig:

    def __init__(self) -> None:
        # Set Root before importing project modules
        os.environ["DASH_APP_ROOT"] = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "../../"
        )
        os.environ["APP_ROOT"] = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "../../../"
        )

        self.run_mode = os.getenv("RUN_MODE")
        if not self.run_mode:
            raise ValueError("RUN_MODE not set. It is required")

        self.APP_ROOT = os.getenv("APP_ROOT")
        self.DASH_APP_ROOT = os.getenv("DASH_APP_ROOT")
        self.APP_CONFIG_FILE = os.path.join(self.APP_ROOT, "config.ini")

        if self.run_mode == "prod":
            self.prod_arguments()

        config = configparser.ConfigParser()
        config.sections()
        config.read(self.APP_CONFIG_FILE)

        self.APP_TITLE = config.get("appcfg", "title")
        self.allow_plus_in_email = config.getboolean(
            "appcfg", "allow_plus_in_email"
        )

        self.file_ttl = config.getint("appcfg", "file_ttl")
        self.max_file_size = config.getint("appcfg", "max_file_size")
        self.max_storage_size = config.getint("appcfg", "max_storage_size")
        self.require_email_verification = config.getboolean(
            "appcfg", "require_email_verification"
        )
        self.dataplane_url = config.get("dataplane", "url")
        self.webhook_domain_whitelist = config.get(
            "appcfg", "webhook_domain_whitelist"
        ).split(",")

        # Providers need the full config to be passed
        self.vaultprovider = vp.VaultProviderFactory.get_provider(config)
        self.filestoreprovider = fsp.FileStoreProviderFactory.get_provider(
            config, self.vaultprovider
        )
        self.backgroundprovider = bp.BackgroundProviderFactory.get_provider(
            config
        )
        self.dataplane_token = self.vaultprovider.get_secret("dataplane_token")
        if not self.dataplane_token:
            raise ValueError(
                "dataplane_token not found in vault. It is required"
            )
        if self.run_mode == "prod" and self.dataplane_token == "for_dev_only":
            raise ValueError(
                f"dataplane_token is set to {self.dataplane_token}. Do not run in prod with this token"
            )

        # Handle configs with secrets
        # look for the syntax ${vault:secret_name} and replace with the secret
        self.db_url = config.get("appcfg", "db_url")

        # Logging
        self.log_level = config.get("appcfg", "log_level").upper()
        _log_level = {
            "DEBUG": logging.DEBUG,
            "INFO": logging.INFO,
            "WARN": logging.WARN,
            "ERROR": logging.ERROR,
        }
        logging.getLogger().setLevel(
            _log_level.get(self.log_level, logging.INFO)
        )

    def prod_arguments(self):
        config_file = os.getenv("APP_CONFIG_FILE")

        try:
            _valid_config_file = os.path.exists(config_file)
        except Exception as e:
            _valid_config_file = False

        if not _valid_config_file:
            raise FileNotFoundError(
                f"Config file not found at {config_file or 'Not provided'} define in env var APP_CONFIG_FILE"
            )

        self.APP_CONFIG_FILE = config_file


@lru_cache
def get_settings() -> AppConfig:
    return AppConfig()
