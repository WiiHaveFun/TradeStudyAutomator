import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog as fd
import math


class FolderPickerFrame(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)

        # file parameters and file data
        self.dir = None
        self.data = None

        self.readerWindow = None

        # buttons
        self.buttonFrame = ttk.Frame(self)
        self.readButton = ttk.Button(self.buttonFrame, text="Choose file")
        self.viewButton = ttk.Button(self.buttonFrame, text="View file")

        # path label
        self.filePathLabel = ttk.Label(self, text="Path:")

        self.create_widgets()

    def create_widgets(self):
        self.readButton['command'] = self.choose_folder
        self.viewButton['command'] = self.view_first_file

        self.readButton.grid(column=0, row=0, sticky=tk.W, padx=5, pady=5)
        self.viewButton.grid(column=1, row=0, sticky=tk.W, padx=5, pady=5)
        self.buttonFrame.grid(column=0, row=0, sticky=tk.W)
        self.filePathLabel.grid(column=0, row=1, columnspan=2, sticky=tk.W, padx=5, pady=5)

    def choose_folder(self):
        # show the open file dialog
        directory = fd.askdirectory()

        # display file path and read file if a file is picked
        if directory:
            try:
                f = open(directory + "/data1.txt")
            except FileNotFoundError:
                tk.messagebox.showwarning(
                    message="Folder missing data files\ndata1.txt must be present\nPlease try again"
                )
            else:
                self.dir = directory
                self.filePathLabel['text'] = "Path: " + self.dir
                self.data = f.read()

    def view_first_file(self):
        if self.dir is not None:
            if self.readerWindow is None:
                self.readerWindow = tk.Toplevel()
                self.readerWindow.geometry("750x375")
                self.readerWindow.title(self.dir + "/data1.txt")
                self.readerWindow.protocol('WM_DELETE_WINDOW', self.remove_window)

                self.view_text()

    def remove_window(self):
        self.readerWindow.destroy()
        self.readerWindow = None

    def view_text(self):
        # Add line numbers
        lines = self.data.split("\n")

        order = math.floor(math.log(len(lines), 10))

        for i in range(len(lines)):
            lines[i] = str(i + 1).rjust(order + 1, " ") + "\t" + lines[i]
        numbered_data = "\n".join(lines)

        self.readerWindow.columnconfigure(0, weight=1)
        self.readerWindow.rowconfigure(0, weight=1)

        text = tk.Text(self.readerWindow)
        text.grid(column=0, row=0, sticky=tk.NSEW)
        text.insert(tk.END, numbered_data)
        text.configure(state=tk.DISABLED)

    def get_data(self):
        return self.data

    def is_folder_picked(self):
        return self.dir is not None
