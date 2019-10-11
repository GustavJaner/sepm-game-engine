import socket

# Connect to host
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('0.0.0.0', 8080))
print("< successfully joined a new online game >")

# Send connection message to host
client.send(str.encode("I am CLIENT\n"))

# Listen for verification message from host
from_host = client.recv(4096).decode()
print("from_host:\n" + from_host)

# Game loop
while True:
    # Listen for message from host
    from_host = client.recv(4096).decode()
    print("from_host:\n" + from_host)
    if(from_host == "q"): # If host quit the current online game
        print("< leaving game >")
        break

    # Send message to host
    msg = input("- send message to host (q to quite game): ")
    client.send(str.encode(msg))
    if(msg == "q"): # To quit the current online game
        print("< leaving game >")
        break


client.close()
