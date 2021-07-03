import calendar
from datetime import datetime, date, timedelta

from due.configparse import TASK_FILE_PATH, COLOR
from due.tasks import TaskTree

# declare version
__version__ = "1.0.0"

# load config yaml from configparse into this namespace
TASK_FILE_PATH = TASK_FILE_PATH
COLOR = COLOR

# get dates from system
TODAY = datetime.today()
CAL_STR = calendar.TextCalendar(calendar.SUNDAY).formatmonth(TODAY.year, TODAY.month)
WEEK_BEGIN = TODAY - timedelta(days=(TODAY.weekday()+1) % 7) #week begins on sunday
WEEK_END = TODAY + timedelta((calendar.SATURDAY-TODAY.weekday()) % 7 ) # week ends on saturday

# load task tree from json
TASK_TREE = TaskTree.load()