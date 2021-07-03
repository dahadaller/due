import json
import argparse
import calendar
from datetime import datetime, date, timedelta
from itertools import chain
from pathlib import Path

from rich.console import Console
# from rich import print as rprint
from rich.tree import Tree


from due import CAL_STR, TODAY, WEEK_BEGIN, WEEK_END, TASK_TREE, TASK_FILE_PATH, COLOR
from due.tasks import TaskTree

class Commands:

    @staticmethod
    def valid_date(date_string):
        try:
            return datetime.strptime(date_string, "%Y-%m-%d").date()
        except ValueError:
            msg = f"Not a valid date: '{date_string}'. Use YYYY-MM-DD format"
            raise argparse.ArgumentTypeError(msg)

    @staticmethod
    def valid_id(id_string):
            if id_string in TASK_TREE.tree.nodes:
                return id_string
            else:
                msg = f"Id not found in task tree: '{id_string}'"
                raise argparse.ArgumentTypeError(msg)

    @staticmethod
    def highlight_dates(cal_str, begin_date, end_date):
        pass
        # print(begin_date, end_date)

        # cal_list = list(cal_str)

        # highlight_text = u"\u001b[7m" # ansi code for "reversed" (highlighted) text
        # reset = u"\u001b[0m" #reset ansi to default

        # begin = begin_date.strftime(' %-d ')
        # end = end_date.strftime(' %-d ')

        # begin_idx = cal_str.rfind(begin) + 1
        # end_idx = cal_str.rfind(end) + len(begin)

        # cal_list.insert(begin_idx,highlight_text)
        # cal_list.insert(end_idx,reset)

        # return ''.join(cal_list)

    @classmethod
    def display_today(*args,**kwargs):
        pass
        # TASK_TREE = TASK_TREE
        # print(Commands.highlight_dates(CAL_STR, TODAY, TODAY))
        # print(TASK_TREE
        #     .due_by(TODAY.strftime('%Y-%m-%d'))
        #     .search(lambda task: not task.complete))

    @classmethod
    def display_tomorrow(*args, **kwargs):
        pass
        # TASK_TREE = TASK_TREE
        # tomorrow = TODAY + timedelta(days=1)
        # print(Commands.highlight_dates(CAL_STR, tomorrow, tomorrow))
        # print(TASK_TREE
        #     .due_by(tomorrow.strftime('%Y-%m-%d'))
        #     .search(lambda task: not task.complete))

    @classmethod
    def display_week(*args, **kwargs):
        pass
        # print(Commands.highlight_dates(CAL_STR,WEEK_BEGIN,WEEK_END))
        # print(TASK_TREE.due_by(WEEK_END.strftime('%Y-%m-%d')))

    @classmethod
    def add_task(*args, **kwargs):
        pass
        # TASK_TREE = TASK_TREE

        # # positional arguments from command line:
        # id = kwargs['parent_id']
        # task_name = kwargs['child_task_name']
        # deadline = kwargs['child_task_deadline']

        # # add subtask to task tree and print result to terminal
        # TASK_TREE.get_subtask(id).add_subtask(
        #     TaskTree(
        #         task_name =  task_name,
        #         deadline =  deadline
        #     )
        # )
        # print(TASK_TREE)

        # # repeated tasks (optional)

        # # save task tree to json file
        # TASK_TREE.to_json_file()

    @classmethod
    def rm_task(*args, **kwargs):
        pass

    @classmethod
    def complete_task(*args, **kwargs):
        pass

    @classmethod
    def uncomplete_task(*args, **kwargs):
        pass

    @classmethod
    def ls(*args, **kwargs):

        # PARSE COMMAND LINE ARGUMENTS
        depth = kwargs['depth']
        deadline = kwargs['deadline']
        root_id = kwargs['id']

        if kwargs['done'] == True: # TODO: --done flag will not produce a complete tree because children can be completed before parents and so there's no way to get to parents. need to use "promote" algorithm to elevate children in this case.
            completion_status = True
        elif kwargs['undone'] == True: 
            completion_status = False
        else:
            completion_status = None

        # LOAD TASK TREE FROM JSON
        task_tree = TASK_TREE.depth_limit(depth).due_by(deadline).completed(completion_status)

        # PARSE CONFIG FILE CONTENTS
        cons = Console(theme=COLOR)

        # CREATE RICH TEXT TREE
        display_tree = Tree(f"[task_id]{root_id}[/task_id]")

        def dfs(node,display_tree):

            for neighbor in task_tree.tree.adj[node]:

                attr = task_tree.tree.nodes[neighbor]

                if attr['complete']:

                    line = f"[complete]{neighbor} {attr['task_name']} {attr['deadline']}[/complete]"

                else:
                    line = (
                        f"[task_id]{neighbor}[/task_id] "
                        f"[task_name]{attr['task_name']}[/task_name] " 
                        f"[deadline]{attr['deadline']}[/deadline]" 
                    )

                # the tree.add() method returns a pointer to the node that was just added
                branch = display_tree.add(line)
                dfs(neighbor,branch)
            
            return display_tree

        display_tree = dfs(root_id,display_tree)

        cons.print(kwargs,'\n')
        cons.print(display_tree)

    

    # @classmethod 
    # init(*args,**kwargs):
    #     # TODO: this function should create a new todo.json file in default location 
    #     # if such a file already exists, then the user is asked to provide the filename in order to confirm erasing the tasks file
    #     # can also init from a file in another location, which should change where due looks for thie todo.json in the future.
    #     pass

