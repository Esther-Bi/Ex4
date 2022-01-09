import json

from client_python.DiGraph import DiGraph


class Agent:

    def __init__(self, id: int = None, value: float = 0.0, src: int = None, dest: int = None, speed: int = 0,
                 pos: str = "0.0,0.0,0.0", graph: DiGraph = None) -> None:
        self.id = id
        self.value = value
        self.src = src
        self.dest = dest
        self.speed = speed
        p = pos.split(",")
        self.x = float(p[0])
        self.y = float(p[1])
        self.node_tasks = []
        self.path = 0
        if self.dest == -1:
            found_current = None
            for node in graph.nodes.keys():
                node_x = graph.nodes[node].x
                node_y = graph.nodes[node].y
                if self.x - 0.0000001 <= node_x <= self.x + 0.0000001 and self.y - 0.0000001 <= node_y <= self.y + 0.0000001:
                    found_current = node
                    break
            self.current = found_current
        else:
            self.current = None

    def add_task(self, node_id_src: list = None, node_id_dest: int = None):
        self.node_tasks.extend(node_id_src)
        if self.node_tasks[-1] != node_id_dest:
            self.node_tasks.append(node_id_dest)

    def remove_task(self):
        self.node_tasks.pop(0)

    def already_taken(self, src_node: int = None, dest_node: int = None):
        if len(self.node_tasks) ==0:
            if self.src == src_node and self.dest == dest_node:
                return True
            return False
        src = False
        if self.src == src_node and self.node_tasks[0] == dest_node:
            return True
        if self.dest == src_node and self.node_tasks[0] == dest_node:
            return True
        if self.dest == -1:
            if self.current == src_node and self.node_tasks[0] == dest_node:
                return True
        for i in self.node_tasks:
            if src and i == dest_node:
                return True
            src = False
            if i == src_node:
                src = True
                continue
        return False

    def next_node(self):
        return self.node_tasks[0]


class Agents:

    def __init__(self, file_name: str = None, graph: DiGraph = None) -> None:
        self.agent_dict = {}
        if file_name is None:
            return
        try:
            dict_building = json.loads(file_name)
            for agent in dict_building['Agents']:
                data = agent['Agent']
                id = int(data['id'])
                value = float(data['value'])
                src = int(data['src'])
                dest = int(data['dest'])
                speed = float(data['speed'])
                pos = data['pos']
                a = Agent(id, value, src, dest, speed, pos, graph)
                self.agent_dict[id] = a
        except json.decoder.JSONDecodeError:
            print("String could not be converted to JSON")

    def change_values(self, agent_json: str = None, graph: DiGraph = None):
        if agent_json is None:
            return
        try:
            dict_Agent = json.loads(agent_json)
            for agent in dict_Agent['Agents']:
                data = agent['Agent']
                id = int(data['id'])

                value = float(data['value'])
                self.agent_dict[id].value = value
                src = int(data['src'])
                self.agent_dict[id].src = src
                dest = int(data['dest'])
                self.agent_dict[id].dest = dest
                if dest == -1:
                    found_current = None
                    for node in graph.nodes.keys():
                        node_x = graph.nodes[node].x
                        node_y = graph.nodes[node].y
                        if self.agent_dict[id].x - 0.0000001 <= node_x <= self.agent_dict[id].x + 0.0000001 and \
                                self.agent_dict[id].y - 0.0000001 <= node_y <= self.agent_dict[id].y + 0.0000001:
                            found_current = node
                            break
                    self.agent_dict[id].current = found_current
                else:
                    self.agent_dict[id].current = None
                speed = float(data['speed'])
                self.agent_dict[id].speed = speed
                pos = data['pos']
                p = pos.split(",")
                self.agent_dict[id].x = float(p[0])
                self.agent_dict[id].y = float(p[1])
                path = 0
                for i in range(len(self.agent_dict[id].node_tasks) - 1):
                    node_src = self.agent_dict[id].node_tasks[i]
                    node_dest = self.agent_dict[id].node_tasks[i + 1]
                    if node_src == node_dest:
                        weight = 0
                    else:
                        weight = graph.nodes[node_src].edge_out[node_dest]
                    path = path + weight
                self.agent_dict[id].path = path / self.agent_dict[id].speed

        except json.decoder.JSONDecodeError:
            print("String could not be converted to JSON")
