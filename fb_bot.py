import os
import requests
from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler

PAGE_ID = os.getenv("PAGE_ID")
PAGE_ACCESS_TOKEN = os.getenv("PAGE_ACCESS_TOKEN")

def post_to_facebook():
    message = "This is your scheduled post!"
    url = f"https://graph.facebook.com/{PAGE_ID}/feed"
    params = {
        "message": message,
        "access_token": PAGE_ACCESS_TOKEN
    }
    response = requests.post(url, data=params)
    print(f"Posted to Facebook: {response.json()}")

# Check if it's an "every other Monday"
def is_post_day():
    today = datetime.now()
    first_monday = datetime(2025, 1, 6)  # adjust as needed
    delta = today.date() - first_monday.date()
    return delta.days % 14 == 0

def job_wrapper():
    if is_post_day():
        post_to_facebook()
    else:
        print("Not a post week. Skipping...")

# Schedule to run every Monday at 8 AM
scheduler = BlockingScheduler()
scheduler.add_job(job_wrapper, 'cron', day_of_week='mon', hour=8, minute=0)

print("Scheduler running...")
scheduler.start()
