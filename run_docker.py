#!/usr/bin/python
import subprocess
import logging
logging.basicConfig(filename="./data/logs/build_log.log", format='%(asctime)s - %(levelname)s - %(name)s - %(filename)s.%(funcName)s()(%(lineno)d):%(message)s')

if __name__ == '__main__':
    logging.info("Starting building docker image.")
    with open("./data/logs/build_log.log", "a") as output:
        subprocess.call("docker build . -t test-bdh ", shell=True, stdout=output, stderr=output)
    logging.info("Docker image was successful built.")
    logging.info("DStarting docker container.")
    with open("./data/logs/build_log.log", "a") as output:
        subprocess.call('docker run -v "D:\\Personal projects\\bdh\\data":/data test-bdh', shell=True, stdout=output,
                        stderr=output)
    logging.info("Docker container ran successfully.")