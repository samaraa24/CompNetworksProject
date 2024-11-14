# client UI

# import module 
from tkinter import *

# create root window 
root = Tk()

# main window title and dimension 
root.title("File Sharing Cloud Service")
root.geometry('600x500')

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
    upload = Button(root, text = "Upload File", fg = "blue", command = NONE)
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





