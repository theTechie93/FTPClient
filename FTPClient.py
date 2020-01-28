import os
import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import askopenfilename
from tkinter.ttk import *

import paramiko

titleName = "FTP Client"


def printTotals(transferred, toBeTransferred):
    print("Transferred: {0}\tOut of: {1}".format(transferred, toBeTransferred))


def UploadFile(fileName, hostName, UName, hostPass, RemPath):
    HostName = hostName.get()
    UserName = UName.get()
    HostPass = hostPass.get()
    FullFile = fileName.get()
    FileName = os.path.basename(FullFile)
    RemotePath = RemPath.get()
    fileName.set("")
    s = paramiko.SSHClient()
    s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    s.connect(HostName, 22, username=UserName, password=HostPass, timeout=4)
    sftp = s.open_sftp()
    sftp.put(FullFile, RemotePath + FileName, callback=printTotals)
    messagebox.showinfo("Info",
                        "The File: " + FullFile + "\nUploaded Successfully to the FTP Server\n" + "ftp://" + HostName + RemotePath)

class Application(Frame):
    def __init__(self, master):
        super(Application, self).__init__(master)
        self.grid()
        self.createGUI()

    def pch_file_dialog(self):
        try:
            file = askopenfilename(initialdir="C:/",
                                   filetypes=(("Select File", "*.*"), ("all files", "*.*")),
                                   title="Select  File")
            FileName.set(file)
            self.SelectPCH.xview_moveto(1)
            return file
        except TypeError:
            from tkinter import messagebox
            messagebox.showinfo("", "No File Selected")
            return

    def createGUI(self):
        global FileName
        global hostName
        global hostPass
        global UName
        global RemPath
        FileName = StringVar()
        hostName = StringVar()
        hostPass = StringVar()
        UName = StringVar()
        RemPath = StringVar()
        self.MainFrame = tk.LabelFrame(self, text="FTP Client", )
        self.MainFrame.pack(padx=5, pady=10, ipadx=150, ipady=110)

        self.HostLabelName = Label(self.MainFrame, text="Host:")
        self.HostLabelName.place(x=10, y=20)

        self.Host = Entry(self.MainFrame, textvariable=hostName, width=20)
        self.Host.place(x=80, y=20)
        self.Host.insert(END, "Host IP Address")

        self.UserLabelName = Label(self.MainFrame, text="User Name:")
        self.UserLabelName.place(x=10, y=50)
        self.UName = Entry(self.MainFrame, textvariable=UName, width=20)
        self.UName.place(x=80, y=50)
        self.UName.insert(END, "Username")

        self.PassLabelName = tk.Label(self.MainFrame, text="Password:")
        self.PassLabelName.place(x=10, y=80)

        self.Pass = Entry(self.MainFrame, show="*", textvariable=hostPass, width=20)
        self.Pass.place(x=80, y=80)
        self.Pass.insert(END, "Password")

        self.PassLabelName = tk.Label(self.MainFrame, text="Remote Path:")
        self.PassLabelName.place(x=10, y=110)

        self.Pass = Entry(self.MainFrame, textvariable=RemPath, width=20)
        self.Pass.place(x=80, y=110)
        self.Pass.insert(END, "Remote Path")

        self.LabelName = tk.Label(self.MainFrame, text="Select File:")
        self.LabelName.place(x=10, y=140)
        self.SelectPCH = Entry(self.MainFrame, textvariable=FileName, width=20)
        self.SelectPCH.place(x=80, y=140)

        self.BrowsButton = tk.Button(self.MainFrame, width=10, text="Browse",
                                     command=lambda: self.pch_file_dialog())
        self.BrowsButton.place(x=210, y=140)

        self.BrowsButton = tk.Button(self.MainFrame, width=10, text="Upload",
                                     command=lambda: UploadFile(FileName, hostName, UName, hostPass, RemPath))
        self.BrowsButton.place(x=210, y=170)


root = Tk()
root.title(titleName)
root.geometry("320x250")
app = Application(root)
root.mainloop()
