import tkinter as tk
import tkinter.ttk as ttk

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        self.geometry("1000x500")
        self.title("M-FLY Trade Study Automator")
        self.resizable(0, 0)

        self.columnconfigure(0, weight=1)

        self.createWidgets()

    def createWidgets(self):
        # Window header
        headerLabel = ttk.Label(self, text="M-FLY Trade Study Automater", font=("Helvetica", 20))
        headerLabel.grid(column=0, row=0, sticky=tk.NW, padx=5, pady=5)

        csv_header = ttk.Label(self, text="Select trade study data")
        csv_header.grid(column=0, row=1, sticky=tk.W, padx=5, pady=5)

        avl_header = ttk.Label(self, text="Select avl file")
        avl_header.grid(column=0, row=3, sticky=tk.W, padx=5, pady=5)


if __name__ == "__main__":
    mainWindow = MainWindow()
    mainWindow.mainloop()