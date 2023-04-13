import schedule
import loaddelay
import loadstops
import time



if __name__ == '__main__':
    schedule.every(1).minute.do(loaddelay.run)
    while True:
        schedule.run_pending()
        time.sleep(1)