import json
import argparse
import calendar
from datetime import datetime, date, timedelta
from itertools import chain
from pathlib import Path

from due.task import Task
from due import CAL_STR, TODAY, WEEK_BEGIN, WEEK_END


class Main:
    task_tree = Task.from_json_file() # TODO: is there a way to put this in __init__.py?

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
    def display_today(*args,**kwargs):
        task_tree = Main.task_tree
        print(Main.highlight_dates(CAL_STR, TODAY, TODAY))
        print(task_tree
            .due_by(TODAY.strftime('%Y-%m-%d'))
            .search(lambda task: not task.complete))

    @classmethod
    def display_tomorrow(*args, **kwargs):
        task_tree = Main.task_tree
        tomorrow = TODAY + timedelta(days=1)
        print(Main.highlight_dates(CAL_STR, tomorrow, tomorrow))
        print(task_tree
            .due_by(tomorrow.strftime('%Y-%m-%d'))
            .search(lambda task: not task.complete))

    @classmethod
    def display_week(*args, **kwargs):

        print(Main.highlight_dates(CAL_STR,WEEK_BEGIN,WEEK_END))
        print(task_tree.due_by(WEEK_END.strftime('%Y-%m-%d')))

    @classmethod
    def add_task(*args, **kwargs):
        task_tree = Main.task_tree

        # positional arguments from command line:
        id = kwargs['parent_id']
        task_name = kwargs['child_task_name']
        deadline = kwargs['child_task_deadline']

        # add subtask to task tree and print result to terminal
        task_tree.get_subtask(id).add_subtask(
            Task(
                task_name =  task_name,
                deadline =  deadline
            )
        )
        print(task_tree)

        # repeated tasks (optional)

        # save task tree to json file
        task_tree.to_json_file()

    @classmethod
    def rm_task(*args, **kwargs):
        task_tree = Main.task_tree
        id = kwargs['id'].split('.')
        child_id = id[-1]
        parent_id = '.'.join(id[:-1])
        task_tree.get_subtask(parent_id).remove_subtask(child_id)
        print(task_tree)
        task_tree.to_json_file()

    @classmethod
    def complete_task(*args, **kwargs):
        task_tree = Main.task_tree
        id = kwargs['id']
        task_tree.get_subtask(id).complete = True
        print(task_tree)
        task_tree.to_json_file()

    @classmethod
    def uncomplete_task(*args, **kwargs):
        task_tree = Main.task_tree
        id = kwargs['id']
        task_tree.get_subtask(id).complete = False
        print(task_tree)
        task_tree.to_json_file()

    @classmethod
    def ls(*args, **kwargs):
        task_tree = Main.task_tree
        id = kwargs['id']
        depth = kwargs['depth']
        show_deadline = not kwargs['nodates']
        show_year = not kwargs['noyear']
        show_id = not kwargs['noids']
        color = True

        if kwargs['done']:
            f = lambda task: task.complete
        elif kwargs['notdone']:
            f = lambda task: not task.complete
        else:
            f = lambda task: True

        print(task_tree
                .get_subtask(id)
                .search(f)
                .to_string(
                    max_depth=depth,
                    show_id=show_id,
                    show_deadline=show_deadline,
                    show_year=show_year,
                    color=color))

    # @classmethod 
    # init(*args,**kwargs):
    #     # TODO: this function should create a new todo.json file in default location 
    #     # if such a file already exists, then the user is asked to provide the filename in order to confirm erasing the tasks file
    #     # can also init from a file in another location, which should change where due looks for thie todo.json in the future.
    #     pass



if __name__ == '__main__':

    # due
    due = argparse.ArgumentParser(prog='due')
    subcommands = due.add_subparsers()
    due.set_defaults(func=Main.display_today) # no subparser defaults to `due today`

    # # due init
    # init = subcommands.add_parser('init')
    # ls.add_argument('id',type=str, nargs='?', default='todo.json')
    # init.set_defaults(func=Main.init)

    # due today
    today = subcommands.add_parser('today', aliases=['td'])
    today.set_defaults(func=Main.display_today)

    # due tomorrow
    tomorrow = subcommands.add_parser('tomorrow', aliases=['tm'])
    tomorrow.set_defaults(func=Main.display_tomorrow)

    # due week
    week = subcommands.add_parser('week', aliases=['we','w'])
    week.set_defaults(func=Main.display_week)

    # due ls
    ls = subcommands.add_parser('ls')
    ls.add_argument('id',type=str, nargs='?', default='root')
    ls.add_argument("-d", "--depth",type=int)
    ls.add_argument("--done",action='store_true')
    ls.add_argument("--notdone",action='store_true')
    ls.add_argument("--nodates",action='store_true')
    ls.add_argument("--noyear",action='store_true')
    ls.add_argument("--noids",action='store_true')
    ls.set_defaults(func=Main.ls)

    # due add
    add = subcommands.add_parser('add')
    add.add_argument('parent_id',type=str)
    add.add_argument('child_task_name',type=str)
    add.add_argument('child_task_deadline',type=str)
    add.set_defaults(func=Main.add_task)

    # due rm
    rm = subcommands.add_parser('rm')
    rm.add_argument('id',type=str)
    rm.set_defaults(func=Main.rm_task)

    # due done
    done = subcommands.add_parser('done')
    done.add_argument('id',type=str)
    done.set_defaults(func=Main.complete_task)

    # due undone
    undone = subcommands.add_parser('undone')
    undone.add_argument('id',type=str)
    undone.set_defaults(func=Main.uncomplete_task)

    # parse arguments and run
    args = due.parse_args()
    args.func(**vars(args)) #allows you to pass arguments to functions in Main class