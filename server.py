import os
import socket
import threading
import time

IP = "localhost"
PORT = 4450
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8"
SERVER_PATH = "server_files"  # Directory for storing server files


def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    conn.send("OK@Welcome to the file sharing server".encode(FORMAT))

    while True:
        try:
            data = conn.recv(SIZE).decode(FORMAT)
            cmd, *args = data.split("@")
            send_data = "OK@"

            if cmd == "LOGOUT":
                break

            elif cmd == "UPLOAD":
                filename, filesize = args
                filesize = int(filesize)
                if os.path.exists(os.path.join(SERVER_PATH, filename)):
                    conn.send(f"ERROR@File {filename} already exists.".encode(FORMAT))
                else:
                    with open(os.path.join(SERVER_PATH, filename), "wb") as f:
                        received = 0
                        while received < filesize:
                            bytes_read = conn.recv(SIZE)
                            f.write(bytes_read)
                            received += len(bytes_read)
                    conn.send(f"OK@Upload of {filename} complete.".encode(FORMAT))

            elif cmd == "DOWNLOAD":
                filename = args[0]
                filepath = os.path.join(SERVER_PATH, filename)
                if os.path.exists(filepath):
                    filesize = os.path.getsize(filepath)
                    conn.send(f"OK@{filesize}".encode(FORMAT))
                    with open(filepath, "rb") as f:
                        while (bytes_read := f.read(SIZE)):
                            conn.sendall(bytes_read)
                else:
                    conn.send(f"ERROR@File {filename} does not exist.".encode(FORMAT))

            elif cmd == "DELETE":
                filename = args[0]
                filepath = os.path.join(SERVER_PATH, filename)
                if os.path.exists(filepath):
                    os.remove(filepath)
                    conn.send(f"OK@File {filename} deleted.".encode(FORMAT))
                else:
                    conn.send(f"ERROR@File {filename} not found.".encode(FORMAT))

            # checks for directories in server files
            elif cmd == "DIR":
                directories = ""
                for file in os.listdir(SERVER_PATH):
                    possibleDirectory = os.path.join(SERVER_PATH, file)
                    if os.path.isdir(possibleDirectory):
                        directories += file
                        directories += "\n"
                if directories != "":
                    send_data += directories
                else:
                    send_data += "No directories"
                conn.send(send_data.encode(FORMAT))

        except Exception as e:
            conn.send(f"ERROR@{str(e)}".encode(FORMAT))
            break

    print(f"{addr} disconnected")
    conn.close()


def main():
    if not os.path.exists(SERVER_PATH):
        os.makedirs(SERVER_PATH)
    
    # create text2 file in server files
    filename = "text2.txt"
    with open(os.path.join(SERVER_PATH, filename), "w") as file:
        file.write("This is a test file for the server.")
        file.close()
    #create files file in server files
    filename = "files.txt"
    with open(os.path.join(SERVER_PATH, filename), "w") as file:
        file.write("This is files.txt for the server.")
        file.close()


    print("Starting the server")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen()
    print(f"Server is listening on {IP}: {PORT}")

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()


if __name__ == "__main__":
    main()