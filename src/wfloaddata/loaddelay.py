import requests, os
from zipfile import ZipFile
import logging
import logging.config
import datetime
import shutil
import pandas as pd
import requests
import regex
import yaml
import pyarrow
from src.common import common as cmn


logging.config.dictConfig(cmn.get_config()['log'])


def get_rtvp(url, headers):
    logging.debug("Start loading rtvp json.")
    response = requests.get(url, headers=headers)
    if (response.status_code != 200):
        logging.error("API request ended with status code: " + str(response.status_code))
        raise Exception("API request ended with status code: " + str(response.status_code))
    else:
        logging.debug("API request ended with status code: 200")
    return response


def normalize_json(json_file, separator):
    logging.debug("Normalize json with separator " + separator)
    try:
        normalized_json = pd.json_normalize(json_file.json()['features'], sep=separator)
    except:
        logging.error("Failed json normalizing")
        logging.error(json_file.json)
    return normalized_json


def apply_filters(veh_pos, filters: dict):
    logging.debug("Applying filters.")
    if filters:
        for key, value in filters.items():
            veh_pos = veh_pos[veh_pos[key].str.contains(value, regex=False, na=False)]
            logging.debug("String filter \"" + value + "\" on column " + key + " was applied.")
    else:
        logging.debug("No filter applied")
    return veh_pos


def save_file(path, file, time):
    logging.debug("Saving file to "+path+time+"_rtvp.parquet")
    file.to_parquet(path+time+"_rtvp.parquet")

def run():
    url = cmn.get_config()['pid']['rtvp']['url']
    separator = cmn.get_config()['data']['rtvp']['json-separator']
    saving_path = cmn.get_config()['data']['stage']['path']
    today = datetime.datetime.today().strftime('%Y_%m_%d')
    now = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
    headers = cmn.get_api_headers()
    veh_pos_raw = get_rtvp(url, headers)
    veh_pos = normalize_json(veh_pos_raw, separator)
    veh_pos = apply_filters(veh_pos,cmn.get_config()['data']['rtvp']['filters'])
    save_file(saving_path,veh_pos,now)

if __name__ == '__main__':
    run()
