import tkinter as tk
import tkinter.ttk as ttk
from MainWindow import MainWindow
from FilePickerFrame import FilePickerFrame
from ColumnHeaderFrame import ColumnHeaderFrame
from LineEditsFrame import LineEditsFrame
import os
import subprocess
import time
import datetime

mainWindow = MainWindow()

columnHeaderFrame = ColumnHeaderFrame(mainWindow)
columnHeaderFrame.grid(row=3, column=0, stick=tk.W, pady=5)

csvPickerFrame = FilePickerFrame(mainWindow, "CSV files", "*.csv", header_displayer=columnHeaderFrame)
csvPickerFrame.grid(row=2, column=0, sticky=tk.W)

avlPickerFrame = FilePickerFrame(mainWindow, "AVL files", "*.avl")
avlPickerFrame.grid(row=5, column=0, sticky=tk.W)

lineEditsFrame = LineEditsFrame(mainWindow, csvPickerFrame, avlPickerFrame)
lineEditsFrame.grid(row=7, column=0, sticky=tk.W)

tradeStudyStarted = False
def start_trade_study():
    global tradeStudyStarted

    if not tradeStudyStarted:
        tradeStudyStarted = True
        lines = avlPickerFrame.get_data().split("\n")
        csvData = csvPickerFrame.get_csv_data()
        csvData.pop(0)
        edits = lineEditsFrame.get_line_edits()

        dateString = datetime.datetime.now().strftime("%Y-%m-%d %H.%M.%S");
        os.mkdir(dateString);

        instructionsFile = open("sizing.txt", "w")
        instructions = instructionsFile.readlines()
        instructions[0] = "load " + avlPickerFrame.f.name + "\n"
        instructionsFile.writelines(instructions)

        for i in range(len(csvData)):
            for edit in edits:
                line = lines[int(edit.line) - 1].split()
                line[int(edit.word) - 1] = str(csvData[i][int(edit.column.split("—")[0]) - 1])
                line = "\t".join(line)
                lines[int(edit.line) - 1] = line
                avlData = "\n".join(lines)

                avlFile = open(avlPickerFrame.f.name, "w")
                avlFile.write(avlData)
                avlFile.close()

                print("running!")
                proc = subprocess.Popen("./run_sizing.sh")
                time.sleep(5)
                proc.kill()

                new_data_file_name = dateString + "/data" + str(i + 1) + ".txt"
                os.rename("data.txt", new_data_file_name)

        tradeStudyStarted = False

startButton = ttk.Button(mainWindow, text="Start", command=start_trade_study)
startButton.grid(row=8, column=0, sticky=tk.W, padx=5, pady=5)

mainWindow.mainloop()