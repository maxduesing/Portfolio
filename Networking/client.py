import socket
import threading

disconnectmsg = "/quit"

def recbroadmsg(client, clientport): #need clientport to write to output file correctly
    while True:
        message = client.recv(1024).decode()
        if not message:
            break
        print(message)
        with open(f"output-client-{clientport}.txt", "a") as f:
            f.write(f"\nReceived: {message}\n") #specifies in output files which are received messages


def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("127.0.0.1", 5000))
    clientport = client.getsockname()[1]
    with open(f"output-client-{clientport}.txt", "w") as f: #using w to overwrite previous program run's output
        f.write("01631411 - Maxwell Duesing\n")
    client.send("New Client has Connected to Server".encode()) # encode to convert into bytes to send
    print("Your device has connected successfully to the server.")
    with open(f"output-client-{clientport}.txt", "a") as f:
        f.write("\nYour device has connected successfully to the server.\n")
    thread = threading.Thread(target=recbroadmsg, args=(client, clientport))
    thread.start()
    connected = True
    while connected:
        message = input("")
        client.send(message.encode())
        with open(f"output-client-{clientport}.txt", "a") as f:
            f.write(f"\nSent: {message}\n") #specifies in output files which are sent messages
        if message == disconnectmsg:
            connected = False

if __name__ == "__main__":
    main()
