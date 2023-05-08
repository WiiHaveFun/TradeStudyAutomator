import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog as fd


class FilePickerFrame(ttk.Frame):
    def __init__(self, container, file_type_name, file_type):
        super().__init__(container)

        self.fileType = file_type
        self.fileTypeName = file_type_name
        self.fName = None
        self.f = None
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
            ("All files", "*.*")
        }

        # show the open file dialog
        self.fName = fd.askopenfilename(filetypes=file_types)

        # display file path
        if self.fName is not None:
            self.filePathLabel['text'] = "Path: " + self.fName
            # self.data = self.f.read()

    def view_file(self):
        if self.fName is not None:
            if self.readerWindow is None:
                self.f = open(self.fName, "r")
                self.data = self.f.read()

                self.readerWindow = tk.Toplevel()
                self.readerWindow.geometry("750x375")
                self.readerWindow.title(self.fName)
                self.readerWindow.protocol('WM_DELETE_WINDOW', self.remove_window)

                if self.fileType == "*.csv":
                    self.view_csv()
                else:
                    self.view_text()

    def remove_window(self):
        self.readerWindow.destroy()
        self.readerWindow = None
        self.f.close()

    # TODO Make scrollable
    def view_csv(self):
        data_array = [r.split(",") for r in self.data.split("\n")]
        # print([r.split(",") for r in self.data.split("\n")])

        for r, row_array in enumerate(data_array):
            if r > 0:
                ttk.Label(self.readerWindow, text=r).grid(column=0, row=r, sticky=tk.W, padx=5)
            for c, entry in enumerate(row_array):
                ttk.Label(self.readerWindow, text=entry).grid(column=c + 1, row=r, padx=20)
                # self.readerWindow.columnconfigure(c, weight=1)

    def view_text(self):
        self.readerWindow.columnconfigure(0, weight=1)
        self.readerWindow.rowconfigure(0, weight=1)

        text = tk.Text(self.readerWindow)
        text.grid(column=0, row=0, sticky=tk.NSEW)
        text.insert(tk.END, self.data)
        text.configure(state=tk.DISABLED)
