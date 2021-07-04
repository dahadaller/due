from pathlib import Path

import yaml
from rich.theme import Theme

# this configparse.py file exists to avoid circular import between __init__.py and tasks.py:
    # tasks.py uses 'from due import TASK_FILE_PATH'
    # __init__.py uses 'from due.tasks import TaskTree'

# import configuration data from config.yaml
CONFIG_PATH = Path(__file__).parent / 'config.yaml'

with CONFIG_PATH.open(mode='r') as config_file:
    config = yaml.load(config_file, Loader=yaml.FullLoader)

# assign config data to variables
TASK_FILE_PATH = Path(config['task_file'])
COLOR = Theme(config['color'])


