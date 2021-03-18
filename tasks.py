import json

class Task:
    """docstring"""

    def __init__(self, task_id, task_name, deadline=None, deadline_changes = {}, subtasks = [], complete=False):

        self.task_id = task_id
        self.name = task_name
        self.deadline = deadline
        self.deadline_changes = deadline_changes
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
                        deadline_changes = {k:v for k,v in subtask['deadline_changes'].items()},
                        subtasks = subtask['subtasks'],
                        complete = subtask['complete']
                    )
                )
        # if subtasks is empty or is an array of Task objects
        else:
            self.subtasks = subtasks

    @staticmethod
    def from_json(file_path):
        with open(file_path, "r") as read_file:
            t = Task(task_id='root',
                task_name='root',
                subtasks= json.load(read_file))
        return t

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
            task_id = self.task_id,
            task_name =  self.name,
            complete = checkbox,
            deadline = self.deadline,
            subtasks = subtasks
        )
        return output


    def __repr__(self):
        if self.name == 'root' and self.task_id=='root':
            output = ''.join([s.to_string() for s in self.subtasks])
        else:
            output = self.to_string()
        return output

    # TODO: revise to allow for decimal task id's
    # def add_subtask(self, task_name, deadline=None, deadline_changes = {}, subtasks = [], complete=False):
    #     prev_task_id = self.subtasks[-1]['task_id']
    #     new_task_id = Task.TASK_IDs[Task.TASK_IDs.find(prev_task_id) + 1]
    #     self.subtasks.append(
    #         Task(
    #             task_id = new_task_id,
    #             task_name = task_name,
    #             deadline=deadline,
    #             deadline_changes=deadline_changes,
    #             subtasks=subtasks,
    #             complete=complete
    #         )
    #     )

    def filter_by_id(self, task_id):

        task_list = self.subtasks

        for i, id in enumerate(task_id.split('.')):
            filtered = list(filter(lambda x: x.task_id == id, task_list))
            assert filtered, 'No task at index [{i}] of task id [{task_id}] Check that your task id is correct.'.format(i=i,task_id=task_id)
            task = filtered[0]
            task_list = task.subtasks

        return task

    def filter(self,callback):

        # base case: no subtasks
        if not self.subtasks:
            if callback(self):
                return Task(
                    task_id = self.task_id,
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
                    task_id = self.task_id,
                    task_name = self.name,
                    deadline = self.deadline,
                    deadline_changes = self.deadline_changes,
                    subtasks = fil_subtasks,
                    complete= self.complete
                )







# DISPAY INTERFACE
    # TODO: SHOW TaskList AND ALL SUBTASKS: show TaskList until given date along with all the subtasks and their due dates
        # print yaml to terminal
    # TODO: SHOW THIS WEEK'S TASKS: generate a list of all tasks due at the end of the week, by milestone
        # import yaml to task objects
        # filter all task objects in list by date
            # use datetime methods to create string for end of week
    # TODO: SHOW TODAY'S TASKS: generate a list of all tasks for today, sorted by milestone
    # TODO:export to markdown/yaml for all of these views?


# TODO: display an "error log" for each deferment as follows:
    # list summary statistics for each category of deferment
    # milestone_name
        # deferments of TaskList
            # deferment_date    task_name   from    to  category    justification
        # deferments of subtasks
            # deferment_date    task_name   from    to  category    justification

# TODO: implement function to filter deferments by category

t = Task.from_json('todo.json')
# print(t)
# print(t.filter_by_id('0'))
print(t.filter(lambda x: x.name.startswith('sec'))) # filter by task name
print(t.filter(lambda x: x.deadline <= '2021-04-03')) #filter by deadline

# print(t)
