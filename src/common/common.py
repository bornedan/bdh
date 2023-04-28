import datetime
import yaml
import logging
from logging import config
import sys
import os

config = None
logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(name)s - %(filename)s.%(funcName)s()(%(lineno)d):%(message)s')

#Function for replacing placehlders in inner dictionary
"""def list_replace_value(l: list, old: str, new: str) -> list:
    x = []
    for e in l:
        if isinstance(e, list):
            e = list_replace_value(e, old, new)
        elif isinstance(e, dict):
            e = dict_replace_value(e, old, new)
        elif isinstance(e, str):
            e = e.replace(old, new)
        x.append(e)
    return x"""

#Function for replacing placehlders in inner dictionary
"""def dict_replace_value(d: dict, old: str, new: str) -> dict:
    x = {}
    for k, v in d.items():
        if isinstance(v, dict):
            v = dict_replace_value(v, old, new)
        elif isinstance(v, list):
            v = list_replace_value(v, old, new)
        elif isinstance(v, str):
            v = v.replace(old, new)
        x[k] = v
    return x"""


def log_unexpected_except(exc_type, exc_value, exc_traceback):
    """
    Redirecting unexpected errors to logger.
    :param exc_type:
    :param exc_value:
    :param exc_traceback:
    :return:
    """
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    logging.error("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))


def get_config():
    """
    Load config variables from config.yaml

    :return: Loaded config file [Dictionary]
    """
    global config
    if config == None:
        sys.excepthook = log_unexpected_except
        logging.debug("Start read config.yaml")
        try:
            with open("/config.yaml") as f:
                config = yaml.safe_load(f)
        except:
            logging.error("Load config.yaml failed")
        logging.debug("Config.yaml was loaded.")
    else:
        logging.debug("Config file was loaded earlier.")
    return config

#Set logger from config file
logging.config.dictConfig(get_config()['log'])


def get_api_headers():
    """
    Create HTTP API header for connecting to Golemio API.
    \n
    Header format:
        'Content-Type': 'application/json; charset=utf-8',
        'x-access-token': [api_key]
    \n
    x-access-token is loaded from file based on config file. \n
    :return: Header [Dictionary]
    """
    logging.debug("Start method")
    get_config()
    api_key_file = open(config['token-url'], "r")
    logging.debug("Get api key url: " + str(api_key_file))
    api_key = api_key_file.read()
    api_key_file.close()
    logging.debug("Get api key")
    headers = {
        'Content-Type': 'application/json; charset=utf-8',
        'x-access-token': api_key
    }
    return headers


if __name__ == '__main__':
    get_config()
