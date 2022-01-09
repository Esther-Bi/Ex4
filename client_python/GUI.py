import asyncio
import time
import json
from pygame import gfxdraw, display, RESIZABLE, transform, image
import pygame
from pygame.color import Color

from client_python.Agent import Agents
from client_python.DiGraph import DiGraph
from client_python.GUI_draw import GUI
from client_python.GraphAlgo import GraphAlgo

from client import Client
from client_python.pokemon import Pokemons
from client_python.pokemon import Pokemon

# init pygame
WIDTH, HEIGHT = 1080, 720
# default port
PORT = 6666
# server host (default localhost 127.0.0.1)
HOST = '127.0.0.1'
pygame.init()

screen = display.set_mode((WIDTH, HEIGHT), depth=32, flags=RESIZABLE)
clock = pygame.time.Clock()
pygame.font.init()

client = Client()
client.start_connection(HOST, PORT)

FONT = pygame.font.SysFont('comicsansms', 15, bold=True)
OPEN_FONT = pygame.font.SysFont('comicsansms', 50, bold=True)

graph_json = client.get_graph()
print(graph_json)
graph = DiGraph(graph_json) # upload graph
algo_graph = GraphAlgo(graph) # convert to GraphAlgo for the usage of shortest path

# get data proportions
min_x = min(list(graph.nodes.values()), key=lambda n: n.x).x
min_y = min(list(graph.nodes.values()), key=lambda n: n.y).y
max_x = max(list(graph.nodes.values()), key=lambda n: n.x).x
max_y = max(list(graph.nodes.values()), key=lambda n: n.y).y


def scale(data, min_screen, max_screen, min_data, max_data):
    """
    get the scaled data with proportions min_data, max_data
    relative to min and max screen dimentions
    """
    return ((data - min_data) / (max_data - min_data)) * (max_screen - min_screen) + min_screen


def my_scale(data, x=False, y=False):
    if x:
        return scale(data, 50, screen.get_width() - 50, min_x, max_x)
    if y:
        return scale(data, 50, screen.get_height() - 50, min_y, max_y)


async def move_after(delay):
    """
    make a delay on function move() to reduce the number of times calling it
    """
    await asyncio.sleep(delay)
    client.move()


async def move_pokemons(flag: bool = False):
    """
    if the agent is on an edge that has a pokemon (flag = True) - call to move() function
    if the agent is on an edge that has no pokemon on it (flag = False) - call to move() function every 0.122 seconds
    """
    if not flag:
        await move_after(0.122)
    if flag:
        client.move()


info_details = json.loads(client.get_info())
num_of_agents = info_details['GameServer']['agents']
pokemons = Pokemons(client.get_pokemons(), graph)
pokemons.pokemon_list.sort(key=lambda x: x.value)

# add agents
i = 0
while i < num_of_agents:
    client.add_agent("{\"id\":" + str(pokemons.pokemon_list[i].src) + "}")
    i += 1

agents = Agents(client.get_agents(), graph)

gui = GUI('designs/opening_background.jpg', 'designs/agent.png', 'designs/pokemon1.png', 'designs/pokemon2.png',
          'designs/background.jpg', graph, algo_graph, screen)

didnt_start_yet = True

# opening screen
while didnt_start_yet:
    screen.fill(Color(0, 0, 0))
    gui.draw_opening_background()
    start_button = gui.start_button(WIDTH, HEIGHT, OPEN_FONT)
    didnt_start_yet = gui.check_events(client, None, start_button, False, True)
    display.update() # update screen changes

# starts the game
client.start()
while client.is_running() == 'true':
    screen.fill(Color(0, 0, 0)) # refresh surface
    gui.draw_background()
    gui.timer_window(client, FONT) # Timer window
    stop_button = gui.stop_button(FONT) # Stop button
    gui.moves_window(client, FONT) # Moves counter window
    gui.grade(client, FONT) # Grade counter window

    pokemons = Pokemons(client.get_pokemons(), graph)
    pokemons.pokemon_list.sort(key=lambda x: x.value)

    gui.check_events(client, stop_button, None, True, False)

    gui.draw_edges(my_scale)
    gui.draw_nodes(my_scale, FONT)
    gui.draw_agents(agents, my_scale)
    gui.draw_pokemons(pokemons, my_scale)

    display.update() # update screen changes
    clock.tick(60) # refresh rate

    gui.algo(agents, pokemons, client) # find the best adjustments of pokemons to agents
    gui.next_edge(agents, client) # move all agents

    move = False
    for agent in agents.agent_dict.values():
        for pokemon in pokemons.pokemon_list:
            if agent.src == pokemon.src and agent.dest == pokemon.dest:
                move = True
                break
        if move:
            break

    asyncio.run(move_pokemons(move)) # decrease number of calling to move()
