import schedule
import time
from datetime import datetime

def task():
    print("This is a task.", datetime.now())

# schedule.every(5).minutes.at(":00").do(task)
for i in range(12):
            schedule.every(1).hours.at(":{:02d}".format(i*5)).do(task)

try:
    print("start", datetime.now())
    while True:
        schedule.run_pending()
        time.sleep(1)
except:
    pass