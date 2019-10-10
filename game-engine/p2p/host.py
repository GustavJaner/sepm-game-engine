import socket

# Host server
serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serv.bind(('0.0.0.0', 8080))
serv.listen(5)

while True:
    # Accept client connection
    conn, addr = serv.accept()

    # Listen for connection message from client
    from_client = conn.recv(4096).decode()
    print(from_client)

    # Send verification message to client
    msg = str.encode("I am SERVER\n")
    conn.send(msg)

    while True:
        # Send message to client
        msg = str.encode(input("send message to client: "))
        conn.send(msg)

        # Listen for message from client
        from_client = conn.recv(4096).decode()
        print(from_client)


    conn.close()
