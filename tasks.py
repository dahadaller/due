import json

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
                        complete = subtask['complete']
                    )
                )
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
            subtasks = task_dict.get('subtasks',[]),
        )

    @staticmethod
    def from_json_file(file_path):
        with open(file_path, "r") as read_file:
            return Task(
                task_name='root',
                subtasks= json.load(read_file)
            )

    def to_dict(self):
        return {
            'task_id': self.id,
            'task_name': self.name,
            'deadline': self.deadline,
            'deadline_changes': self.deadline_changes,
            'complete':self.complete,
            'subtasks':  [s.to_dict() for s in self.subtasks]
        }

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
            subtasks = subtasks
        )
        return output

    def __str__(self):
        if self.name == 'root' and self.id=='root':
            output = ''.join([s.to_string() for s in self.subtasks])
        else:
            output = self.to_string()
        return output

    def filter_by_id(self, task_id):

        task_list = self.subtasks

        for i, id in enumerate(task_id.split('.')):
            filtered = list(filter(lambda x: x.id == id, task_list))
            assert filtered, 'No task at index [{i}] of task id [{task_id}] Check that your task id is correct.'.format(i=i,task_id=task_id)
            task = filtered[0]
            task_list = task.subtasks

        return task

    def filter(self,callback):

        # base case: no subtasks
        if not self.subtasks:
            if callback(self):
                return Task(
                    task_id = self.id,
                    task_name = self.name,
                    deadline = self.deadline,
                    deadline_changes = self.deadline_changes,
                    # subtasks=
                    complete= self.complete
                )
            else:
                return None

        # inductive step: if filtered subtasks exist, recurse
        else:
            # filter subtasks
            fil_subtasks = []
            for subtask in self.subtasks:
                fil_subtask = subtask.filter(callback)
                if fil_subtask:
                    fil_subtasks.append(fil_subtask)

            if not fil_subtasks:
                return None
            else:
                return Task(
                    task_id = self.id,
                    task_name = self.name,
                    deadline = self.deadline,
                    deadline_changes = self.deadline_changes,
                    subtasks = fil_subtasks,
                    complete= self.complete
                )


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
# ---

# - argparse help menu setup

# - due today / due td
# - due tomorrow / due tm

# - due week (due this week) show  the week number, this week's date range, and all tasks due for the week
    # - due week +1 (due next week)
    # - due week -1 (due last week)
    # - due week 3 (due 3rd week of year)

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

# Flashcards to make:
    # using str.format() https://realpython.com/python-string-formatting/#2-new-style-string-formatting-strformat
    # the difference between __str__ and __rep__ https://realpython.com/python-print/#printing-custom-data-types
    # difference between static, class, and other method decorators in python classes https://realpython.com/instance-class-and-static-methods-demystified/
    # how to use if-else conditionals in list comprehension: https://stackoverflow.com/questions/4406389/if-else-in-a-list-comprehension
    # difference between json.loads() and json.load(): https://stackoverflow.com/questions/39719689/what-is-the-difference-between-json-load-and-json-loads-functions
    # how to load json data from and dump data to json files
    # how to dump json to file: https://stackoverflow.com/a/12309296/7215135
    # how to make a second constructor as I did with Task.from_json_file() and Task.from_dict(): https://www.geeksforgeeks.org/what-is-a-clean-pythonic-way-to-have-multiple-constructors-in-python/
    #
if __name__ = '__main__':

    # import from json file
    t = Task.from_json_file('todo.json')
    # add task
    g = Task(
        task_name =  'do thejsnflkiogndlkjfnglsjkdfgnlkj thing',
        deadline  = '2021-03-18'
    )
    # filter and add subtask
    t.filter_by_id('0.1').add_subtask(g)
    # print(t.filter(lambda x: x.name.startswith('sec'))) # filter by task name
    # print(t.filter(lambda x: x.deadline <= '2021-04-03')) #filter by deadline

    # write changes to file
    t.to_json_file('todo_2.json')

    # load from file once again
    l = Task.from_json_file('todo_2.json')
