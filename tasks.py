# TODO: serialize data to json with default function for json.dump
    # https://stackoverflow.com/a/41200652/7215135
# TODO: create in-memory milestone list with subtasks (without deferments) and
    # serialize to json using "default" function argument in json.dumps
# TODO: find out how to deserialize json data into a milestone list complete with
    # task objects and deferment objects 


class Milestones:
    """docstring"""

    def __init__(self, path, task_list):

        if not path:
            self.data = task_list
        else:
            # TODO:  Flashcard for import json into dict

            with open(path, "r") as read_file:
                self.data = json.load(read_file)


    def to_json(self,path):
        with open(path, "w") as write_file:
            json.dump(self.data, write_file)


class Task:
    """docstring"""

    def __init__(self, task_name, deadline):

        self.name = task_name
        self.deadline = deadline

        self.deadline_changes = {}
        self.sub_tasks = {}


#
# class Deferment:
#     """docstring"""
#
#     def __init__(self, deferment_date):
#         self.date = deferment_date
#         self.from = None
#         self.to =  None
#         self.category = None
#         self.justification = None
#
#
#
#     # edit this to print the task and all subtasks in a really pretty way.
#     # https://realpython.com/operator-function-overloading/#printing-your-objects-prettily-using-str
#     def __str__(self):
#         pass


# DISPAY INTERFACE
    # TODO: SHOW MILESTONES AND ALL SUBTASKS: show milestones until given date along with all the subtasks and their due dates
    # TODO: SHOW THIS WEEK'S TASKS: generate a list of all tasks due at the end of the week
    # TODO: SHOW TODAY'S TASKS: generate a list of all tasks for today, sorted by milestone
    # TODO:export to markdown for all of these views


# TODO: display an "error log" for each deferment as follows:
    # list summary statistics for each category of deferment
    # milestone_name
        # deferments of Milestones
            # deferment_date    task_name   from    to  category    justification
        # deferments of sub_tasks
            # deferment_date    task_name   from    to  category    justification
# TODO: implement function to filter deferments by category
