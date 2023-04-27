import datetime
import yaml
import logging
from logging import config
import sys
import os
config = None
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(name)s - %(filename)s.%(funcName)s()(%(lineno)d):%(message)s')
def list_replace_value(l: list, old: str, new: str) -> list:
    x = []
    for e in l:
        if isinstance(e, list):
            e = list_replace_value(e, old, new)
        elif isinstance(e, dict):
            e = dict_replace_value(e, old, new)
        elif isinstance(e, str):
            e = e.replace(old, new)
        x.append(e)
    return x
def dict_replace_value(d: dict, old: str, new: str) -> dict:
    x = {}
    for k, v in d.items():
        if isinstance(v, dict):
            v = dict_replace_value(v, old, new)
        elif isinstance(v, list):
            v = list_replace_value(v, old, new)
        elif isinstance(v, str):
            v = v.replace(old, new)
        x[k] = v
    return x


def log_unexpected_except(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    logging.error("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))

def get_config():
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
        #path=os_path
        #config = dict_replace_value(config, "@path@", path)
    else:
        logging.debug("Config file was loaded earlier.")
    #config['log']['handlers']['file']['filename'] = config['log-setting']['orig-path']+datetime.datetime.today().strftime('%Y_%m_%d')+"_wf_load_data" + ".log"
    return config


logging.config.dictConfig(get_config()['log'])

def get_api_headers():
    logging.debug("Start method")
    get_config()
    api_key_file = open(config['token-url'],"r")
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