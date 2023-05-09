import tkinter as tk
from MainWindow import MainWindow
from FilePickerFrame import FilePickerFrame

mainWindow = MainWindow()

csvPickerFrame = FilePickerFrame(mainWindow, "CSV files", "*.csv")
csvPickerFrame.grid(row=2, column=0, sticky=tk.W)

avlPickerFrame = FilePickerFrame(mainWindow, "AVL files", "*.avl")
avlPickerFrame.grid(row=4, column=0, sticky=tk.W)

mainWindow.mainloop()
