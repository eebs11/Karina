

def selectFile():
    import Tkinter as tk
    import tkFileDialog
    import os
    
    tkWindow = tk.Tk()
    
    # Build a list of tuples for each file type the file dialog should display
    my_filetypes = [('all files', '.*'), ('text files', '.txt')]
    
    # Ask the user to select a single file name.
    filePath = ""
    filePath = tkFileDialog.askopenfilename(parent=tkWindow,
                                        initialdir=os.getcwd(),
                                        title="Please select a file:",
                                        filetypes=my_filetypes)
    
    tkWindow.destroy()
    
    return(filePath)
