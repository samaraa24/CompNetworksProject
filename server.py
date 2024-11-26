import os
import socket
import threading
import time
import shutil
import network_analysis

IP = "localhost"
PORT = 4450
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8"
SERVER_PATH = "server_files"  # Directory for storing server files

# handles the client's commands
def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    conn.send("OK@Welcome to the file sharing server".encode(FORMAT))
    current_directory = SERVER_PATH

    # while the server is handling the client(s)
    while True:
        try:
            data = conn.recv(SIZE).decode(FORMAT)
            cmd, *args = data.split("@")
            send_data = "OK@"

            # logout command
            if cmd == "LOGOUT":
                break
            
            # uploads the file chosen by the user
            elif cmd == "UPLOAD":
                filename, filesize = args
                filesize = int(filesize)
                filepath = os.path.join(SERVER_PATH, filename)
                if os.path.exists(filepath):
                    conn.send(f"ERROR@File {filename} already exists.".encode(FORMAT))
                else:
                    start_time = int(round(time.time() * 1000000000))
                    with open(filepath, "wb") as f:
                        received = 0
                        while received < filesize:
                            bytes_read = conn.recv(SIZE)
                            f.write(bytes_read)
                            received += len(bytes_read)
                    end_time = int(round(time.time() * 1000000000))
                    network_analysis.update_database("Upload", os.path.basename(filename), filesize, start_time, end_time)
                    conn.send(f"OK@Upload of {filename} complete.".encode(FORMAT))

            # download the file specified by the user's input
            elif cmd == "DOWNLOAD":
                filename = args[0]
                filepath = os.path.join(SERVER_PATH, filename)
                if os.path.exists(filepath):
                    start_time = int(round(time.time() * 1000000000))
                    filesize = os.path.getsize(filepath)
                    conn.send(f"OK@{filesize}".encode(FORMAT))
                    with open(filepath, "rb") as f:
                        while (bytes_read := f.read(SIZE)):
                            conn.sendall(bytes_read)
                    end_time = int(round(time.time() * 1000000000))
                    network_analysis.update_database("Download", os.path.basename(filename), filesize, start_time, end_time)
                else:
                    conn.send(f"ERROR@File {filename} does not exist.".encode(FORMAT))

            # deletes the file input by the user
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
                files = ""
                current_directory = os.path.join(SERVER_PATH,args[0])
                for file in os.listdir(current_directory):
                    possibleDirectory = os.path.join(current_directory, file)
                    if os.path.isdir(possibleDirectory):
                        directories += "DIRECTORY "
                        directories += file
                        directories += "\n"
                    if not os.path.isdir(possibleDirectory):
                        files += "FILE "
                        files += file
                        files += "\n"
                if directories != "":
                    send_data += directories
                if files != "":
                    send_data += files
                if(directories == "") and (files == ""):
                    send_data += "No files or directories."
                conn.send(send_data.encode(FORMAT))
                

            # creates directories/subdirectories
            elif cmd == "CREATEDIR":
                current_directory = os.path.join(SERVER_PATH,args[0])
                filename = args[1]
                filepath = os.path.join(current_directory, filename)
                print(filepath)
                if not os.path.exists(filepath):
                    os.mkdir(filepath)
                    conn.send(f"OK@{filepath}".encode(FORMAT))
                else:
                    conn.send(f"ERROR@File {filepath} already exists or incorrect format.".encode(FORMAT))
            
            # deletes directories/subdirectories
            elif cmd == "DELETEDIR":
                current_directory = os.path.join(SERVER_PATH,args[0])
                filename = args[1]
                filepath = os.path.join(current_directory, filename)
                print(filepath)
                if os.path.exists(filepath):
                    shutil.rmtree(filepath)
                    conn.send(f"OK@{filepath}".encode(FORMAT))
                else:
                    conn.send(f"ERROR@File {filepath} does not exist".encode(FORMAT))

        # throws an exception
        except Exception as e:
            conn.send(f"ERROR@{str(e)}".encode(FORMAT))
            break

    # client has disconnected
    print(f"{addr} disconnected")
    conn.close()


def main():
    # if there is no server directory make one
    if not os.path.exists(SERVER_PATH):
        os.makedirs(SERVER_PATH)

    # starts the server
    print("Starting the server")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen()
    print(f"Server is listening on {IP}: {PORT}")

    # handles multithreading
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()


if __name__ == "__main__":
    main()
