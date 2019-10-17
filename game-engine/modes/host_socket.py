from multiprocessing.connection import Listener
import socket
from modes.host_game import HostGame
from screens.host_game import waiting_for_other_player


def host_socket(screen):

    # Setup socket object and host the server
    serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    host_name = socket.gethostname()
    host_ip = socket.gethostbyname(host_name)
    host_port = 8080

    serv = Listener((host_ip, host_port))

    # Another player has connected to the host's server
    client_socket = waiting_for_other_player(screen, serv, host_ip)

    print("CONNECT")
    client_socket.send("\tstarting game...")    # Send verification message to client

    # Start the online Game
    game = HostGame(screen, client_socket)
    game.game_loop() # Loops until a player presses Q to quit the game session

    client_socket.close() # Close the connection
    serv.close() # Close the socket and server
