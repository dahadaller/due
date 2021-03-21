import json
import argparse
import calendar

from datetime import datetime, date, timedelta
from itertools import chain

class Task:
    """docstring"""

    def __init__(self, task_name, task_id='root', deadline=None,complete=False, deadline_changes = {}, subtasks = []):

        self.id = task_id
        self.name = task_name
        self.deadline = deadline
        self.deadline_changes = {k:v for k,v in deadline_changes.items()}
        self.complete = complete

        # if subtasks is an array of dictionaries, Depth First Search
        # if isinstance(subtasks, dict):
        if subtasks and isinstance(subtasks[0],dict):
            self.subtasks = []
            for subtask in subtasks:
                self.subtasks.append(
                    Task(
                        task_id = subtask['task_id'],
                        task_name = subtask['task_name'],
                        deadline = subtask['deadline'],
                        deadline_changes = subtask['deadline_changes'],
                        subtasks = subtask['subtasks'],
                        complete = subtask['complete']))
        # if subtasks is empty or is an array of Task objects
        else:
            self.subtasks = subtasks

    @staticmethod
    def from_dict(task_dict):
        return Task(
            task_id = task_dict.get('task_id','root'),
            task_name = task_dict.get('task_name','root'),
            deadline = task_dict.get('deadline',None),
            complete = task_dict.get('complete',False),
            deadline_changes = task_dict.get('deadline_changes',{}),
            subtasks = task_dict.get('subtasks',[]))

    @staticmethod
    def from_json_file(file_path):
        with open(file_path, "r") as read_file:
            return Task(
                task_name='root',
                subtasks= json.load(read_file))

    def to_dict(self):
        return {
            'task_id': self.id,
            'task_name': self.name,
            'deadline': self.deadline,
            'deadline_changes': self.deadline_changes,
            'complete':self.complete,
            'subtasks':  [s.to_dict() for s in self.subtasks]}

    def to_json_file(self, file_path):
        with open(file_path,'w') as write_file:
            json.dump([s.to_dict() for s in self.subtasks], write_file, indent=4)

    def to_string(self, indent=0, max_depth=None):
        if max_depth is not None:
            if max_depth > 0:
                subtasks = ''.join([s.to_string(indent+4, max_depth-1) for s in self.subtasks])
            else:
                subtasks = ''
        else:
            subtasks = ''.join([s.to_string(indent+4) for s in self.subtasks])

        indents = ' ' * indent
        checkbox = "☑" if self.complete else "☐"
        output = "{indents}{complete} {deadline} {task_id} {task_name}\n{subtasks}".format(
            indents = indents,
            task_id = self.id,
            task_name =  self.name,
            complete = checkbox,
            deadline = self.deadline,
            subtasks = subtasks)
        return output

    def __str__(self):
        if self.name == 'root' and self.id=='root':
            output = ''.join([s.to_string() for s in self.subtasks])
        else:
            output = self.to_string()
        return output

    def search(self,callback):

        # base case: no subtasks
        if not self.subtasks:
            if callback(self):
                return Task(
                    task_id = self.id,
                    task_name = self.name,
                    deadline = self.deadline,
                    deadline_changes = self.deadline_changes,
                    # subtasks=
                    complete= self.complete)
            else:
                return None

        # inductive step: check filtered subtasks postorder dfs (children, root)
        else:
            # filter subtasks (recurse on children)
            fil_subtasks = [s.search(callback) for s in self.subtasks]
            fil_subtasks = [s for s in fil_subtasks if s is not None]

            # if parent's subtasks match filter, keep parent.
            if fil_subtasks:
                return Task(
                    task_id = self.id,
                    task_name = self.name,
                    deadline = self.deadline,
                    deadline_changes = self.deadline_changes,
                    subtasks = fil_subtasks,
                    complete= self.complete)
            # if parent itself matches filter, keep parent
            else:
                if callback(self):
                    return Task(
                        task_id = self.id,
                        task_name = self.name,
                        deadline = self.deadline,
                        deadline_changes = self.deadline_changes,
                        # subtasks=
                        complete= self.complete)
                # otherwise don't keep
                else:
                    return None

    def promote(self,callback):

        # base case: no subtasks
        if not self.subtasks:
            if callback(self):
                return tuple([Task(
                    task_id = self.id,
                    task_name = self.name,
                    deadline = self.deadline,
                    deadline_changes = self.deadline_changes,
                    # subtasks=
                    complete= self.complete)])
            else:
                return tuple()

        # inductive step: check if subtasks should be promoted postorder dfs (children, then root)
        else:

            # if parent matches, keep parent along with all children
            if callback(self):
                return tuple([Task(
                    task_id = self.id,
                    task_name = self.name,
                    deadline = self.deadline,
                    deadline_changes = self.deadline_changes,
                    subtasks = self.subtasks,
                    complete= self.complete)])

            # if parent doesn't match, promote children in it's place
            else:

                # promte subtasks (recurse on children)
                promoted_subtasks = [s.promote(callback) for s in self.subtasks]
                promoted_subtasks = list(chain(*promoted_subtasks)) # flatten list
                # promoted_subtasks = [item for sublist in promoted_subtasks for item in sublist] #flatten
                promoted_subtasks = [ps for ps in promoted_subtasks if ps is not None] # remove None values
                # [print(t) for t in promoted_subtasks]

                ret = []
                for subtask in promoted_subtasks:
                    ret.append(Task(
                        task_id = subtask.id,
                        task_name = subtask.name,
                        deadline = subtask.deadline,
                        deadline_changes = subtask.deadline_changes,
                        subtasks = subtask.subtasks,
                        complete= subtask.complete))
                return tuple(ret)

    def due_by(self, deadline):
        # display method to be run on the root task only
        root_copy = Task(
            task_id = self.id,
            task_name = self.name,
            deadline = self.deadline,
            deadline_changes = self.deadline_changes,
            subtasks= [],
            complete= self.complete)

        for milestone in self.subtasks:

            milestone_copy = Task(
                task_id = milestone.id,
                task_name = milestone.name,
                deadline = milestone.deadline,
                deadline_changes = milestone.deadline_changes,
                subtasks = [],
                complete = milestone.complete)

            for subtask in milestone.subtasks:
                promoted = subtask.promote(lambda x: x.deadline <= deadline)
                for p in promoted:
                    milestone_copy.subtasks.append(p)

            root_copy.subtasks.append(milestone_copy)

        return root_copy

    def next_id(self):
        id = self.id
        id = list(id.rpartition('.'))
        id[-1] = int(id[-1]) + 1
        id[-1] = str(id[-1])
        id = ''.join(id)
        return id

    def add_subtask(self, subtask):
        if self.subtasks:
            subtask.id = self.subtasks[-1].next_id()
        else:
            subtask.id = 0
        self.subtasks.append(subtask)
        return self

    def get_subtask(self, subtask_id):

        task_list = self.subtasks
        digits_so_far = []

        for id_digit in subtask_id.split('.'):
            filtered = list(filter(lambda x: x.id == id_digit, task_list))
            if not filtered:
                # TODO: maybe this print statement shold be a part of the parser
                print('No subtasks under task {digits_so_far} Check that your input,  {subtask_id}, is correct.'.format(digits_so_far='.'.join(digits_so_far), subtask_id=subtask_id))
                return
            task = filtered[0]
            task_list = task.subtasks
            digits_so_far.append(id_digit)

        return task

