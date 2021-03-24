import json
import argparse
import calendar
from datetime import datetime, date, timedelta
from itertools import chain
from pathlib import Path

class Task:
    """
    A class that represents a Task. This is a recursive class, so subtasks
    are also Task objects, and so we can form trees from Tasks. The root
    task of such a tree is treated as a dummy node that allows us to traverse
    the Tasks in the tree.

    ...

    Attributes
    ----------
    id : str
        The id of a Task is a period-delimited numeric string (eg. "1.0.2.3")
        that uniquely identifies a task. The id can be of variable length
        and represents the position of the Task in the Task/Subtask heirarchy
        tree. The root subtask has a task id of "root". For example, one
        heirarchy looks like this: "root" > "1" > "1.0" > "1.0.2" > "1.0.2.3",
        where ">" means "is parent task to" in this case. (default 'root')
    name : str
        The name of a Task desccribes what should be done to complete some
        objective.
    kind : str
        The kind of task (root, empty, None) distinguishes what kind of node
        the Task object is. Task objects that are not subtasks are root.
        Task objects with no Attributes are empty.
    deadline : str
        The deadline is a date in format date.strftime('%Y-%m-%d'),
        eg. 2021-03-21. The deadline is a date by which the task should be
        completed.(default  None)
    complete : bool
        The complete attribute indicates whether a task has been marked as
        completed or not. Tasks where complete = True will show a checked box
        in the CLI interface.(default  False)
    deadline_changes:  dict
        If deadlines are ever pushed back for a given task, that information is
        recorded here. In this dictionary, the keys are date-strings with the
        date.strftime('%Y-%m-%d') format, and the values are strings indicating
        the reason that the task could not be completed on the key date.
        (default  {})
    subtasks: list
        This is a list of child Tasks which should be completed before the
        parent task can be marked as completed. (default [])

    Methods
    -------
    says(sound=None)
        Prints the animals name and what sound it makes
    """

    def __init__(self, task_name, task_id='root', task_kind=None, deadline=None, complete=False, deadline_changes = {}, subtasks = []):

        """
        Creates an instance of a Task. Note that, if subtasks is a list of
        dictionaries instead of a list of Task objects, __init__ will recurse
        into the subtasks list and initialize Tasks from those dictionaries.

        Parameters
        ----------
        task_name : str
            The name of a Task desccribes what should be done to complete some
            objective.
        task_id : str, optional
            The id of a Task is a period-delimited numeric string (eg. "1.0.2.3")
            that uniquely identifies a task. The id can be of variable length
            and represents the position of the Task in the Task/Subtask heirarchy
            tree. The root subtask has a task id of "root". For example, one
            heirarchy looks like this: "root" > "1" > "1.0" > "1.0.2" > "1.0.2.3",
            where ">" means "is parent task to" in this case. (default 'root')
        task_kind : str, optional
            The kind of task (root, empty, None) distinguishes what kind of node
            the Task object is. Task objects that are not subtasks are root.
            Task objects with no Attributes are empty.
        deadline : str, optional
            The deadline is a date in format date.strftime('%Y-%m-%d'),
            eg. 2021-03-21. The deadline is a date by which the task should be
            completed.(default  None)
        complete : bool, optional
            The complete attribute indicates whether a task has been marked as
            completed or not. Tasks where complete = True will show a checked box
            in the CLI interface.(default  False)
        deadline_changes:  dict, optional
            If deadlines are ever pushed back for a given task, that information is
            recorded here. In this dictionary, the keys are date-strings with the
            date.strftime('%Y-%m-%d') format, and the values are strings indicating
            the reason that the task could not be completed on the key date.
            (default  {})
        subtasks: list, optional
            This is a list of child Tasks which should be completed before the
            parent task can be marked as completed. (default [])
        """
        self.id = task_id
        self.name = task_name
        self.deadline = deadline
        self.deadline_changes = {k:v for k,v in deadline_changes.items()}
        self.complete = complete
        self.kind = task_kind

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
    def empty():
        return Task(
            task_name = '',
            task_id = '',
            task_kind='empty',
            deadline = '',
            complete = None,
            deadline_changes = {},
            subtasks = []
        )

    @staticmethod
    def from_dict(task_dict):
        """
        Creates an instance of a Task from a dictionary. Note that, if there
        exists a "subtasks" key in this dictionary with a value that is a
        list of other dictionaries, this staticmethod will recurseively
        create Task instances from those dictionaries as well.

        Parameters
        ----------
        task_dict: dict
            A dictionary that mirrors the structure of the Task object with keys
            task_id, task_name, deadline, complete, deadline_changes, and subtasks.
            All keys are optional. If a key and it's value aren't provided,
            a default will be set. The defaults are listed below
                task_id: 'root'
                task_name: 'root'
                deadline: None
                complete: False
                deadline_changes: {}
                subtasks: []
        """
        return Task(
            task_id = task_dict.get('task_id','root'),
            task_name = task_dict.get('task_name','root'),
            deadline = task_dict.get('deadline',None),
            complete = task_dict.get('complete',False),
            deadline_changes = task_dict.get('deadline_changes',{}),
            subtasks = task_dict.get('subtasks',[]))

    @staticmethod
    def from_json_file(file_path):
        """
        Creates a root task, and then assigns all tasks in a json file
        as subtasks to this root task.

        Parameters
        ----------
        file_path: str
            The file path where the json file is located.
        """
        with open(file_path, "r") as read_file:
            return Task(
                task_name='root',
                subtasks= json.load(read_file))

    def to_dict(self):
        """
        Creates a dictionary from a Task object, and recurseively creates
        dictionaries for any Task objects in the subtasks list.
        """
        return {
            'task_id': self.id,
            'task_name': self.name,
            'deadline': self.deadline,
            'deadline_changes': self.deadline_changes,
            'complete':self.complete,
            'subtasks':  [s.to_dict() for s in self.subtasks]}

    def to_json_file(self, file_path):
        """
        Creates a JSON file from the subtasks of  a root Task object (id='root')

        Raises
        ------
        AssertionError
            If the task upon which this method is called is not a root task,
            i.e. id=root.
        """
        assert self.id == 'root', "Can only export root task to JSON."

        with open(file_path,'w') as write_file:
            json.dump([s.to_dict() for s in self.subtasks], write_file, indent=4)

    def to_string(self, indent=0, max_depth=None, full_id='', show_id=True, show_deadline=True, show_year=True, color=False):

        if self.id == 'root':
            full_id = ''
        elif full_id == '':
            full_id = self.id
        else:
            full_id = full_id + "." + self.id

        if not self.deadline:
            deadline = ''
        elif not show_year:
            deadline = self.deadline[5:]
        else:
            deadline = self.deadline


        if self.kind == 'empty' or self.id == 'root':
            checkbox = ''
        elif self.complete:
            checkbox = "☑"
        else:
            checkbox = "☐"


        indents = ' ' * indent

        magenta = "\u001b[35m"
        cyan = "\u001b[36m"
        reset_color = "\u001b[0m"

        # recurse to create subtasks
        if max_depth is not None:
            if max_depth > 0:
                subtasks = ''.join([s.to_string(indent=indent+4, max_depth=max_depth-1, full_id=full_id,color=color,show_id=show_id, show_deadline=show_deadline, show_year=show_year,) for s in self.subtasks])
            else:
                subtasks = ''
        else:
            subtasks = ''.join([s.to_string(indent=indent+4,full_id=full_id,color=color,show_id=show_id, show_deadline=show_deadline, show_year=show_year,) for s in self.subtasks])


        output = "{indents}{checkbox} {task_name} {color_1}{deadline}{reset} {color_2}{full_id}{reset}\n{subtasks}".format(
            indents = indents,
            full_id = full_id if show_id else '',
            task_name = self.name,
            checkbox = checkbox,
            deadline = deadline if show_deadline else '',
            subtasks = subtasks,
            color_1 = magenta if color else '',
            color_2 = cyan if color else '',
            reset = reset_color if color else '')
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

    def remove_subtask(self,id_digit):
        #TODO: if no such task with ID exists, an error message should be printed
        self.subtasks = [s for s in self.subtasks if s.id != id_digit]
        return self

    def get_subtask(self, subtask_id):

        # for root task id
        if self.id == 'root' and subtask_id == 'root':
            return self

        # for numerical, period-delimited task ids
        task_list = self.subtasks
        digits_so_far = []

        for id_digit in subtask_id.split('.'):
            filtered = list(filter(lambda x: x.id == id_digit, task_list))
            if not filtered:
                # TODO: maybe this print statement shold be a part of the parser
                print('No subtasks under task {digits_so_far} Check that your input,  {subtask_id}, is correct.'.format(digits_so_far='.'.join(digits_so_far), subtask_id=subtask_id))
                return Task.empty() # return empty task
            task = filtered[0]
            task_list = task.subtasks
            digits_so_far.append(id_digit)

        return task
