import tkinter as tk
import tkinter.ttk as ttk


class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        self.geometry("1000x500")
        self.title("M-FLY Trade Study Automator")
        self.resizable(False, False)

        # self.columnconfigure(0, weight=1)
        # self.columnconfigure(1, weight=1)

        self.create_widgets()

    def create_widgets(self):
        # Window header
        header_label = ttk.Label(self, text="M-FLY Trade Study Automator", font=("Helvetica", 20))
        header_label.grid(column=0, row=0, sticky=tk.NW, padx=5, pady=5)

        csv_header = ttk.Label(self, text="Select trade study data")
        csv_header.grid(column=0, row=1, sticky=tk.W, padx=5, pady=5)

        avl_header = ttk.Label(self, text="Select avl file")
        avl_header.grid(column=0, row=4, sticky=tk.W, padx=5, pady=5)

        line_edit_header = ttk.Label(self, text="Line edits")
        line_edit_header.grid(column=0, row=6, sticky=tk.W, padx=5, pady=5)

        read_csv_header = ttk.Label(self, text="Select trade study results")
        read_csv_header.grid(column=1, row=1, sticky=tk.W, padx=5, pady=5)

        word_picker_header = ttk.Label(self, text="Data picker")
        word_picker_header.grid(column=1, row=4, sticky=tk.W, padx=5, pady=5)


if __name__ == "__main__":
    mainWindow = MainWindow()
    mainWindow.mainloop()
