import time, schedule
from FanboxScrapSel import FanboxScrapSel


def process():
    print("process to start.")
    FanboxScrapSel().fanboxScrapProcess()
    print("process completed.")


def scheduler():
    schedule.every().minute.do(process)
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == '__main__':
    scheduler()
