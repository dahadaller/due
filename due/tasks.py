import json

from pathlib import Path
from datetime import date

import networkx as nx
from networkx.readwrite import json_graph

from due import TASK_FILE_PATH


class TaskTree:

    def __init__(self):

        self.tree = nx.DiGraph()
        self.tree.add_node('0')

    def add_task(self, parent_task_id, task_name, deadline):

        # adds subtask to existing task with id parent_task_id
        # new subtask has subtask name of task_name
        # and deadline of deadline

        id_suffix = str(len(list(self.tree.successors(parent_task_id))))
        task_id = parent_task_id + '.' + id_suffix

        self.tree.add_node(
            task_id, 
            task_name=task_name, 
            deadline=deadline,
            complete=False,
        )

        self.tree.add_edge(parent_task_id,task_id)

    def delete_task(self,task_id):
        self.tree.remove_node(task_id)

    def complete_task(self,task_id):
        self.tree.nodes[task_id]['complete'] = True

    def uncomplete_task(self,task_id):
        self.tree.nodes[task_id]['complete'] = False

    def due_by(self,deadline):
        selected_nodes = [n for n,v in self.tree.nodes(data=True) if n == '0' or v['deadline'] <= deadline]
        return selected_nodes

    def save(self, file:Path = TASK_FILE_PATH) -> None:
        data = json_graph.tree_data(self.tree, root='0')
        with file.open(mode='w') as write_file:
            json.dump(data, write_file, indent=4)

    @staticmethod
    def load(file:Path = TASK_FILE_PATH):
        with file.open(mode='r') as read_file:
            data = json.load(read_file)
        t = TaskTree()
        t.tree = json_graph.tree_graph(data)
        return t



# t = TaskTree()
# t.add_task('0','do this','1234')
# t.add_task('0','and this','1234')
# t.add_task('0','also this','1234')
# t.add_task('0.2','mep','1234')
# t.add_task('0.2','mop','1234')
# t.add_task('0.2','merp','1234')
# t.add_task('0.1','rich','1234')
# t.add_task('0.1','man','1234')
# t.add_task('0.1','problems','1234')

# t.complete_task('0.2')
# print(t.tree.nodes)





