import socket
import json
from modes.online_game import OnlineGame
from screens.host_game import waiting_for_other_player

def hostGame(screen):

    # Setup socket object and host the server
    serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    host_name = socket.gethostname()
    host_ip = socket.gethostbyname(host_name)
    host_port = 8080

    serv.bind((host_ip, host_port))
    serv.listen(1)                  # Listen and accept only one connection

    # Another player has connected to the host's server
    conn, addr = waiting_for_other_player(screen, serv, host_ip)
    conn.send(str.encode("\tstarting game..."))    # Send verification message to client


    # Start the online Game
    game = OnlineGame(screen, conn)
    game.game_loop() # Loops until a player presses Q to quit the game session


    # End and close the online Session
    msg = "q"
    conn.send(str.encode(msg))
    #socket.shutdown(SHUT_RDWR)
    conn.close() # Close the connection
    serv.close() # Close the socket and server







    # # Game loop
    # while True:
    #     # Send message to client
    #     msg = "LETS PLAY!"
    #     conn.send(str.encode(msg))
    #     if(msg == "q"): # To quit the current online game
    #         print("< closing server >")
    #         break
    #
    #     # Listen for message from client
    #     from_client = conn.recv(4096).decode()
    #     print("from_client:\n" + from_client)
    #     # print(json.dumps(from_client))
    #
    #     if(from_client == "q"): # If client quit the current online game
    #         print("< closing server >")
    #         break
    #
    #
