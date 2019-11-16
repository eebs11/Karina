# -*- coding: utf-8 -*-
"""
Created on Wed Nov 08 16:59:08 2017

@author: 425196
"""



def selectFolder():
    import Tkinter as tk
    import tkFileDialog
    import os
    
    tkWindow = tk.Tk()
    
    # Build a list of tuples for each file type the file dialog should display
    my_filetypes = [('all files', '.*'), ('text files', '.txt')]
    
    # Ask the user to select a single file name.
    folderPath = ""
    folderPath = tkFileDialog.askdirectory(parent=tkWindow, title="Select A Folder", mustexist=1,
                                        initialdir=os.getcwd()
                                        )
    
    tkWindow.destroy()

    return(folderPath)
