import json
import string

class TaskList:
    """docstring"""

    def __init__(self, path, global_task=None):

        if not path:
            self.global_task = global_task
        else:
            # TODO:  Flashcard for import json into dict
            with open(path, "r") as read_file:
                self.global_task = Task(
                    task_id='',
                    task_name='global',
                    subtasks= json.load(read_file)
                )

    def filter_by_task_id(self, composite_task_id):

        task_list = self.global_task.subtasks
        for id in composite_task_id:
            for task in task_list:
                if task.task_id == id:
                    task_list = task.subtasks
                    break

        print(task)
        return task
    #
    # def filter_by_date(self, date):
    #
    #     task_list = self.global_task.subtasks
    #
    #     for task in task_list:
    #         if task.name == task_name:
    #             break
    #         else:
    #             task_list = task.subtasks
    #
    #     print(task)

    def __str__(self):

        s = """
        Task Name: {task_name}
        Deadline: {deadline}
        Task ID: {task_id}
        """

        ret = []
        for task in self.global_task.subtasks:
            ret.append(
                s.format(
                    task_name = task.name,
                    deadline = task.deadline,
                    task_id = task.task_id
                )
            )
        return ''.join(ret)



class Task:
    """docstring"""

    TASK_IDs = string.ascii_letters + string.digits

    def __init__(self, task_id, task_name, deadline=None, deadline_changes = {}, subtasks = [], complete=False):

        self.task_id = task_id
        self.name = task_name
        self.deadline = deadline
        self.deadline_changes = deadline_changes
        self.complete = complete


        # if subtasks is an array of dictionaries, Depth First Search
        if subtasks:
            assert len(subtasks) < len(Task.TASK_IDs), "Maximum number of subtasks reached"
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



    def __str__(self):
        s = """
        Task Name: {task_name}
        Deadline: {deadline}
        Deadline Changes: {deadline_changes}
        """
        return s.format(
            task_name = self.name,
            deadline = self.deadline,
            deadline_changes = self.deadline_changes
        )

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
    # TODO:export to markdown for all of these views


# TODO: display an "error log" for each deferment as follows:
    # list summary statistics for each category of deferment
    # milestone_name
        # deferments of TaskList
            # deferment_date    task_name   from    to  category    justification
        # deferments of subtasks
            # deferment_date    task_name   from    to  category    justification

# TODO: implement function to filter deferments by category

t = TaskList('todo.json')
t.filter_by_task_id('a')
# print(t)
