import socket
import threading

disconnectmsg = "/quit"
activeconn = 0
clientbroadlist = []

def broadcast(message):
    for client in clientbroadlist: #used to send message to every client connected to server
        client.send(message.encode())

def handle_client(client, addr):
    global activeconn, server #established global variables to be used across entire program
    print(f"New Connection: {addr}")
    with open("output-server-5000.txt", "a") as f:
        f.write(f"\nNew Connection: {addr}\n")
    connected = True
    while connected:
        message = client.recv(1024).decode()
        if not message:
            connected = False
        elif message == disconnectmsg:
            connected = False
            client.send("Server: Disconnected client successfully.".encode())
            with open("output-server-5000.txt", "a") as f:
                f.write("\nServer: Disconnected client successfully.\n")
        else:
            broadcast(f"{addr}: {message}")
    activeconn -= 1
    clientbroadlist.remove(client)
    print(f"Update -> Active Connections: {activeconn}")
    with open("output-server-5000.txt", "a") as f:
        f.write(f"\nUpdate -> Active Connections: {activeconn}\n")
    if activeconn == 0: #when activeconn == 0 after clients have disconnected
        print("All Connections Expired. Shutting Down Now.")
        with open("output-server-5000.txt", "a") as f:
            f.write("\nAll Connections Expired. Shutting Down Now.\n")
        server.close()
    client.close()

def main():
    global activeconn, server
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("127.0.0.1", 5000))
    print("Server established.")
    with open("output-server-5000.txt", "w") as f: #using w to overwrite previous program run's output
        f.write("01631411 - Maxwell Duesing\n")
        f.write("\nServer established.\n")
    server.listen()
    server.settimeout(1)
    
    while True:
        try:
            client, addr = server.accept()
        except socket.timeout:
            continue
        except OSError:
            break
        connmsg = client.recv(1024).decode() #the message sent by the client once the connection is established
        print(connmsg)
        activeconn += 1
        clientbroadlist.append(client)
        print(f"Active Connections: {activeconn}")
        with open("output-server-5000.txt", "a") as f:
            f.write(f"\nActive Connections: {activeconn}\n")
        thread = threading.Thread(target=handle_client, args=(client, addr))
        thread.start()

if __name__ == "__main__":
    main()

