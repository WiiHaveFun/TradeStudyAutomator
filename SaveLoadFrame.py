import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog as fd
import pickle
import os

from FilePickerFrame import FilePickerFrame
from NewTradeFrame import NewTradeFrame


class SaveLoadFrame(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)

        # file parameters and trade study data
        self.f = None
        self.ts = None

        # window for new trade study
        self.new_ts_window = None

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
        if self.new_ts_window is None:
            self.new_ts_window = tk.Toplevel()
            # self.new_ts_window.geometry("1000x500")
            self.new_ts_window.title("New Trade Study")
            self.new_ts_window.protocol('WM_DELETE_WINDOW', self.remove_window)

            cmd = self.register(self.remove_window)
            self.new_ts_window.bind("<<Saved>>", cmd + " %d")

            self.new_trade_frame = NewTradeFrame(self.new_ts_window)

    def remove_window(self, f_name=None):
        if f_name is not None:
            self.load_ts(f_name)
        self.new_ts_window.destroy()
        self.new_ts_window = None

    def load_ts(self, f_name=None):
        if not f_name:
            # file type
            file_types = {
                ("Trade Study files", ".trade"),
            }

            # open file dialog
            f_name = fd.askopenfilename(filetypes=file_types)

        # read file if a file is picked and display the file basename
        if f_name:
            self.f = open(f_name, "rb")
            self.ts = pickle.load(self.f)
            self.f.close()
            self.loaded_file_label['text'] = "Name: " + os.path.basename(self.f.name)

            if self.ts.mass:
                self.event_generate("<<Loaded>>", data="1")
            else:
                self.event_generate("<<Loaded>>", data="0")

    def get_ts(self):
        return self.ts

    def is_ts_picked(self):
        return self.ts is not None
