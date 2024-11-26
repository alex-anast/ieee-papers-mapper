from apscheduler.schedulers.blocking import BlockingScheduler

scheduler = BlockingScheduler()
scheduler.add_job(data_extraction, "interval", hours=24)  # Run every 24 hours
scheduler.start()
