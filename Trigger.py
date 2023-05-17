#trigger
import schedule
import time
import datetime



def job():
    print("Zaman:", datetime.datetime.now())


#schedule.every().monday.at("10:00").do(job)
schedule.every(1).minutes.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)

#triggerend