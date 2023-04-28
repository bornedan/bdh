import schedule
import loaddelay
import loadstops
import delaymaintenance
import time

if __name__ == '__main__':
    # SETTING workflow's scheduling
    schedule.every(60).seconds.do(loaddelay.run)
    schedule.every().day.at("02:30").do(loadstops.run)
    schedule.every().day.at("03:00").do(delaymaintenance.run)
    while True:
        schedule.run_pending()
        time.sleep(1)
