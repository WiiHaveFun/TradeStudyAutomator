import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog as fd
import pickle


class SaveLoadFrame(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)

        # file parameters and trade study data
        self.f = None
        self.ts = None

        # buttons
        self.button_frame = ttk.Frame(self)
        self.new_ts_button = ttk.Button(self.button_frame, text="New Trade Study")
        self.load_ts_button = ttk.Button(self.button_frame, text="Load Trade Study")

        # selected file label
        self.loaded_file_label = ttk.Label(self, text="Trade Study: ")

        self.create_widgets()

    def create_widgets(self):
        self.new_ts_button['command'] = self.new_ts
        self.load_ts_button['command'] = self.load_ts

        self.new_ts_button.grid(column=0, row=0, sticky=tk.W, padx=5, pady=5)
        self.load_ts_button.grid(column=1, row=0, sticky=tk.W, padx=5, pady=5)
        self.button_frame.grid(column=0, row=0, sticky=tk.W, padx=5, pady=5)
        self.loaded_file_label.grid(column=0, row=1, sticky=tk.W, padx=5, pady=5)

    def new_ts(self):
        return

    def load_ts(self):
        # file type
        file_types = {
            ("Trade Study files", ".trade"),
        }

        # open file dialog
        f_name = fd.askopenfilename(filetypes=file_types)

        # read file if a file is picked and display the name
        if f_name:
            self.f = open(f_name, "rb")
            self.ts = pickle.load(self.f)
            self.f.close()

            print(self.ts)

            self.loaded_file_label['text'] = "Path: " + self.f.name

    def get_ts(self):
        return self.ts

    def is_ts_picked(self):
        return self.ts is not None
