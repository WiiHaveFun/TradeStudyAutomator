import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog as fd
import math
import os

from ScrollableFrame import ScrollableFrame


class FilePickerFrame(ttk.Frame):
    def __init__(self, container, file_type_name, file_type):
        super().__init__(container)

        # file data
        self.file_type = file_type
        self.file_type_name = file_type_name
        self.f = None
        self.data = None

        self.viewer_window = None

        # buttons
        self.button_frame = ttk.Frame(self)
        self.read_button = ttk.Button(self.button_frame, text="Choose file")
        self.view_button = ttk.Button(self.button_frame, text="View file")

        # path label
        self.picked_file_label = ttk.Label(self, text="Path:")

        self.create_widgets()

    def create_widgets(self):
        self.read_button['command'] = self.choose_file
        self.view_button['command'] = self.view_file

        self.read_button.grid(column=0, row=0, sticky=tk.W, padx=5, pady=5)
        self.view_button.grid(column=1, row=0, sticky=tk.W, padx=5, pady=5)
        self.button_frame.grid(column=0, row=0, sticky=tk.W)
        self.picked_file_label.grid(column=0, row=1, columnspan=2, sticky=tk.W, padx=5, pady=5)

    def choose_file(self):
        if self.viewer_window is not None:
            self.remove_window()

        # file type
        file_types = {
            (self.file_type_name, self.file_type),
        }

        # show the open file dialog
        f_name = fd.askopenfilename(filetypes=file_types)

        # display file path and read file if a file is picked
        if f_name:
            self.f = open(f_name)
            self.picked_file_label['text'] = "Path: " + os.path.basename(self.f.name)
            self.data = self.f.read()
            self.f.close()

    def view_file(self):
        if self.f is not None:
            if self.viewer_window is None:
                self.viewer_window = tk.Toplevel()
                self.viewer_window.title(self.f.name)
                self.viewer_window.protocol('WM_DELETE_WINDOW', self.remove_window)

                if self.file_type == "*.csv":
                    self.view_csv()
                else:
                    self.view_text()

    def remove_window(self):
        self.viewer_window.destroy()
        self.viewer_window = None

    def view_text(self):
        self.viewer_window.geometry("750x375")

        # Add line numbers
        lines = self.data.split("\n")

        order = math.floor(math.log(len(lines), 10))

        for i in range(len(lines)):
            lines[i] = str(i + 1).rjust(order + 1, " ") + "\t" + lines[i]
        numbered_data = "\n".join(lines)

        self.viewer_window.columnconfigure(0, weight=1)
        self.viewer_window.rowconfigure(0, weight=1)

        text = tk.Text(self.viewer_window)
        text.grid(column=0, row=0, sticky=tk.NSEW)
        text.insert(tk.END, numbered_data)
        text.configure(state=tk.DISABLED)

    def view_csv(self):
        csv_frame = ScrollableFrame(self.viewer_window)
        csv_frame.pack(expand=True)

        data_array = self.get_data()

        for r, row_array in enumerate(data_array):
            if r > 0:
                ttk.Label(csv_frame.scrollable_frame, text=r).grid(column=0, row=r, sticky=tk.W, padx=5)
            for c, entry in enumerate(row_array):
                ttk.Label(csv_frame.scrollable_frame, text=entry).grid(column=c + 1, row=r, padx=20)

    def get_data(self):
        if self.file_type == "*.csv":
            data = [r.split(",") for r in self.data.split("\n")]
        else:
            data = self.data

        return data

    def is_file_picked(self):
        return self.f is not None
