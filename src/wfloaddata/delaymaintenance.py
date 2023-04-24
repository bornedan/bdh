from src.common import common as cmn
import pandas as pd
import os
import re
import datetime
from datetime import datetime
import pyarrow
import copy
import logging
import logging.config

logging.config.dictConfig(cmn.get_config()['log'])


def get_all_files(source_path):
    logging.debug("Finding all files in source folder.")
    gtfs_files = os.listdir(source_path)
    return gtfs_files


def filter_rtvp_files(files_list):
    logging.debug("Filtering only rtvp files.")
    pat = re.compile(
        r'^\d\d\d\d_(0[1-9]|10|11|12)_(0[1-2]|[1-2][0-9]|3[0-1])_([0-1][0-9]|2[0-3])_([0-5][0-9])_([0-5][0-9])_rtvp.parquet$')
    filtered_file = [name for name in files_list if pat.match(name)]
    return filtered_file


def extract_datetime(files_list):
    logging.debug("Parse datetimes from rtvp files")
    f_list = []
    for file in files_list:
        split_name = file.split('_')
        date = "{0}_{1}_{2}".format(split_name[0], split_name[1], split_name[2])
        time = "{0}_{1}_{2}".format(split_name[3], split_name[4], split_name[5])
        date_time = "{0}_{1}".format(date, time)
        date_time_obj = datetime.strptime(date_time, '%Y_%m_%d_%H_%M_%S')
        f_list.append((file, date_time_obj))
    return f_list


def split_files_to_groups(files):
    logging.debug("Split rtvp files to same date group.")
    groups = []
    files_rmv = copy.deepcopy(files)
    files_iter = copy.deepcopy(files)
    while True:
        if files_iter:
            grp_size = len(groups)
            processing_date = None
            groups.append([])
            for file in files_iter:
                if processing_date is None:
                    processing_date = file[1].date()
                    groups[grp_size].append(file)
                    files_rmv.remove(file)
                else:
                    if file[1].date() == processing_date:
                        groups[grp_size].append(file)
                        files_rmv.remove(file)
        else:
            break
        files_iter = copy.deepcopy(files_rmv)
    logging.debug("{} separated date group found.".format(len(groups)))
    return groups;


def get_compacted_file_name(group):
    logging.debug("Creating compacted file name.")
    if group:
        dt = group[0][1]
        name = dt.date().strftime('%Y_%m_%d_rtvp.parquet')
        date = dt.date()
        logging.debug("File name: {}".format(name))
        return (name, date)
    else:
        logging.error("File name does not exists!")
        return ("", datetime.now().date())


def load_dfs(source_path, group, date):
    logging.debug("Start compacting files from {}".format(str(group[0][1].date())))
    frames = []
    for file in group:
        df = pd.read_parquet(("{}/{}").format(source_path, file[0]))
        df['timestamp'] = date
        frames.append(df)
    res = pd.concat(frames)
    logging.debug("Compacting completed")
    return res


def save_to_file(source_path, target_path, grouped_files):
    logging.debug("Start saving compacted files.")
    existing_files = os.listdir(target_path)
    for group in grouped_files:
        cfn = get_compacted_file_name(group)
        file_name = cfn[0]
        logging.debug("Saving rtvp to {}".format(file_name))
        date = cfn[1]
        compacted_df = load_dfs(source_path, group, date)
        if file_name in existing_files:
            logging.debug("File name {} already exists".format(file_name))
            df_e = pd.read_parquet("{0}/{1}".format(target_path, file_name))
            df_e = pd.concat([df_e, compacted_df])
            df_e.to_parquet("{0}/{1}".format(target_path, file_name))
        else:
            compacted_df.to_parquet("{0}/{1}".format(target_path, file_name))
        logging.debug("Compacted file was saved.")


def delete_uncompacted_rtvp_files(path, file_list):
    logging.debug("Removing files from directory.")
    for file in file_list:
        try:
            os.remove("{}/{}".format(path, file))
            logging.debug("File: " + path + "/" + file + " was removed.")
        except:
            logging.error("File: " + path + "/" + file + " can not be removed.")
    logging.debug("Removing files ended.")


def run():
    source_path = cmn.get_config()['data']['stage']['path']
    target_path = cmn.get_config()['data']['rtvp']['path']
    compact_file_names = get_all_files(source_path)
    rtvp_file_names = filter_rtvp_files(compact_file_names)
    datetime_list = extract_datetime(rtvp_file_names)
    groups = split_files_to_groups(datetime_list)
    save_to_file(source_path, target_path, groups)
    delete_uncompacted_rtvp_files(source_path, rtvp_file_names)


if __name__ == '__main__':
    run()
