import requests, os
from zipfile import ZipFile
import logging
import logging.config
import datetime
import shutil

from src.common import common as cmn

logging.config.dictConfig(cmn.get_config()['log'])

def download_gtfs_zip(url, save_path, chunk_size=128):
    """
    Download zip file from http://data.pid.cz/PID_GTFS.zip with all information about Prague public transport like
    bus stop list, etc...
    :param url: Web url with zip file.
    :param save_path: Path to destination folder.
    :param chunk_size:
    :return:
    """
    logging.debug("Start downloading bus stops names.")
    try:
        r = requests.get(url, stream=True)
        with open(save_path, 'wb') as fd:
            for chunk in r.iter_content(chunk_size=chunk_size):
                fd.write(chunk)
    except:
        logging.error("Downloading gtfs file failed.")
    logging.debug("Downloaded was ended.")

def unzip_gtfs(source_path,destanation_path):
    """
    Unzip given .zip file.
    :param source_path: .zip file destination.
    :param destanation_path: Unzip files location.
    :return:
    """
    logging.debug("Start unzipping file.")
    try:
        with ZipFile(source_path, 'r') as zObject:
            zObject.extractall(
                path=destanation_path)
    except:
        logging.error("Unzipping gtfs file failed.")

    logging.debug("Unzipping was ended.")

def delete_gtfs_files(gtfs_dir_path):
    """
    Load list of given filenames from config.yaml and remove other files in gtfs_dir_path.
    :param gtfs_dir_path: Path to folder with files.
    :return:
    """
    logging.debug("Listing gtfs file names.")
    gtfs_files = os.listdir(gtfs_dir_path)
    file_to_stay = cmn.get_config()['data']['gtfs']['no-delete-list']
    logging.debug("Removing gtfs file to stay")
    for file_name in file_to_stay:
        if file_name in gtfs_files:
            gtfs_files.remove(file_name)
    logging.debug("Removing files from directory.")
    for file in gtfs_files:
        try:
            os.remove(gtfs_dir_path + "/" + file)
            logging.debug("File: " + gtfs_dir_path + "/" + file + " was removed.")
        except:
            logging.warning("File: "+gtfs_dir_path+ "/"+ file + " can not be removed.")
    logging.debug("Removing files ended.")

def move_files(source_dir, dest_dir,day):
    """
    Take files from source_dir and move to dest_dir. Add prefix current date and change suffix to .csv.
    :param source_dir:
    :param dest_dir:
    :param day:
    :return:
    """
    logging.debug("Start moving gtfs files from "+ source_dir+ " to "+ dest_dir)
    files_to_move = os.listdir(source_dir)
    try:
        for file in files_to_move:
            renamed_file = file.replace(".txt",".csv")
            os.rename(source_dir+"/"+file,source_dir+"/"+day+"_"+renamed_file)
            shutil.move(source_dir+"/"+day+"_"+renamed_file,dest_dir+"/"+day+"_"+renamed_file)
        logging.debug("Files was correctly moved")
    except:
        logging.error("Moving files from" +source_dir+" to " +dest_dir+" failed.")

def clean_up(path):
    """
    Remove downloaded zip file.
    :param path: Path to zip file.
    :return:
    """
    logging.debug("Starting cleanup  "+ path)
    try:
        shutil.rmtree(path)
        os.remove(path+".zip")
    except:
        logging.error("Cleaning process failed.")
    logging.debug("Cleaning ended.")




def run():
    today = datetime.datetime.today().strftime('%Y_%m_%d')
    url = cmn.get_config()['pid']['gtfs']['url']
    path = cmn.get_config()['data']['stage']['path']+today + "_gtfs"
    dest_path = cmn.get_config()['data']['gtfs']['path']
    download_gtfs_zip(url, path +".zip")
    unzip_gtfs(path+".zip",path)
    delete_gtfs_files(path)
    move_files(path,dest_path,today)
    clean_up(path)



if __name__ == '__main__':
    run()