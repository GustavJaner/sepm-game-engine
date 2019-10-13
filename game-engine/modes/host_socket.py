import socket
from modes.host_game import HostGame
from screens.host_game import waiting_for_other_player


def host_socket(screen):

    # Setup socket object and host the server
    serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    host_name = socket.gethostname()
    host_ip = socket.gethostbyname(host_name)
    host_port = 8080

    serv.bind((host_ip, host_port))
    serv.listen(1)                  # Listen and accept only one connection

    # Another player has connected to the host's server
    client_socket, client_ip = waiting_for_other_player(screen, serv, host_ip)
    client_socket.send(str.encode("\tstarting game..."))    # Send verification message to client

    # Start the online Game
    game = HostGame(screen, client_socket)
    game.game_loop() # Loops until a player presses Q to quit the game session

    # End and close the online Session
    # msg = "q"
    # client_socket.send(str.encode(msg))
    # serv.shutdown('SHUT_RDWR')
    client_socket.close() # Close the connection
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
