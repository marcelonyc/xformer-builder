import configparser
import os
import argparse


def upgrade_config(current_config, default_config, new_config):
    config = configparser.ConfigParser()
    config.read(default_config)
    config.read(current_config)
    config.write(open(new_config, "w"))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--current_config", help="Current Config file")
    parser.add_argument("-d", "--default_config", help="Current Config file")
    parser.add_argument("-n", "--new_config", help="New Config file")
    args = parser.parse_args()
    return args


args = main()

upgrade_config(args.current_config, args.default_config, args.new_config)
