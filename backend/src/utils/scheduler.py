from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from database.session import engine

jobstores = {"default": SQLAlchemyJobStore(engine=engine)}
scheduler = BackgroundScheduler(jobstores=jobstores)

scheduler.start()
