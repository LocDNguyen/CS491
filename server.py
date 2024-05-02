# import socket
# from _thread import *
# from game import Spaceship
# import pickle
# from constants import *

# import pygame

# server = "192.168.254.12"
# port = 5555

# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# try:
#     s.bind((server, port))
# except socket.error as e:
#     str(e)

# s.listen(2)
# print("Waiting for a connection, Server Started")

# win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# players = [Spaceship(SCREEN_WIDTH/2 - 50, SCREEN_HEIGHT - 100, 1), Spaceship(SCREEN_WIDTH/2 + 50, SCREEN_HEIGHT - 100, 1)]

# def threaded_client(conn, player):
#     conn.send(pickle.dumps(players[player]))
#     reply = ""
#     while True:
#         try:
#             data = pickle.loads(conn.recv(2048))
#             players[player] = data

#             if not data:
#                 print("Disconnected")
#                 break
#             else:
#                 if player == 1:
#                     reply = players[0]
#                 else:
#                     reply = players[1]

#                 print("Received: ", data)
#                 print("Sending : ", reply)

#             conn.sendall(pickle.dumps(reply))
#         except:
#             break

#     print("Lost connection")
#     conn.close()

# currentPlayer = 0
# while True:
#     conn, addr = s.accept()
#     print("Connected to:", addr)

#     start_new_thread(threaded_client, (conn, currentPlayer))
#     currentPlayer += 1

import socket
from _thread import *
import pickle
from game import Game

server = "192.168.254.12"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)
print("Waiting for a connection, Server Started")

connected = set()
games = {}
idCount = 0


def threaded_client(conn, p, gameId):
    global idCount
    conn.send(str.encode(str(p)))

    reply = ""
    while True:
        try:
            data = conn.recv(4096).decode()

            if gameId in games:
                game = games[gameId]

                if not data:
                    break
                else:
                    if data == "reset":
                        game.resetWent()
                    elif data != "get":
                        game.play(p, data)

                    conn.sendall(pickle.dumps(game))
            else:
                break
        except:
            break

    print("Lost connection")
    try:
        del games[gameId]
        print("Closing Game", gameId)
    except:
        pass
    idCount -= 1
    conn.close()



while True:
    conn, addr = s.accept()
    print("Connected to:", addr)

    idCount += 1
    p = 0
    gameId = (idCount - 1)//2
    if idCount % 2 == 1:
        games[gameId] = Game(gameId)
        print("Creating a new game...")
    else:
        games[gameId].ready = True
        p = 1


    start_new_thread(threaded_client, (conn, p, gameId))