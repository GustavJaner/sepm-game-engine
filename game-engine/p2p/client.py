import socket

# Connect to server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('0.0.0.0', 8080))

# Send connection message to server
msg = str.encode("I am CLIENT\n")
client.send(msg)

# Listen for verification message from server
from_server = client.recv(4096).decode()
print(from_server)

while True:
    # Listen for message from server
    from_server = client.recv(4096).decode()
    print(from_server)

    # Send message to server
    msg = str.encode(input("send message to server: "))
    client.send(msg)


client.close()
