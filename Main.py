import tkinter as tk
import tkinter.ttk as ttk
import numpy as np
from MainWindow import MainWindow
from FilePickerFrame import FilePickerFrame
from ColumnHeaderFrame import ColumnHeaderFrame
from LineEditsFrame import LineEditsFrame
from FolderPickerFrame import FolderPickerFrame
import os
import subprocess
import time
import datetime

from WordPickerFrame import WordPickerFrame

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

    if not tradeStudyStarted and avlPickerFrame.is_file_picked() and csvPickerFrame.is_file_picked():
        tradeStudyStarted = True

        if os.path.isfile("data.txt"):
            os.remove("data.txt")

        lines = avlPickerFrame.get_data().split("\n")
        csvData = csvPickerFrame.get_csv_data()
        csvData.pop(0)
        edits = lineEditsFrame.get_line_edits()

        dateString = datetime.datetime.now().strftime("%Y-%m-%d %H.%M.%S")
        os.mkdir(dateString)

        instructionsFile = open("avl_commands.txt", "r")
        instructions = instructionsFile.readlines()
        instructionsFile.close()

        instructionsFile = open("avl_commands.txt", "w")
        instructions[0] = "load " + avlPickerFrame.f.name + "\n"
        instructionsFile.writelines(instructions)
        instructionsFile.close()

        for i in range(len(csvData)):
            for edit in edits:
                line = lines[int(edit.line) - 1].split()
                line[int(edit.word) - 1] = str(csvData[i][int(edit.column.split("—")[0]) - 1])
                line = " ".join(line)
                lines[int(edit.line) - 1] = line

            avlData = "\n".join(lines)

            avlFile = open(avlPickerFrame.f.name, "w")
            avlFile.write(avlData)
            avlFile.close()

            print("running!")
            try:
                proc = subprocess.Popen("./run_avl_commands.sh") # For Mac
            except:
                proc = subprocess.Popen("run_avl_commands_2.bat") # For Windows

            while not os.path.isfile("data.txt"):
                pass
            # time.sleep(1)

            proc.kill()

            new_data_file_name = dateString + "/data" + str(i + 1) + ".txt"
            os.rename("data.txt", new_data_file_name)

        tradeStudyStarted = False

        tk.messagebox.showinfo(message="Finished")


startButton = ttk.Button(mainWindow, text="Start", command=start_trade_study)
startButton.grid(row=8, column=0, sticky=tk.W, padx=5, pady=5)

tradeDataPickerFrame = FolderPickerFrame(mainWindow)
tradeDataPickerFrame.grid(row=2, column=1, sticky=tk.W)

wordPickerFrame = WordPickerFrame(mainWindow, tradeDataPickerFrame)
wordPickerFrame.grid(row=5, column=1, sticky=tk.W)

def save_to_csv():
    if tradeDataPickerFrame.is_folder_picked():
        directory = tradeDataPickerFrame.get_directory()
        pickedData = wordPickerFrame.get_picked_data()

        dataArray = np.array([])

        isFinished = False
        count = 1
        while not isFinished:
            try:
                f = open(directory + "/data" + str(count) + ".txt")
                text = f.readlines()
                f.close()
            except FileNotFoundError:
                isFinished = True
            else:
                if count == 1:
                    for p in pickedData:
                        line = text[int(p.line) - 1]
                        header = line.split()[int(p.word) - 1]
                        dataArray = np.append(dataArray, header)

                dataRow = np.array([])
                for p in pickedData:
                    line = text[int(p.line) - 1]
                    data = float(line.split()[int(p.word) + 1])
                    dataRow = np.append(dataRow, data)

                dataArray = np.vstack((dataArray, dataRow))
                count += 1

        np.savetxt(directory + '/output.csv', dataArray, delimiter=',', fmt='%s')

        tk.messagebox.showinfo(message="Finished")


saveButton = ttk.Button(mainWindow, text="Save to CSV", command=save_to_csv)
saveButton.grid(row=6, column=1, sticky=tk.W, padx=5, pady=5)

mainWindow.mainloop()