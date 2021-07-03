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

TASK_FILE_PATH = Path(config['task_file'])

COLOR = Theme(config['color'])
# custom_theme = Theme({
#     "info" : "dim cyan",
#     "warning": "magenta",
#     "danger": "bold red"
# })
# console = Console(theme=custom_theme)
# console.print("This is information", style="info")
# console.print("[warning]The pod bay doors are locked[/warning]")
# console.print("Something terrible happened!", style="danger")


# # TODO: these are to format output. I may not want to see the dates, year component of dates, or only tasks that aren't done.
# # Find out how to use rich to format output of task tree. Colors and unicode checkboxes would be nice.
# no_dates = kwargs['nodates']
# no_year = kwargs['noyear']


