import time
import schedule
from tdnet_bot.db import collect
from datetime import datetime


schedule.every().monday.at("18:00").do(collect)
schedule.every().tuesday.at("18:00").do(collect)
schedule.every().wednesday.at("18:00").do(collect)
schedule.every().thursday.at("18:00").do(collect)
schedule.every().friday.at("18:00").do(collect)

while True:
    print(f"collect 実行: {datetime.now()}")
    schedule.run_pending()
    time.sleep(60) 