class Main:
    today = datetime.today()

    cal_str = calendar.TextCalendar(calendar.SUNDAY).formatmonth(today.year, today.month)
    task_tree = Task.from_json_file('todo.json') # TODO:  how can I change this to another file if i need to? or even another file type?

    week_begin = today - timedelta(days=(today.weekday()+1)) #week begins on sunday
    week_end = today + timedelta((calendar.SATURDAY-today.weekday()) % 7 ) # week ends on saturday

    @staticmethod
    def highlight_dates(cal_str, begin_date, end_date):

        cal_list = list(cal_str)

        highlight_text = u"\u001b[7m" # ansi code for "reversed" (highlighted) text
        reset = u"\u001b[0m" #reset ansi to default

        begin = begin_date.strftime('%d')
        end = end_date.strftime('%d')

        begin_idx = cal_str.rfind(begin)
        end_idx = cal_str.rfind(end) + 1 + len(begin)

        cal_list.insert(begin_idx,highlight_text)
        cal_list.insert(end_idx,reset)

        return ''.join(cal_list)

    @classmethod
    def display_today(*args):
        cal_str, today, task_tree, highlight_dates = Main.cal_str, Main.today, Main.task_tree, Main.highlight_dates
        print(highlight_dates(cal_str, today, today))
        print(task_tree
            .due_by(today.strftime('%Y-%m-%d'))
            .search(lambda task: not task.complete))

    @classmethod
    def display_tomorrow(*args):
        cal_str, today, task_tree, highlight_dates = Main.cal_str, Main.today, Main.task_tree, Main.highlight_dates
        tomorrow = today + timedelta(days=1)
        print(highlight_dates(cal_str, tomorrow, tomorrow))
        print(task_tree
            .due_by(tomorrow.strftime('%Y-%m-%d'))
            .search(lambda task: not task.complete))

    @classmethod
    def display_week(*args):
        cal_str, task_tree, week_begin, week_end, highlight_dates = Main.cal_str, Main.task_tree, Main.week_begin, Main.week_end, Main.highlight_dates
        print(highlight_dates(cal_str,week_begin,week_end))
        print(task_tree.due_by(week_end.strftime('%Y-%m-%d')))


