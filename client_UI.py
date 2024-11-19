# client UI

# import module 
from tkinter import *
from tkinter import filedialog
from tkinter import simpledialog
from tkinter import messagebox
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

# create windows
root = Tk()
file_window = Toplevel(root)

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


def view_all_files():

    #sending command to server 
    s.send("DIR@".encode(FORMAT))

    #receiving response 
    response = s.recv(SIZE).decode(FORMAT)
    status, files = response.split("@",1)

    #new window will open with the file database
    file_window.title("File Database")
    file_window.geometry('600x500')

    #making listbox inside new window to display the files 
    file_listbox = Listbox(file_window,height=15, 
                           width=50, bg="lightgrey", 
                           font=("Helvetica", 12), fg="black")
    file_listbox.pack(pady = 10, padx = 10, fill = BOTH, expand = True)

    #adding a scrollbar 
    scrollbar = Scrollbar(file_window)
    scrollbar.pack(side = RIGHT, fill = BOTH)
    file_listbox.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=file_listbox.yview)

    #when it finds the files, if the server isnt empty, the files will be displayed 
    if status == "OK":

        if files.strip():
            file_list = files.strip().split("\n")
        
            for file in file_list:
                file_listbox.insert(END, file)

        else:
            file_listbox.insert(END, "SERVER IS EMPTY")
            
    else:
        file_listbox.insert(END,f"Error: {files}")



def delete_files():
    file_window

    filename = simpledialog.askstring("Delete Files", "Enter File Name")
   
    if filename:
        #sending delete command to server
        s.send(f"DELETE@{filename}".encode(FORMAT))

        #receive server's response 
        response = s.resv(SIZE).decode(FORMAT)
        status, message = response.split("@", 1)

        #server response 
        if status == "OK":
            messagebox.showinfo("{filename} was successfully deleted", message)
        else:
            messagebox.showerror("Error", message)
    else: 
        print("File does not exist")
            

# from main window to upload window where user would actually upload files after connecting to server 
def connect_server():
    # connecting to server 
    s.connect((IP, PORT))
    data = s.recv(SIZE).decode(FORMAT)
    status, msg = data.split("@")
    

    connect.configure(text = msg) #stand in text for the actual action
    connect.place(x = 180, y = 0)

    # menu of options
    listbox = Listbox(root, height = 10, 
                    width = 15, 
                    bg = "grey",
                    activestyle = 'dotbox', 
                    font = "Helvetica",
                    fg = "yellow")

    # upload files button
    upload = Button(root, text = "Upload File", fg = "black", command = upload_file)
    upload.pack()
    upload.place(x = 240, y = 30)

    # download files button
    download = Button(root, text = "Download Files", fg = "black", command = download_file)
    download.pack()
    download.place(x = 228, y = 60)

    # view list of files button
    view_files = Button(root, text = "View All Files", fg = "black", command = view_all_files)
    view_files.pack()
    view_files.place(x = 235, y = 90)

    delete = Button(root, text = "Delete Files", fg = "black", command = delete_files)
    delete.pack()
    delete.place(x = 240, y = 120)
        
    listbox.insert(1, upload)
    listbox.insert(2, download)
    listbox.insert(3, view_files)
    listbox.insert(4, delete)


# connect server IP port -> initiate connection from client to server with specified files 
connect = Button(root, text = "Connect to Server", fg = "black", bg = "blue", command = connect_server)
connect.pack(pady = 30)
connect.place(x = 220, y = 180)


# execution
root.mainloop()
file_window.mainloop()
