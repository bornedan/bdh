import pickle
import logging
import logging.config
import datetime
import pandas as pd
import requests
import json

from src.common import common as cmn

logging.config.dictConfig(cmn.get_config()['log'])


def validate_JSON(jsonData):
    try:
        json.loads(jsonData)
    except ValueError as err:
        return False
    return True


def get_rtvp(url: str, headers: dict) -> object:
    logging.debug("Start loading rtvp json.")
    for index in range(5):
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            logging.warning("Attempt: {} API request ended with status code: {}".format(index,str(response.status_code)))
        elif not validate_JSON(response.text):
            logging.warning(
                "Attempt: {} JSON file is broken.".format(index))
        else:
            logging.debug("API request correctly was load.")
            return response
    logging.ERROR("Load API response failed.")
    raise Exception("Can not load API response.")


def normalize_json(json_file, separator):
    logging.debug("Normalize json with separator " + separator)
    try:
        normalized_json = pd.json_normalize(json_file.json()['features'], sep=separator)
    except:
        logging.error("Failed json normalizing")
        try:
            logging.error("Try save json object.")
            with open('/data/logs/json.pickle', 'wb') as outp:
                pickle.dump(json_file, outp, pickle.HIGHEST_PROTOCOL)
        except:
            logging.error("Saving pickle object failed.")
        try:
            logging.error("Print json object as string.")
            logging.error(str(json_file))
        except:
            logging.error("Can not print json object as string.")
        try:
            logging.error("Try print separate info about json object.")
            try:
                logging.error("Print status code")
                logging.error(str(json_file.status_code))
            except:
                logging.error("Can not print status code")
            try:
                logging.error("Print string request")
                logging.error(str(json_file.request))
            except:
                logging.error("Can not print string request")
            try:
                logging.error("Print header")
                logging.error(str(json_file.headers))
            except:
                logging.error("Can not print header")
            try:
                logging.error("Print json text")
                logging.error(str(json_file.text))
            except:
                logging.error("Can not text")
            logging.error("End of section separate info about json object.")
        except:
            logging.error("Unexpected error. Can not analyze this object.")
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
    logging.debug("Saving file to " + path + time + "_rtvp.parquet")
    file.to_parquet(path + time + "_rtvp.parquet")


def run():
    url = cmn.get_config()['pid']['rtvp']['url']
    separator = cmn.get_config()['data']['rtvp']['json-separator']
    saving_path = cmn.get_config()['data']['stage']['path']
    now = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
    headers = cmn.get_api_headers()

    veh_pos_raw = get_rtvp(url, headers)
    veh_pos = normalize_json(veh_pos_raw, separator)
    veh_pos = apply_filters(veh_pos, cmn.get_config()['data']['rtvp']['filters'])
    save_file(saving_path, veh_pos, now)


if __name__ == '__main__':
    run()
