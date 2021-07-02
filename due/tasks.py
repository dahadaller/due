import json

from pathlib import Path
from datetime import date,datetime

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

        # TODO: assert that deadline of parent must be after deadline of child
        # TODO: assert that parent can't be done while children aren't (somehow)

        id_suffix = str(len(list(self.tree.successors(parent_task_id))))
        task_id = parent_task_id + '.' + id_suffix

        self.tree.add_node(
            task_id, 
            task_name=task_name, 
            deadline=deadline,
            complete=False,
        )

        self.tree.add_edge(parent_task_id,task_id)
        return self

    def delete_task(self,task_id):
        self.tree.remove_node(task_id)
        return self

    def complete_task(self,task_id):
        # TODO: assert that parent can't be done while children aren't
        self.tree.nodes[task_id]['complete'] = True
        return self

    def uncomplete_task(self,task_id):
        self.tree.nodes[task_id]['complete'] = False
        return self

    def subtree(self,callback):
        #callback must return a boolean based on node,data inputs
        selected_nodes = [node for node,data in self.tree.nodes(data=True) if callback(node,data)]
        t = TaskTree() 
        t.tree = self.tree.subgraph(selected_nodes)
        return t

    def due_by(self,deadline):
        if deadline in (False,None):
            return self
        callback = lambda node,data: node == '0' or data['deadline'] <= deadline
        return self.subtree(callback)

    def depth_limit(self,depth):
        if depth in (False,None):
            return self
        node_depth_dict = nx.shortest_path_length(self.tree,'0')
        callback = lambda node,data: node_depth_dict[node]<=depth
        return self.subtree(callback)

    def completed(self,completion_status):
        if completion_status == None:
            return self
        callback = lambda node,data: node == '0' or data['complete'] == completion_status
        return self.subtree(callback)

    def save(self, file:Path = TASK_FILE_PATH) -> None:

        # convert any deadline attributes in task tree from date obj to strings before saving
        for node,data in self.tree.nodes(data=True):
            if data.get('deadline',None):
                self.tree.nodes[node]['deadline'] = datetime.strftime(data['deadline'], "%Y-%m-%d")

        data = json_graph.tree_data(self.tree, root='0')
        with file.open(mode='w') as write_file:
            json.dump(data, write_file, indent=4)

    @staticmethod
    def load(file:Path = TASK_FILE_PATH):

        with file.open(mode='r') as read_file:
            data = json.load(read_file)
        t = TaskTree()
        t.tree = json_graph.tree_graph(data)

        # convert any deadline attributes in task tree from string to date obj after loading
        for node,data in t.tree.nodes(data=True):
            if data.get('deadline',None):
                t.tree.nodes[node]['deadline'] = datetime.strptime(data['deadline'], "%Y-%m-%d").date()

        return t



# t = TaskTree()
# (
#     t.add_task('0','do this',date.today())
#     .add_task('0','and this',date.today())
#     .add_task('0','also this',date.today())
#     .add_task('0.2','mep',date.today())
#     .add_task('0.2','mop',date.today())
#     .add_task('0.2','merp',date.today())
#     .add_task('0.1','rich',date.today())
#     .add_task('0.1','man',date.today())
#     .add_task('0.1','problems',date.today())
#     .complete_task('0.2.0')
# )
# t.save()






