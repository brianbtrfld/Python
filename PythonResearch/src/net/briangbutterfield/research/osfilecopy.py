'''
Created on Jul 18, 2012

@author: brianb
'''

import tkinter as tk
import os
import shutil
import datetime
from tkinter import *
from tkinter.filedialog import askopenfilenames

    
def doCopy():
    
    global entryWidget
    global statusWidget
    
    srcPath = "c:\\temp\\src"
    destPath = "c:\\temp\\dest"
    readMeFilePath = "c:\\temp\\dest\\ReadMe.txt"
    
    #prompt for file selection
    options = {}
    options['title'] = "Select APEX Files"
    options['initialdir'] = srcPath
    options['filetypes'] = [("txt files",".txt")]
    selectedFiles = askopenfilenames(**options)
    
    #split selected files string into a list
    fileList = root.tk.splitlist(selectedFiles)
    
    
    #delete .apex existing files
    deleteFiles = entryDelete.get().strip()
    if deleteFiles == "yes":
        for filename in os.listdir(destPath):
            deleteFile = os.path.join(destPath, filename)
            if deleteFile.endswith(".txt"):
                os.remove(deleteFile)
                statusWidget.insert(END, "\n" + "  Deleted File: " + filename)
                root.update_idletasks()
    
    #update status
    statusWidget.insert(END, "\n\n" + "Selected Files")
    for file in fileList:
        statusWidget.insert(END, "\n" + str(file))
        root.update_idletasks()
    
    #copy the files
    with open(readMeFilePath, mode = "a") as readMeFile:
        now = datetime.datetime.now()
        readMeFile.write("\n\n" + os.environ.get("USERNAME", "Butterfield") + " - " + now.strftime("%m-%d-%Y %H:%M %p"))
        readMeFile.write("\n" + entryWidget.get().strip())
        readMeFile.write("\n" + "Installed the following packages:")
        
        for copyFile in fileList:
            statusWidget.insert(END, "\n\n" + "Copying File: " + copyFile)
            statusWidget.yview(MOVETO, 1.0)
            root.update_idletasks()
            shutil.copy(copyFile, destPath)
            readMeFile.write("\n   [" + os.path.split(copyFile)[1] + "]")
            #update status
            statusWidget.insert(END, " - DONE!")
            root.update_idletasks()
            
        statusWidget.insert(END, "\n\n" + "COMPLETE!")        
        statusWidget.yview(MOVETO, 1.0)    
    
if __name__ == "__main__":
    
    root = tk.Tk()
    #root.withdraw()
    
    root.title("APEX File Copy Utility")
    root["padx"] = 20
    root["pady"] = 20
    
    # Create a text frame to hold the text Label and the Entry widget
    frame = Frame(root)
    frame["padx"] = 10
    frame["pady"] = 10
    frame.pack()
        
    logFrame = Frame(root)
    logFrame["padx"] = 10
    logFrame["pady"] = 10
    logFrame.pack(side=BOTTOM)

    #Create a Label in textFrame
    entryLabelLog = Label(frame)
    entryLabelLog["text"] = "Enter Log Message"
    entryLabelLog.pack(side=TOP)

    # Create an Entry Widget in textFrame
    entryWidget = Entry(frame)
    entryWidget["width"] = 100
    entryWidget.pack(side=TOP)
    
    #Create a Label in textFrame
    entryLabelDelete = Label(frame)
    entryLabelDelete["text"] = "Delete Existing Files?  Enter yes or no."
    entryLabelDelete.pack(side=TOP)
    
    #Delete entry prompt
    entryDelete = Entry(frame)
    entryDelete["width"] = 20
    entryDelete.insert(END, "no")
    entryDelete.pack(side=BOTTOM)
    
    #Status text view scrollbar
    statusWidgetScrollbar = Scrollbar(logFrame)
    statusWidgetScrollbar.pack(side=RIGHT, fill=Y)
    
    #Status text view
    statusWidget = Text(logFrame, yscrollcommand=statusWidgetScrollbar.set)
    statusWidget["width"] = 100
    statusWidget["height"] = 20
    statusWidget.pack(side=BOTTOM)
    
    statusWidgetScrollbar.config(command=statusWidget.yview)
    
    button = Button(root, text="Execute", command=doCopy)
    button.pack()

    root.mainloop()
    
    

