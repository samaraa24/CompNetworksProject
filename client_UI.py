# client UI

# import module 
from tkinter import *
from tkinter import filedialog
from tkinter import simpledialog
from tkinter import messagebox
import socket
import os


# server information
IP = "localhost"
PORT = 4450
SIZE = 1024
FORMAT = "utf-8"
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
current_directory = ""

# create windows
root = Tk()

# main window title and dimension 
root.title("File Sharing Cloud Service")
root.geometry('600x500')

# stating the maximum file sizes in bytes 
MAX_FILE_SIZES = {
    ".txt" : 25 * 1024 * 1024, # 25 MB
    ".mp3" : 0.5 * 1024 * 1024 * 1024, #0.5 GB
    ".mp4" : 2 * 1024 * 1024 * 1024 #2 GB
}


# commmand when user wants to upload a file 
def upload_file():
    # allows user to upload text, audio, and video files 
    filename = filedialog.askopenfilename(title= "Select a file", filetypes=[("Text files", ".txt"),
                                                                             ("Audio files", ".mp3"), 
                                                                             ("Video files", ".mp4")])

    # returns if no file is selected
    if not filename:
        return
 
    # checks for file extension chosen to connect it to it's file size
    file_extension = os.path.splitext(filename)[1]
    file_size = os.path.getsize(filename)       

    # sending error message if user selects incorrect file size 
    while file_size > MAX_FILE_SIZES[file_extension]:
        messagebox.showerror("Error", "File does not meet size requirement")
        filename = filedialog.askopenfilename(title= "Select a file", filetypes=[("Text files", ".txt"),
                                                                             ("Audio files", ".mp3"), 
                                                                             ("Video files", ".mp4")])
        # returns if no file is selected
        if not filename:
            return

        # checks for file extension chosen to connect it to it's file size
        file_extension = os.path.splitext(filename)[1]
        file_size = os.path.getsize(filename)    

    f = open(filename, 'rb')
    print('Selected:', filename)

    file_path = os.path.join(current_directory, os.path.basename(filename))

    # sends upload command with file name and size
    s.send(f"UPLOAD@{file_path}@{file_size}".encode(FORMAT))

    # sends data to server
    sendData = f.read(SIZE)
    while (sendData):
        s.send(sendData)
        sendData = f.read(SIZE)
    f.close()

    # receives status from server
    data = s.recv(SIZE).decode(FORMAT)
    status, msg = data.split("@")
    print(status,": ",msg)


# command when user wants to download a file
def download_file():
    # allows user to type the name of the file they are trying to download
    filename = simpledialog.askstring("Download File","Enter File Name")

    if not filename:
        return

    # appends the file path to include the current directory and sends to server
    file_path = os.path.join(current_directory, filename)
    s.send(f"DOWNLOAD@{file_path}".encode(FORMAT))

    # receives message from server
    data = s.recv(SIZE).decode(FORMAT)
    status, msg = data.split("@")

    if status == "OK":
        # server returns the size of the file
        filesize = int(msg)

        # a file is opened for writing in the directory the client program is located
        f = open(filename, 'wb')
        bytes_received = 0

        # receives data from server until the number of received bites reaches the file size
        while bytes_received < filesize:
            bytes_read = s.recv(SIZE)
            f.write(bytes_read)
            bytes_received += len(bytes_read)

        print(f"Download of {filename} complete.")

    # prints error message if unsuccessful download
    else:
        print(status,": ",msg)


def view_all_files():
    file_window = Toplevel(root)
    
    # sending command to server 
    s.send(f"DIR@{current_directory}".encode(FORMAT))

    # receiving response 
    response = s.recv(SIZE).decode(FORMAT)
    status, files = response.split("@",1)

    # new window will open with the file database
    file_window.title("File Database")
    file_window.geometry('600x500')

    # making listbox inside new window to display the files 
    file_listbox = Listbox(file_window,height=15, 
                           width=50, bg="lightgrey", 
                           font=("Helvetica", 12), fg="black")
    file_listbox.pack(pady = 10, padx = 10, fill = BOTH, expand = True)

    # adding a scrollbar 
    scrollbar = Scrollbar(file_window)
    scrollbar.pack(side = RIGHT, fill = BOTH)
    file_listbox.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=file_listbox.yview)

    # when it finds the files, if the server isnt empty, the files will be displayed 
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

    filename = simpledialog.askstring("Delete Files", "Enter File Name")

    file_path = os.path.join(current_directory, os.path.basename(filename))
   
    if filename:
        # sending delete command to server
        s.send(f"DELETE@{file_path}".encode(FORMAT))

        # receive server's response 
        response = s.recv(SIZE).decode(FORMAT)
        status, message = response.split("@", 1)

        # server response 
        if status == "OK":
            messagebox.showinfo(f"{filename} was successfully deleted", message)
        else:
            messagebox.showerror("Error", message)
    else: 
        print("File does not exist")


