# Base code from Michael Breslavsky https://github.com/breslavmich/jet_fighter_multiplayer/tree/master

import json
import socket
import threading
import time
import pygame.event
import game
# from ImageLabel import ImageLabel
from constants import SERVER_IP, SERVER_PORT, LOADING_IMG, WHITE_CONTROLS, BLACK_CONTROLS, SCREEN_WIDTH, SCREEN_HEIGHT, CENTER
import chatlib
import tkinter as tk
from tkinter import messagebox
import ipaddress
from gamestate import *
from testscreen import *
import sys
from pygame.locals import *
from spaceinvader import *

win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.font.init()

class Client:
    def __init__(self):
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.__status_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.id = 0
        self.game = None
        self.server_ip = SERVER_IP
        self.server_port = SERVER_PORT

    def build_and_send_message(self, command: str, data: str) -> None:
        """Building a message according to the protocol and sending it to the server"""
        message = chatlib.build_message(command, data) + chatlib.END_OF_MESSAGE
        self.__socket.send(message.encode())
        print("[SERVER] -> [{}]:  {}".format(self.__socket.getpeername(), message))

    def recv_message_and_parse(self) -> tuple:
        """Receiving a message from the server and parsing it according to the protocol"""
        try:
            full_msg = ''
            while True:  # Receiving a message in a loop a character at a time until message end character appears
                char = self.__socket.recv(1).decode()
                if char == chatlib.END_OF_MESSAGE:
                    break
                full_msg += char
            cmd, data = chatlib.parse_message(full_msg)
            print("[{}] -> [SERVER]:  {}".format(self.__socket.getpeername(), full_msg))
            return cmd, data
        except:
            return None, None

    def connect(self):
        """Connecting to the server"""
        try:
            self.__socket.connect((self.server_ip, self.server_port))
            cmd, data = self.recv_message_and_parse()
            if cmd == chatlib.PROTOCOL_SERVER['error_msg']:
                raise Exception("ERROR: " + data)
            elif cmd == chatlib.PROTOCOL_SERVER['connected_successfully']:
                data = int(data)
                if data == 0 or data == 1:
                    self.id = data
            elif cmd == chatlib.PROTOCOL_SERVER['connection_limit']:
                raise Exception("Game is full.")
            else:
                raise Exception("Invalid connection message:", cmd, data)

        except Exception as e:
            return "Connection Error!!! " + str(e)

    def startup_screen(self):
        """Showing a startup screen prompting the player to enter the IP and PORT of the server"""

        def wait_start_msg(result: list):
            """Function to wait for the start message from the server"""
            global destroy_screen
            cmd, data = self.recv_message_and_parse()
            if cmd != chatlib.PROTOCOL_SERVER['game_starting_message']:
                print("Game Start Error", "Error while waiting for another player to connect.")
                result.append(True)
                connect_and_start()
            result.append(True)
            return 1

        def connect_and_start():
            """Getting the info the client provided, checking it and connecting to the server.
            If the game starts after that, starting the game. If the game is waiting for another player, displaying a loading screen"""
            # Getting info from entry fields
            ip_txt = SERVER_IP
            port_txt = SERVER_PORT
            ipaddress.ip_address(ip_txt)

            status = self.connect()  # Connecting to the server
            if status:  # Exiting if there was an error
                # messagebox.showerror("Error", status)
                print("Error status: ", status)
                return

            if self.id == 0:  # If the current player is the first player -> Waiting for another player.
                # Creating a 'waiting for player' window
                result = []
                # Starting a thread to listen to the server's start message
                wait = threading.Thread(target=wait_start_msg, args=[result])
                wait.start()

                while True:
                    win.fill((0, 0, 0))
                    font = pygame.font.SysFont("comicsans", 80)
                    text = font.render("Waiting for Player...", 1, (255,0,0), True)
                    win.blit(text, (SCREEN_WIDTH/2 - text.get_width()/2, SCREEN_HEIGHT/2 - text.get_height()/2))
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            self.disconnect()
                    pygame.display.update()                
                    if result:  # Checking if the server sent a start message
                        break
        connect_and_start()

    def disconnect(self):
        """Disconnecting from the server, closing the socket and exiting the program"""
        self.build_and_send_message(chatlib.PROTOCOL_CLIENT['disconnect_msg'], '')
        self.__socket.close()
        exit()

    def request_game_obj(self) -> None or int:
        """Requesting the game's current status"""
        try:
            self.build_and_send_message(chatlib.PROTOCOL_CLIENT['game_status_request'], '')
        except socket.error:
            return None
        cmd, data = self.recv_message_and_parse()
        if cmd != chatlib.PROTOCOL_SERVER['game_status_response']:
            if cmd == chatlib.PROTOCOL_SERVER['winner_msg']:  # Checking if the game ended and there is a winner
                # if self.id == int(data):
                #     messagebox.showinfo('Game Ended!', 'Congratulations! You Won!!!')
                # else:
                #     messagebox.showinfo('Game Ended!', 'You Lost!!!')
                self.disconnect()
            return None
        try:
            game_data = json.loads(data)  # Parsing the received dictionary
            self.game.score_0 = game_data['score_0']
            self.game.score_1 = game_data['score_1']
            for i in range(len(self.game.planes)):
                self.game.planes[i].data_from_dict(game_data['planes'][i])
            for i in range(len(self.game.aliens)):
                self.game.aliens[i].data_from_dict(game_data['aliens'][i])
            return 1
        except:
            return None

    def request_initial_data(self) -> dict or None:
        """Requesting the initial game data to start the game"""
        try:
            self.build_and_send_message(chatlib.PROTOCOL_CLIENT['initial_details'], '')
        except socket.error:
            return None
        cmd, data = self.recv_message_and_parse()
        if cmd != chatlib.PROTOCOL_SERVER['initial_data_response']:
            return None
        try:
            data = json.loads(data)  # Loading the dictionary
            return data
        except:
            return None

    def handle_key_press(self, key: int):
        """Sending the relevant information to the server when a key is pressed"""
        if self.id == 1:
            if key == pygame.K_RIGHT:
                key = pygame.K_d
            if key == pygame.K_LEFT:
                key = pygame.K_a
            if key == pygame.K_UP:
                key = pygame.K_w
            if key == pygame.K_DOWN:
                key = pygame.K_s
        if (self.id == 0 and key in WHITE_CONTROLS) or (self.id == 1 and key in BLACK_CONTROLS) \
                or key == pygame.K_SPACE:  # Only sending the information if the key is allowed
            self.build_and_send_message(chatlib.PROTOCOL_CLIENT['key_down_msg'], str(key))

    def handle_key_release(self, key: int):
        """Sending the relevant information to the server when a key is released"""
        if self.id == 1:
            if key == pygame.K_RIGHT:
                key = pygame.K_d
            if key == pygame.K_LEFT:
                key = pygame.K_a
            if key == pygame.K_UP:
                key = pygame.K_w
            if key == pygame.K_DOWN:
                key = pygame.K_s
        if (self.id == 0 and key in WHITE_CONTROLS) or (self.id == 1 and key in BLACK_CONTROLS):
            # Only sending the information if the key is allowed
            self.build_and_send_message(chatlib.PROTOCOL_CLIENT['key_up_msg'], str(key))

    def start(self):
        """Starting and managing the game"""
        game_state = GameState.TITLE

        while True:
            if game_state == GameState.TITLE:
                game_state = title_screen(screen, CENTER, game_loop)

            if game_state == GameState.NEWGAME:
                game_state = play()

            if game_state == GameState.MULTIPLAYER:
                self.startup_screen()  # Showing the startup screen and connecting to the server
                init_data = self.request_initial_data()  # Getting initial data
                if not init_data:
                    messagebox.showerror('Data error', 'Couldn\'t get game data')
                    exit()
                # Setting up initial parameters
                screen_width = init_data['width']
                screen_height = init_data['height']
                plane_pos = init_data['planes_pos']
                alien_pos = init_data['aliens_pos']
                self.game = game.Game(screen_width, screen_height, plane_pos, alien_pos)
                self.game.initialise_window()  # Starting the game's window
                run = True
                while run:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            run = False
                        elif event.type == pygame.KEYDOWN:
                            key = event.key
                            self.handle_key_press(key)
                        elif event.type == pygame.KEYUP:
                            key = event.key
                            self.handle_key_release(key)
                    self.request_game_obj()  # Updating game data each iteration
                    self.game.draw()
                self.disconnect()
                
            if game_state == GameState.HIGHSCORE:
                game_state = highscore(screen, highscore_file, CENTER, game_loop)

            if game_state == GameState.DEAD:
                game_state = game_over(screen, SCREEN_HEIGHT, CENTER, game_loop, spaceship, spaceship_group, 
                                   laser_group, alien_group, alien_laser_group, rock_group, rock_group_two,
                                   all_enemy_lasers, alien_still_group, falling_lasers, big_boss, green_group, sound)
            if game_state == GameState.NAME:
                game_state = getting_name()

            if game_state == GameState.QUIT:
                pygame.quit()
                return 0


if __name__ == '__main__':
    client = Client()
    client.start()
