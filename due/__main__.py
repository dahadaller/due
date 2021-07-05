import argparse

from due.cli import Commands

if __name__ == '__main__':

    # due
    due = argparse.ArgumentParser(prog='due')
    subcommands = due.add_subparsers()
    due.set_defaults(func=Commands.display_today) # no subparser defaults to `due today`

    # # due init
    # init = subcommands.add_parser('init')
    # ls.add_argument('id',type=str, nargs='?', default='todo.json')
    # init.set_defaults(func=Commands.init)

    # due today
    today = subcommands.add_parser('today', aliases=['td'])
    today.set_defaults(func=Commands.display_today)

    # due tomorrow
    tomorrow = subcommands.add_parser('tomorrow', aliases=['tm'])
    tomorrow.set_defaults(func=Commands.display_tomorrow)

    # due week
    week = subcommands.add_parser('week', aliases=['we','w'])
    week.set_defaults(func=Commands.display_week)

    # TODO:
    # add subcommand 'due on YYYY-MM-DD' which should be an alias for `due ls -on YYYY-MM-DD` 

    # due ls
    ls = subcommands.add_parser('ls')
    ls.add_argument('id',type=Commands.valid_id, nargs='?', default='0')
    ls.add_argument("-e", "--depth",type=int)
    ls.add_argument("-d", "--deadline", type=Commands.valid_date)    
    ls.add_argument("--done",action='store_true') 
    ls.add_argument("--undone",action='store_true') 
    ls.add_argument("--nodates",action='store_true')
    ls.add_argument("--noyear",action='store_true')
    ls.add_argument("--noids",action='store_true')
    ls.set_defaults(func=Commands.ls)

    # TODO:
    # due add
    add = subcommands.add_parser('add')
    add.add_argument('parent_id',type=str)
    add.add_argument('child_task_name',type=str)
    add.add_argument('child_task_deadline',type=str)
    add.set_defaults(func=Commands.add_task)

    # TODO:
    # due rm
    rm = subcommands.add_parser('rm')
    rm.add_argument('id',type=str)
    rm.set_defaults(func=Commands.rm_task)

    # TODO:
    # due done
    done = subcommands.add_parser('done')
    done.add_argument('id',type=str)
    done.set_defaults(func=Commands.complete_task)

    # TODO:
    # due undone
    undone = subcommands.add_parser('undone')
    undone.add_argument('id',type=str)
    undone.set_defaults(func=Commands.uncomplete_task)

    # parse arguments and run
    args = due.parse_args()
    args.func(**vars(args)) #allows you to pass arguments to functions in Main class