from celery.task.schedules import crontab
from celery.decorators import periodic_task
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)

@periodic_task(
    run_every=(crontab(minute='*/1')),
    name="task_load_instruments",
    ignore_result=True
)
def task_koad_instruments():
    print("load instruments")
