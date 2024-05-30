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

        self.progress_bar = ttk.Progressbar(self, orient="horizontal", mode="determinate", length=280)

        self.stop_button = ttk.Button(self, text="Stop", command=self.request_stop)

        self.create_widgets()

    def create_widgets(self):
        self.progress_bar.grid(column=0, row=0, padx=5, pady=5)
        self.stop_button.grid(column=0, row=1, padx=5, pady=5)

    def update(self, value):
        self.progress_bar["value"] = value

    def remove_window(self):
        pass

    def request_stop(self):
        self.event_generate("<<Stop>>")

