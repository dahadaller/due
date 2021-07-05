import json
import argparse
import calendar
import re
from datetime import datetime, date, timedelta
from itertools import chain
from pathlib import Path

from rich.console import Console
# from rich import print as rprint
from rich.tree import Tree


from due import CAL_STR, TODAY, TASK_TREE, TASK_FILE_PATH, COLOR
from due.tasks import TaskTree

class RichTextCal:

    @staticmethod
    def header_offset():
        # find the end index of the calendar header
        cal_header_pattern = re.compile(r"Sa\n",re.MULTILINE)
        match = cal_header_pattern.search(CAL_STR)
        header_offset = match.end()
        return header_offset

    @staticmethod
    def highlight_match(regex, multiline=False):
        # find start and end indexes for regex in CAL_STR
        header_offset = RichTextCal.header_offset()
        pattern = re.compile(regex,re.MULTILINE) if multiline else re.compile(regex)
        match = pattern.search(CAL_STR[header_offset:])
        match_start, match_end = header_offset+match.start(), header_offset+match.end()
        cal_str = (
            CAL_STR[:match_start] + 
            r"[reverse]" + 
            CAL_STR[match_start:match_end] + 
            r"[/reverse]" + 
            CAL_STR[match_end:]
        )
        return cal_str


    @staticmethod
    def print_week(day=TODAY.day):
        # highlights week around a given day on calendar
        week_regex = rf"^.*\b{day}.*$"
        cal_str = RichTextCal.highlight_match(week_regex, multiline=True)
        cons = Console(theme=COLOR)
        cons.print(cal_str, highlight=False) #highlight=False because I don't want numbers to be highlighted different color


    @staticmethod
    def print_day(day=TODAY.day):
        # highlights day only on calendar

        # want to highlight space in front of day if it's only one digit.
        day_regex = f' {day}' if len(str(day)) == 1 else str(day)
        cal_str = RichTextCal.highlight_match(day_regex, multiline=False)
        cons = Console(theme=COLOR)
        cons.print(cal_str, highlight=False) #highlight=False because I don't want numbers to be highlighted different color

class RichTextTree:
    # TODO: clean up this class. I believe format_task() should call print_task() and print_task should be renamed
    # TODO: don't need to pass attr for this function. this can be retrieved from TASK_TREE using TASK_TREE.tree.nodes[kwargs['id']
    @staticmethod
    def print_task(task_id, attr, tag, message):
        t_id, name, deadline = task_id, attr['task_name'], attr['deadline'].strftime("%Y-%m-%d")
        line = f"{message}: [{tag}]{t_id} {name} {deadline}[/{tag}]"
        return line

    @staticmethod 
    def format_task(task_id, attr, noids, nodates, noyear):

        if not attr:
            line = '' if noids else f"[task_id]{task_id}[/task_id]"

        # if task is complete, appy [complete] tags
        elif  attr['complete']:
            format_id =  '' if noids else f"{task_id} "
            format_name = f"{attr['task_name']} "
            deadline = attr['deadline'].strftime("%m-%d") if noyear else attr['deadline'].strftime("%Y-%m-%d")
            format_deadline = '' if nodates else f"{deadline} "
            line = f"[complete]{format_id} {format_name} {format_deadline}[/complete]"

        # if task isn't complete, just display id, name and deadline
        else:
            format_id =  '' if noids else f"[task_id]{task_id}[/task_id] "
            format_name= f"[task_name]{attr['task_name']}[/task_name] "
            deadline = attr['deadline'].strftime("%m-%d") if noyear else attr['deadline'].strftime("%Y-%m-%d")
            format_deadline = '' if nodates else f"[deadline]{deadline}[/deadline] "
            line = f"{format_id}{format_name}{format_deadline}"

        return line

    @staticmethod 
    def format_tree(root_task_id, task_tree, noids, nodates, noyear):

        # CREATE RICH TEXT TREE
        attr = task_tree.tree.nodes[root_task_id]
        display_tree = Tree(RichTextTree.format_task(root_task_id, attr, noids, nodates, noyear) )

        def dfs(node,display_tree):

            for neighbor in task_tree.tree.adj[node]:

                attr = task_tree.tree.nodes[neighbor]
                line = RichTextTree.format_task(neighbor, attr, noids, nodates, noyear)

                # the tree.add() method returns a pointer to the node that was just added
                branch = display_tree.add(line)
                dfs(neighbor,branch)
            
            return display_tree

        display_tree = dfs(root_task_id,display_tree)
        return display_tree

