import socket

# Host server
serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serv.bind(('0.0.0.0', 8080))
print("< successfully created a new game server >")
serv.listen(5)
print("< waiting for another player to join game >")

# Accept client connection
conn, addr = serv.accept()
print("< anoter player joined your game >")

# Listen for connection message from client
from_client = conn.recv(4096).decode()
print("from_client:\n" + from_client)

# Send verification message to client
conn.send(str.encode("I am SERVER\n"))

# Game loop
while True:
    # Send message to client
    msg = input("- send message to client (q to quite game): ")
    conn.send(str.encode(msg))
    if(msg == "q"): # To quit the current online game
        print("< closing server >")
        break

    # Listen for message from client
    from_client = conn.recv(4096).decode()
    print("from_client:\n" + from_client)
    if(from_client == "q"): # If client quit the current online game
        print("< closing server >")
        break


conn.close()
