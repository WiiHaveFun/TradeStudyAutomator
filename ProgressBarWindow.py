import tkinter as tk
import tkinter.ttk as ttk


class ProgressBarWindow(tk.Toplevel):
    def __init__(self):
        super().__init__()

        self.geometry("300x50")
        self.title("Trade Study Progress")
        self.protocol('WM_DELETE_WINDOW', self.remove_window)
        self.resizable(False, False)
        self.rowconfigure(0, weight=1)

        self.progressBar = ttk.Progressbar(self, orient="horizontal", mode="determinate", length=280)

        self.create_widgets()

    def create_widgets(self):
        self.progressBar.grid(column=0, row=0, padx=5, pady=5)

    def update(self, value):
        self.progressBar["value"] = value

    def remove_window(self):
        pass
