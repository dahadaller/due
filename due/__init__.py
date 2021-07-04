import calendar
from datetime import datetime, date, timedelta

from due.configparse import TASK_FILE_PATH, COLOR
from due.tasks import TaskTree

# declare version
__version__ = "1.0.0"

# load config yaml from configparse into this namespace
TASK_FILE_PATH = TASK_FILE_PATH
COLOR = COLOR

# get today's date
TODAY = datetime.today()

# create calendar for this month
CAL_STR = calendar.TextCalendar(firstweekday=6).formatmonth(TODAY.year, TODAY.month)

# load task tree from json
TASK_TREE = TaskTree.load()