class Commands:

    @staticmethod
    def get_next_saturday(date_val):
        #12 = 5 mod 7 and 5 is what .weekday() returns for saturday
        days_to_next_saturday = timedelta((12 - date_val.weekday()) % 7) 
        saturday = date_val + days_to_next_saturday
        return saturday

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
    def ls(*args, **kwargs):

        # PARSE COMMAND LINE ARGUMENTS
        depth = kwargs['depth']
        deadline = kwargs['deadline']
        root_id = kwargs['id']
        noids = kwargs['noids']
        nodates = kwargs['nodates']
        noyear = kwargs['noyear']

        if kwargs['done'] == True: # TODO: --done flag will not produce a complete tree because children can be completed before parents and so there's no way to get to parents. need to use "promote" algorithm to elevate children in this case.
            completion_status = True
        elif kwargs['undone'] == True: 
            completion_status = False
        else:
            completion_status = None

        # LOAD TASK TREE FROM JSON and filter based on cli args
        task_tree = (
            TASK_TREE
            .depth_limit(depth)
            .due_by(deadline)
            .completed(completion_status)
        )

        # CREATE RICH TEXT TREE FROM TASK_TREE
        display_tree = RichTextTree.format_tree(root_id, task_tree, noids, nodates, noyear)

        # GET CONFIG FILE CONTENTS AND LOAD COLOR INTO CONSOLE AS THEME
        cons = Console(theme=COLOR)

        # DISPLAY RICH TEXT TREE ON CONSOLE
        cons.print(display_tree)

    @classmethod
    def display_today(*args,**kwargs):
        RichTextCal.print_day()
        Commands.ls(
            id='0',
            depth= None,
            done= False,
            undone= True,
            nodates= True,
            noids=False,
            noyear=False,
            deadline=TODAY
        )


    @classmethod
    def display_tomorrow(*args, **kwargs):
        tomorrow = TODAY + timedelta(days=1)
        RichTextCal.print_day(tomorrow.day)
        Commands.ls(
            id='0',
            depth= None,
            done= False,
            undone= True,
            nodates= True,
            noids=False,
            noyear=False,
            deadline=tomorrow
        )

    @classmethod
    def display_week(*args, **kwargs):
        RichTextCal.print_week()
        Commands.ls(
            id='0',
            depth= None,
            done= False,
            undone= True,
            nodates= True,
            noids=False,
            noyear=False,
            deadline=Commands.get_next_saturday(TODAY)
        )

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
        # TODO: displays deleted task in terminal; make it actually change the task
        line = RichTextTree.print_task(kwargs['id'],TASK_TREE.tree.nodes[kwargs['id']],'delete','deleted')
        cons=Console(theme=COLOR)
        cons.print(line)

    @classmethod
    def complete_task(*args, **kwargs):
        # TODO: displays complete task in terminal; make it actually change the task
        line = RichTextTree.print_task(kwargs['id'],TASK_TREE.tree.nodes[kwargs['id']],'complete','marked done')
        cons=Console(theme=COLOR)
        cons.print(line)

    @classmethod
    def uncomplete_task(*args, **kwargs):
        # TODO: displays incomplete task in terminal; make it actually change the task
        line = RichTextTree.print_task(kwargs['id'],TASK_TREE.tree.nodes[kwargs['id']],'incomplete','marked undone')
        cons=Console(theme=COLOR)
        cons.print(line)


    # @classmethod 
    # init(*args,**kwargs):
    #     # TODO: this function should create a new todo.json file in default location 
    #     # if such a file already exists, then the user is asked to provide the filename in order to confirm erasing the tasks file
    #     # can also init from a file in another location, which should change where due looks for thie todo.json in the future.
    #     pass

