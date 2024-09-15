import configparser
import os
import argparse


def upgrade_config(config_file):
    config = configparser.ConfigParser()
    config.read(config_file)
    config.set("DEFAULT", "version", "1.0")
    with open(config_file, "w") as configfile:
        config.write(configfile)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("current_config", help="Config file to upgrade")
    parser.add_argument("config_file", help="Config file to upgrade")
    args = parser.parse_args()
    return args


args = main()

upgrade_config(args.config_file)
