import json

class TaskList:
    """docstring"""

    def __init__(self, path, root_task=None):

        if not path:
            self.root_task = root_task
        else:
            # TODO:  Flashcard for import json into dict
            with open(path, "r") as read_file:
                self.root_task = Task(
                    task_id='',
                    task_name='root',
                    subtasks= json.load(read_file)
                )

    # TODO: Revise to allow for decimal task id's
    def filter_tasks_by_id(self, composite_task_id):

        task_list = self.root_task.subtasks
        for id in composite_task_id:
            for task in task_list:
                if task.task_id == id:
                    task_list = task.subtasks
                    break

        print(task)
        print(TaskList(root_task=task))
        return TaskList(root_task=task) #todo


    def __repr__(self):
        output = []
        for subtask in self.root_task.subtasks:
            output.append(subtask.print())
        return ''.join(output)



class Task:
    """docstring"""

    def __init__(self, task_id, task_name, deadline=None, deadline_changes = {}, subtasks = [], complete=False):

        self.task_id = task_id
        self.name = task_name
        self.deadline = deadline
        self.deadline_changes = deadline_changes
        self.complete = complete


        # if subtasks is an array of dictionaries, Depth First Search
        if subtasks:
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

    def print(self,indent=0):
        indents = ' ' * indent
        checkbox = "☑" if self.complete else "☐"
        output = "{indents}{complete} {deadline} {task_id} {task_name}\n{subtasks}".format(
            indents = indents,
            task_id = self.task_id,
            task_name =  self.name,
            complete = checkbox,
            deadline = self.deadline,
            subtasks = ''.join([s.print(indent+4) for s in self.subtasks])
        )
        return output


    def __repr__(self):
        return self.print()

    # TODO: revise to allow for decimla task id's
    def add_subtask(self, task_name, deadline=None, deadline_changes = {}, subtasks = [], complete=False):
        prev_task_id = self.subtasks[-1]['task_id']
        new_task_id = Task.TASK_IDs[Task.TASK_IDs.find(prev_task_id) + 1]
        self.subtasks.append(
            Task(
                task_id = new_task_id,
                task_name = task_name,
                deadline=deadline,
                deadline_changes=deadline_changes,
                subtasks=subtasks,
                complete=complete
            )
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

t = TaskList('todo.json')
print(t)
# t.filter_by_task_id('a')
# print(t)
