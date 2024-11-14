# client UI

# import module 
from tkinter import *
from tkinter import filedialog

 #files database
with open("files.txt", "r") as file:
    content = file.read().splitlines()


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
    print('Selected:', filename)

    #checks if file already exists in server or not 
    if filename not in content:
        #open file to edit it 
        with open("files.txt", "a") as file:
            #add file name to the files database 
            file.write(filename + "\n")

    else:
        print('File already exists in Server')



# from main window to upload window where user would actually upload files after connecting to server 
def connect_server():
    # would connect to server 

    connect.configure(text = "Welcome to File Sharing Cloud Service") #stand in text for the actual action

    #menu of options
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
    download = Button(root, text = "Download Files", fg = "blue", command = NONE)
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


# subfolders 

# execution
root.mainloop()