def create_directory():

    dirname = simpledialog.askstring("Create Directories", "Enter Directory Name")

    if dirname:
        #send create directory command to server
        s.send(f"CREATEDIR@{current_directory}@{dirname}".encode(FORMAT))

        # receive server's response
        response = s.recv(SIZE).decode(FORMAT)
        status, message = response.split("@", 1)

        #server response 
        if status == "OK":
            messagebox.showinfo(f"{dirname} was successfully created", message)
        else:
            messagebox.showerror("Error", message)
    else: 
        print("Directory already exists")

def delete_directory():

    dirname = simpledialog.askstring("Delete Directory", "Enter Directory Name")

    if dirname:
        #send create directory command to server
        s.send(f"DELETEDIR@{current_directory}@{dirname}".encode(FORMAT))

        # receive server's response
        response = s.recv(SIZE).decode(FORMAT)
        status, message = response.split("@", 1)

        #server response 
        if status == "OK":
            messagebox.showinfo(f"{dirname} was successfully deleted", message)
        else:
            messagebox.showerror("Error", message)
    else: 
        print("Directory does not exist.")

def change_dir():
    global current_directory

    # sends command and receives response
    s.send(f"DIR@{current_directory}".encode(FORMAT))
    response = s.recv(SIZE).decode(FORMAT)
    status, folders = response.split("@",1)

    if status == "OK":
        # dialog asks for the directory the user wants to change to
        folder_name = simpledialog.askstring("Change Directory","Enter Directory Name ('..' For Parent Directory)")

        if folder_name:
            folder = "DIRECTORY " + folder_name
        else:
            return
        
        if folder in folders:
            # changes to new folder if it is in the list returned by the server
            current_directory = os.path.join(current_directory, folder_name)
            print(current_directory)

        elif folder_name == ".." and current_directory:
            # changes to parent directory if there is one
            current_directory = os.path.dirname(current_directory)
            print(current_directory)
            
        else:
            # does not change directory if it does not exist
            messagebox.showerror("Error", "Error: Directory does not exist.")

    else:
        # prints error if OK status is not received
        messagebox.showerror(status,": ",folders)
            

# from main window to upload window where user would actually upload files after connecting to server 
def connect_server():
    # connecting to server 
    s.connect((IP, PORT))
    data = s.recv(SIZE).decode(FORMAT)
    status, msg = data.split("@")
    

    connect.configure(text = msg) # stand in text for the actual action
    connect.place(x = 180, y = 0)

    # menu of options
    listbox = Listbox(root, height = 10, 
                    width = 15, 
                    bg = "grey",
                    activestyle = 'dotbox', 
                    font = "Helvetica",
                    fg = "yellow")

    # upload files button
    upload = Button(root, text = "Upload File", fg = "blue", bg = "white", command = upload_file)
    upload.pack()
    upload.place(x = 240, y = 30)

    # download files button
    download = Button(root, text = "Download Files", fg = "blue", bg = "white", command = download_file)
    download.pack()
    download.place(x = 228, y = 60)

    # view list of files button
    view_files = Button(root, text = "View All Files", fg = "blue", bg = "white", command = view_all_files)
    view_files.pack()
    view_files.place(x = 235, y = 90)

    # delete files button
    delete = Button(root, text = "Delete Files", fg = "blue", bg = "white", command = delete_files)
    delete.pack()
    delete.place(x = 240, y = 120)

    # create directory button
    createDirectory = Button(root, text = "Create New Directory", fg = "blue", bg = "white", command = create_directory)
    createDirectory.pack()
    createDirectory.place(x = 210, y = 150)

    # create directory button
    deleteDirectory = Button(root, text = "Delete a Directory", fg = "blue", bg = "white", command = delete_directory)
    deleteDirectory.pack()
    deleteDirectory.place(x = 220, y = 180)

    # change directory button
    changeDir = Button(root, text = "Change Directory", fg = "blue", bg = "white", command = change_dir)
    changeDir.pack()
    changeDir.place(x = 220, y = 210)
    
    listbox.insert(1, upload)
    listbox.insert(2, download)
    listbox.insert(3, view_files)
    listbox.insert(4, delete)
    listbox.insert(5, createDirectory)
    listbox.insert(6, deleteDirectory)
    listbox.insert(7, changeDir)


# connect server IP port -> initiate connection from client to server with specified files 
connect = Button(root, text = "Connect to Server", fg = "black", bg = "white", command = connect_server)
connect.pack(pady = 30)
connect.place(x = 220, y = 180)


# execution
root.mainloop()
file_window.mainloop()
