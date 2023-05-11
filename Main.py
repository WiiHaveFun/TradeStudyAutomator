import tkinter as tk
from MainWindow import MainWindow
from FilePickerFrame import FilePickerFrame
from ColumnHeaderFrame import ColumnHeaderFrame
from LineEditsFrame import LineEditsFrame

mainWindow = MainWindow()

columnHeaderFrame = ColumnHeaderFrame(mainWindow)
columnHeaderFrame.grid(row=3, column=0, stick=tk.W, pady=5)

csvPickerFrame = FilePickerFrame(mainWindow, "CSV files", "*.csv", header_displayer=columnHeaderFrame)
csvPickerFrame.grid(row=2, column=0, sticky=tk.W)

avlPickerFrame = FilePickerFrame(mainWindow, "AVL files", "*.avl")
avlPickerFrame.grid(row=5, column=0, sticky=tk.W)

lineEditsFrame = LineEditsFrame(mainWindow, csvPickerFrame, avlPickerFrame)
lineEditsFrame.grid(row=7, column=0, sticky=tk.W)

mainWindow.mainloop()
