from pathlib import Path
import calendar
from datetime import datetime, date, timedelta

import yaml

__version__ = "1.0.0"


config_path = Path(__file__).parent / 'config.yaml'

with config_path.open(mode='r') as config_file:
    config = yaml.load(config_file, Loader=yaml.FullLoader)

TASK_FILE_PATH = Path(config['task_file']).resolve()
print(str(TASK_FILE_PATH))

TODAY = datetime.today()
CAL_STR = calendar.TextCalendar(calendar.SUNDAY).formatmonth(TODAY.year, TODAY.month)
WEEK_BEGIN = TODAY - timedelta(days=(TODAY.weekday()+1) % 7) #week begins on sunday
WEEK_END = TODAY + timedelta((calendar.SATURDAY-TODAY.weekday()) % 7 ) # week ends on saturday