if __name__ == '__main__':

    # due
    due = argparse.ArgumentParser(prog='due')
    subcommands = due.add_subparsers()

    # due today
    today = subcommands.add_parser('today', aliases=['td'])
    today.set_defaults(func=Main.display_today)

    # due tomorrow
    tomorrow = subcommands.add_parser('tomorrow', aliases=['tm'])
    tomorrow.set_defaults(func=Main.display_tomorrow)

    # due week
    week = subcommands.add_parser('week', aliases=['we','w'])
    week.set_defaults(func=Main.display_week)

    # parse arguments and run
    args = due.parse_args()
    args.func()

# TODO
# ---

# the following functions should modify the source json file in addition to the task objects
# - due add --id 1.0 'task name' 'deadline'
# - due add --id 1.0 'task name' 'deadline' --repeat 'weekly:smtwtfs' --until 'date'
#     - --repeat daily
#     - --repeat weekly:smtwtfs
#     - --repeat monthly
#     - --repeat yearly
#     * extra feature: accept cron job syntax here
#     * extra feature: 'custom' monthly feature like "once every 2nd tuesday of the month"
# - due rm --id 1.0
# - due done --id 1.0 / due  --id 1.0
# - due reschedule --id 1.0 'new deadline' / due res -i 1.0 'new deadline' (remember to store when this deadline was originally scheduled in deadline_changes attribute)

# - due (by itself, this should show everything due today, over your weekly todo list)

# - due ls --id 1.0 --depth 3 / due -i 1.0 -d 3 (list single list or subtask)
# - due ls -- all / due ls -a (list all tasks including completed tasks)
# - due ls / due (list all tasks that are uncompleted)

# find out how to set up virtual environment
# - due ls --json (pipe out json to other applications)
# - due ls --yaml (pipe out yaml to other applications)
# - due ls --md (pipe out mardkown to other applications)

# - due backup --yaml 'filename.yaml'
# - due backup --json 'filename.json'

#  figure out how to set the default file to search for to make the root task/task tree.
# - argparse help menu setup

# - due week +1 (due next week)
# - due week -1 (due last week)
# - due week 3 (due 3rd week of year)

# * extra feature: use tree structure for tasks like this: https://stackoverflow.com/a/59109706/7215135
# ├── package
# │   ├── __init__.py
# │   ├── __main__.py
# │   ├── subpackage
# │   │   ├── __init__.py
# │   │   ├── __main__.py
# │   │   └── module.py
# │   └── subpackage2
# │       ├── __init__.py
# │       ├── __main__.py
# │       └── module2.py
# └── package2
#     └── __init__.py

# * extra feature: add week number loading bar to the today, week, tomorrow display functions.
# * extra feature: add loading bar for specific milestones to show how close until deadline

# * extra feature: you could add a utility to gather # TODO's from code with
    # lines of text, filenames, and project names which could be added to your milestone tasks
    # you could assign deadlines to them later on

# TODO: display an "error log" for each deferment as follows:
    # list summary statistics for each category of deferment
    # milestone_name
        # deferments of TaskList
            # deferment_date    task_name   from    to  category    justification
        # deferments of subtasks
            # deferment_date    task_name   from    to  category    justification

# TODO: implement function to filter deferments by category

# TODO: put type hints in all functions

# Flashcards to make:
    # using str.format() https://realpython.com/python-string-formatting/#2-new-style-string-formatting-strformat
    # the difference between __str__ and __rep__ https://realpython.com/python-print/#printing-custom-data-types
    # difference between static, class, and other method decorators in python classes https://realpython.com/instance-class-and-static-methods-demystified/
    # how to use if-else conditionals in list comprehension: fil_subtasks = [s for s in fil_subtasks if s is not None]  https://stackoverflow.com/questions/4406389/if-else-in-a-list-comprehension
    # difference between json.loads() and json.load(): https://stackoverflow.com/questions/39719689/what-is-the-difference-between-json-load-and-json-loads-functions
    # how to load json data from and dump data to json files
    # how to dump json to file: https://stackoverflow.com/a/12309296/7215135
    # how to make a second constructor as I did with Task.from_json_file() and Task.from_dict(): https://www.geeksforgeeks.org/what-is-a-clean-pythonic-way-to-have-multiple-constructors-in-python/
    # how you get today's date from datetime:     datetime.today().strftime('%Y-%m-%d')
    # how to flatten a list in python: flattened_l = [item for sublist in l for item in sublist]
    # read the following articles and make flashcards: https://pymotw.com/3/datetime/index.html  https://pymotw.com/3/time/index.html

# Examples for documentation
    # # print(t.filter(lambda x: x.deadline == datetime.today().strftime('%Y-%m-%d')))
    # print('↓search↓')
    # print(t.search(lambda x: x.complete == True))
    #
    # print('↓promote↓')
    # for s1 in t.subtasks:
    #     for s2 in s1.promote(lambda x: x.deadline <= '2021-03-18'):
    #         print(s2)
    #


# DONE
# ---
# - due today / due td
# - due tomorrow / due tm
# - due week (due this week) show  the week number, this week's date range, and all tasks due for the week
