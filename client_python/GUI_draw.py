import json

import pygame
from pygame import gfxdraw, display, RESIZABLE, transform, image
from pygame.color import Color


class GUI:
    def __init__(self, opening_background, agent, pokemon1, pokemon2, background, graph, algo_graph, screen):
        self.opening_background = opening_background
        self.agent = agent
        self.pokemon1 = pokemon1
        self.pokemon2 = pokemon2
        self.background = background
        self.graph = graph
        self.algo_graph = algo_graph
        self.screen = screen

    def draw_opening_background(self):
        background_image = image.load(self.opening_background)
        background_image = transform.scale(background_image, (self.screen.get_width(), self.screen.get_height()))
        self.screen.blit(background_image, [0, 0])

    def draw_background(self):
        background_image = image.load(self.background)
        background_image = transform.scale(background_image, (self.screen.get_width(), self.screen.get_height()))
        self.screen.blit(background_image, [0, 0])

    def draw_pokemons(self, pokemons, my_scale):
        pokemon_image1 = image.load(self.pokemon1)
        pokemon_image1 = transform.scale(pokemon_image1, (30, 30))
        pokemon_image2 = image.load(self.pokemon2)
        pokemon_image2 = transform.scale(pokemon_image2, (40, 40))
        for p in pokemons.pokemon_list:
            # pygame.draw.circle(screen, p.color,
            #                    (int(my_scale(float(p.x), x=True)), int(my_scale(float(p.y), y=True))), 10)
            if p.color == 1:
                self.screen.blit(pokemon_image1,
                                 (int(my_scale(float(p.x), x=True) - 20), int(my_scale(float(p.y), y=True) - 20)))
            if p.color == 2:
                self.screen.blit(pokemon_image2,
                                 (int(my_scale(float(p.x), x=True) - 20), int(my_scale(float(p.y), y=True) - 20)))

    def draw_agents(self, agents, my_scale):
        agent_image = image.load(self.agent)
        agent_image = transform.scale(agent_image, (60, 60))
        for agent in agents.agent_dict.values():
            self.screen.blit(agent_image,
                             (int(my_scale(float(agent.x), x=True) - 20), int(my_scale(float(agent.y), y=True) - 20)))

    def draw_nodes(self, my_scale, FONT):
        for node_id, node_data in self.graph.nodes.items():
            srcX = self.graph.nodes[node_id].x
            srcY = self.graph.nodes[node_id].y

            x = my_scale(srcX, x=True)
            y = my_scale(srcY, y=True)

            gfxdraw.filled_circle(self.screen, int(x), int(y), 15, Color(64, 80, 174))
            gfxdraw.aacircle(self.screen, int(x), int(y), 15, Color(255, 255, 255))

            # draw the node id
            id_srf = FONT.render(str(node_id), True, Color(255, 255, 255))
            rect = id_srf.get_rect(center=(x, y))
            self.screen.blit(id_srf, rect)

    def draw_edges(self, my_scale):
        for node_id, node_data in self.graph.nodes.items():
            for dest_node_id, edge_weight in self.graph.nodes[node_id].edge_out.items():
                srcX = self.graph.nodes[node_id].x
                srcY = self.graph.nodes[node_id].y
                destX = self.graph.nodes[dest_node_id].x
                destY = self.graph.nodes[dest_node_id].y

                src_x = my_scale(srcX, x=True)
                src_y = my_scale(srcY, y=True)
                dest_x = my_scale(destX, x=True)
                dest_y = my_scale(destY, y=True)

                # draw the line
                pygame.draw.line(self.screen, Color(61, 72, 126), (src_x, src_y), (dest_x, dest_y), 4)

    def algo(self, agents, pokemons, client):
        agents.change_values(client.get_agents(), self.graph)
        for pokemon in pokemons.pokemon_list:
            min_path = float('inf')
            chosen_a = None
            short_path_of_chosen = []
            taken = False
            for agent in agents.agent_dict.values():
                if agent.already_taken(pokemon.src, pokemon.dest):
                    taken = True
                    break
            if taken:
                continue
            for agent in agents.agent_dict.values():
                if agent.node_tasks:
                    n1 = agent.node_tasks[-1]
                else:
                    if agent.dest == -1:
                        n1 = agent.current
                    else:
                        n1 = agent.dest
                n2 = pokemon.src
                current = self.algo_graph.shortest_path(n1, n2)
                if min_path > agent.path + (current[0] / agent.speed):
                    min_path = agent.path + (current[0] / agent.speed)
                    short_path_of_chosen = current[1]
                    chosen_a = agent.id
            agents.agent_dict[chosen_a].add_task(short_path_of_chosen, pokemon.dest)
            agents.change_values(client.get_agents(), self.graph)

    def next_edge(self, agents, client):
        for agent in agents.agent_dict.values():
            if agent.dest == -1 and len(agent.node_tasks) > 0:
                next_node = agent.next_node()
                agent.remove_task()
                client.choose_next_edge(
                    '{"agent_id":' + str(agent.id) + ', "next_node_id":' + str(next_node) + '}')
                ttl = client.time_to_end()
                print(ttl, client.get_info())

    def check_events(self, client, stop_button):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                client.stop_connection()
                pygame.quit()
                exit(0)
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if stop_button.collidepoint(mouse_pos):
                    client.stop_connection()
                    pygame.quit()
                    exit(0)

    def start_button(self, WIDTH, HEIGHT, FONT):
        start_button = pygame.Rect(WIDTH / 2 - 125, HEIGHT / 2 - 50, 250, 75)
        start_text = FONT.render("START", True, Color(0, 0, 0))
        pygame.draw.rect(self.screen, (255, 193, 193), start_button, border_radius=15)
        self.screen.blit(start_text, (WIDTH / 2 - 85, HEIGHT / 2 - 50))
        return start_button

    def stop_button(self, FONT):
        stop_button = pygame.Rect(120, 10, 90, 35)
        stop_text = FONT.render("Stop", True, Color(0, 0, 0))
        pygame.draw.rect(self.screen, (255, 193, 193), stop_button, border_radius=15)
        self.screen.blit(stop_text, (148, 17))
        return stop_button

    def timer_window(self, client, FONT):
        pygame.draw.rect(self.screen, (255, 193, 193), [20, 10, 90, 35], border_radius=15)
        time_text = FONT.render("Time: " + str((int(client.time_to_end()) / 1000)).split('.')[0], True, Color(0, 0, 0))
        self.screen.blit(time_text, (30, 17))

    def moves_window(self, client, FONT):
        pygame.draw.rect(self.screen, (255, 193, 193), [220, 10, 90, 35], border_radius=15)
        info_details = json.loads(client.get_info())
        moves = info_details['GameServer']['moves']
        moves_text = FONT.render("Moves:" + str(moves), True, Color(0, 0, 0))
        self.screen.blit(moves_text, (226, 17))

    def grade(self, client, FONT):
        pygame.draw.rect(self.screen, (255, 193, 193), [320, 10, 90, 35], border_radius=15)
        info_details = json.loads(client.get_info())
        grade = info_details['GameServer']['grade']
        moves_text = FONT.render("Grade:" + str(grade), True, Color(0, 0, 0))
        self.screen.blit(moves_text, (322, 17))
