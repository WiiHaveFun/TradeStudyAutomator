import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog as fd
import math


class FilePickerFrame(ttk.Frame):
    def __init__(self, container, file_type_name, file_type, header_displayer=None):
        super().__init__(container)

        # file parameters and file data
        self.fileType = file_type
        self.fileTypeName = file_type_name
        self.f = None
        self.data = None

        self.readerWindow = None

        # buttons
        self.buttonFrame = ttk.Frame(self)
        self.readButton = ttk.Button(self.buttonFrame, text="Choose file")
        self.viewButton = ttk.Button(self.buttonFrame, text="View file")

        # path label
        self.filePathLabel = ttk.Label(self, text="Path:")

        # header displayer
        self.headerDisplayer = header_displayer

        self.create_widgets()

    def create_widgets(self):
        self.readButton['command'] = self.choose_file
        self.viewButton['command'] = self.view_file

        self.readButton.grid(column=0, row=0, sticky=tk.W, padx=5, pady=5)
        self.viewButton.grid(column=1, row=0, sticky=tk.W, padx=5, pady=5)
        self.buttonFrame.grid(column=0, row=0, sticky=tk.W)
        self.filePathLabel.grid(column=0, row=1, columnspan=2, sticky=tk.W, padx=5, pady=5)

    def choose_file(self):
        # file type
        file_types = {
            (self.fileTypeName, self.fileType),
        }

        # show the open file dialog
        f_name = fd.askopenfilename(filetypes=file_types)

        # display file path and read file if a file is picked
        if f_name:
            self.f = open(f_name)
            self.filePathLabel['text'] = "Path: " + self.f.name
            self.data = self.f.read()
            self.f.close()

            if self.headerDisplayer is not None and self.fileType == "*.csv":
                self.headerDisplayer.update_headers(self.get_csv_data())



    def view_file(self):
        if self.f is not None:
            if self.readerWindow is None:
                self.readerWindow = tk.Toplevel()
                self.readerWindow.geometry("750x375")
                self.readerWindow.title(self.f.name)
                self.readerWindow.protocol('WM_DELETE_WINDOW', self.remove_window)

                if self.fileType == "*.csv":
                    self.view_csv()
                else:
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

    # TODO Make scrollable
    def view_csv(self):
        data_array = self.get_csv_data()

        for r, row_array in enumerate(data_array):
            if r > 0:
                ttk.Label(self.readerWindow, text=r).grid(column=0, row=r, sticky=tk.W, padx=5)
            for c, entry in enumerate(row_array):
                ttk.Label(self.readerWindow, text=entry).grid(column=c + 1, row=r, padx=20)

    def get_data(self):
        return self.data

    def get_csv_data(self):
        data_array = [r.split(",") for r in self.data.split("\n")]
        return data_array

    def is_file_picked(self):
        return self.f is not None
