# client UI

# import module 
from tkinter import *
from tkinter import filedialog
import socket
import os

 #files database
with open("files.txt", "r") as file:
    content = file.read().splitlines()

# server information
IP = "localhost"
PORT = 4450
SIZE = 1024
FORMAT = "utf-8"
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# create root window 
root = Tk()

# main window title and dimension 
root.title("File Sharing Cloud Service")
root.geometry('600x500')

# commmand when user wants to upload a file 
def upload_file():
    #allows user to upload text, audio, and video files 
    filename = filedialog.askopenfilename(title= "Select a file", filetypes=[("Text files", ".txt"),
                                                                             ("Audio files", ".mp3"), 
                                                                             ("Video files", ".mp4")])
    # opens file for reading
    f = open(filename, 'rb')
    print('Selected:', filename)

    # sends upload command with file name and size
    s.send(f"UPLOAD@{os.path.basename(filename)}@{os.path.getsize(filename)}".encode(FORMAT))

    # sends data to server
    sendData = f.read(1024)
    while (sendData):
        s.send(sendData)
        sendData = f.read(1024)
    f.close()

    # receives status from server
    data = s.recv(SIZE).decode(FORMAT)
    status, msg = data.split("@")
    print(status,": ",msg)


# command when user wants to download a file
def download_file():
    filename = "text2.txt" # placeholder for filename input
    s.send(f"DOWNLOAD@{filename}".encode(FORMAT))
    data = s.recv(SIZE).decode(FORMAT)
    status, msg = data.split("@")

    if status == "OK":
        filesize = int(msg)

        f = open(filename, 'wb')
        bytes_received = 0
        while bytes_received < filesize:
            bytes_read = s.recv(SIZE)
            f.write(bytes_read)
            bytes_received += len(bytes_read)

        print(f"Download of {filename} complete.")

    else:
        print(status,": ", msg)


# from main window to upload window where user would actually upload files after connecting to server 
def connect_server():
    # would connect to server 
    s.connect((IP, PORT))
    data = s.recv(SIZE).decode(FORMAT)
    status, msg = data.split("@")
    
    connect.configure(text = msg) #stand in text for the actual action

    # menu of options
    listbox = Listbox(root, height = 10, 
                    width = 15, 
                    bg = "grey",
                    activestyle = 'dotbox', 
                    font = "Helvetica",
                    fg = "yellow")
        
    # upload files button
    upload = Button(root, text = "Upload File", fg = "blue", command = upload_file)
    upload.pack()

    # download files button
    download = Button(root, text = "Download Files", fg = "blue", command = download_file)
    download.pack()

    # view list of files button
    view_files = Button(root, text = "View All Files", fg = "blue", command = NONE)
    view_files.pack()
        
        
    listbox.insert(1, upload)
    listbox.insert(1, download)
    listbox.insert(1, view_files)



# connect server IP port -> initiate connection from client to server with specified files 
connect = Button(root, text = "Connect to Server", fg = "blue", command = connect_server)
connect.pack()


# delete files


# execution
root.mainloop()
