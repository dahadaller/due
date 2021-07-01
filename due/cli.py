import json
import argparse
import calendar
from datetime import datetime, date, timedelta
from itertools import chain
from pathlib import Path

from rich import print
from rich.tree import Tree

from due.tasks import TaskTree
from due import CAL_STR, TODAY, WEEK_BEGIN, WEEK_END, TASK_FILE_PATH


class Commands:
    task_tree = TaskTree.load() # TODO: is there a way to put this in __init__.py?

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
        # task_tree = Commands.task_tree
        # print(Commands.highlight_dates(CAL_STR, TODAY, TODAY))
        # print(task_tree
        #     .due_by(TODAY.strftime('%Y-%m-%d'))
        #     .search(lambda task: not task.complete))

    @classmethod
    def display_tomorrow(*args, **kwargs):
        pass
        # task_tree = Commands.task_tree
        # tomorrow = TODAY + timedelta(days=1)
        # print(Commands.highlight_dates(CAL_STR, tomorrow, tomorrow))
        # print(task_tree
        #     .due_by(tomorrow.strftime('%Y-%m-%d'))
        #     .search(lambda task: not task.complete))

    @classmethod
    def display_week(*args, **kwargs):
        pass
        # print(Commands.highlight_dates(CAL_STR,WEEK_BEGIN,WEEK_END))
        # print(task_tree.due_by(WEEK_END.strftime('%Y-%m-%d')))

    @classmethod
    def add_task(*args, **kwargs):
        pass
        # task_tree = Commands.task_tree

        # # positional arguments from command line:
        # id = kwargs['parent_id']
        # task_name = kwargs['child_task_name']
        # deadline = kwargs['child_task_deadline']

        # # add subtask to task tree and print result to terminal
        # task_tree.get_subtask(id).add_subtask(
        #     TaskTree(
        #         task_name =  task_name,
        #         deadline =  deadline
        #     )
        # )
        # print(task_tree)

        # # repeated tasks (optional)

        # # save task tree to json file
        # task_tree.to_json_file()

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

        # TODO: Fix this nasty KeyError with a try/except clause
            # (env) david@Davids-MacBook-Air due % python -m due ls 1.0
            # Traceback (most recent call last):
            #   File "/opt/homebrew/Cellar/python@3.9/3.9.5/Frameworks/Python.framework/Versions/3.9/lib/python3.9/runpy.py", line 197, in _run_module_as_main
            #     return _run_code(code, main_globals, None,
            #   File "/opt/homebrew/Cellar/python@3.9/3.9.5/Frameworks/Python.framework/Versions/3.9/lib/python3.9/runpy.py", line 87, in _run_code
            #     exec(code, run_globals)
            #   File "/Users/david/Desktop/due/due/__main__.py", line 64, in <module>
            #     args.func(**vars(args)) #allows you to pass arguments to functions in Main class
            #   File "/Users/david/Desktop/due/due/cli.py", line 128, in ls
            #     display_tree = dfs(root_id,display_tree)
            #   File "/Users/david/Desktop/due/due/cli.py", line 121, in dfs
            #     for neighbor in task_tree.tree.adj[node]:
            #   File "/Users/david/Desktop/due/env/lib/python3.9/site-packages/networkx/classes/coreviews.py", line 79, in __getitem__
            #     return AtlasView(self._atlas[name])
            # KeyError: '1.0'

        ## TODO: these are to format output. I may not want to see the dates, year component of dates, or only tasks that aren't done.
        ## Find out how to use rich to format output of task tree. Colors and unicode checkboxes would be nice.
        # not_done = kwargs['notdone']
        # no_dates = kwargs['nodates']
        # no_year = kwargs['noyear']

        # TODO: Find out how to filter your dfs by such elements as these. Maybe you can use a networkx filter function on
        # the task_tree to filter the treebefore dfs() is called?
        # depth = kwargs['depth']
        # done = kwargs['done']

        task_tree = Commands.task_tree

        root_id = kwargs['id']
        display_tree = Tree(f"{root_id} {task_tree.tree.nodes[root_id]}")

        def dfs(node,display_tree):

            for neighbor in task_tree.tree.adj[node]:
                # tree.add() returns a pointer to the node that was just added
                branch = display_tree.add(f"{neighbor} {task_tree.tree.nodes[neighbor]}")
                dfs(neighbor,branch)
            
            return display_tree

        display_tree = dfs(root_id,display_tree)

        print(display_tree)

    

    # @classmethod 
    # init(*args,**kwargs):
    #     # TODO: this function should create a new todo.json file in default location 
    #     # if such a file already exists, then the user is asked to provide the filename in order to confirm erasing the tasks file
    #     # can also init from a file in another location, which should change where due looks for thie todo.json in the future.
    #     pass

