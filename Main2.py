import tkinter as tk
import tkinter.ttk as ttk
from copy import deepcopy

import math

# import numpy as np
from MainWindow2 import MainWindow
from SaveLoadFrame import SaveLoadFrame
from CommandsFrame import CommandsFrame

import multiprocessing
from FilePickerFrame import FilePickerFrame
from ColumnHeaderFrame import ColumnHeaderFrame
from LineEditsFrame import LineEditsFrame
from FolderPickerFrame import FolderPickerFrame
import os
import stat
import subprocess
import datetime
import time

from ProgressBarWindow import ProgressBarWindow

from WordPickerFrame import WordPickerFrame

trade_started = False
stop_requested = multiprocessing.Value('i')
stop_requested.value = 0


def run_process(ts, n, start_idx, end_idx, folder, st, fs, progress, stop_requested):
    # Apply line edits
    # Execute script
    # Wait for output file(s)
    # Move and rename output files
    # Iterate progress tracker
    # Check for stop variable
    # Kill current process
    # Set progress to stopped

    print("started")
    csv_data = deepcopy(ts.csv)
    csv_data.pop(0)
    lines = ts.avl.split("\n")
    edits = ts.edits

    if os.path.isfile("process" + str(n) + "ST.txt"):
        os.remove("process" + str(n) + "ST.txt")
    if os.path.isfile("process" + str(n) + "FS.txt"):
        os.remove("process" + str(n) + "FS.txt")

    counter = 0
    for i in range(start_idx, end_idx):
        for edit in edits:
            line = lines[int(edit.line) - 1].split()
            line[edit.word - 1] = str(csv_data[i][edit.column - 1])
            line = " ".join(line)
            lines[edit.line - 1] = line

            avl_data = "\n".join(lines)
            avl_f = open("process" + str(n) + ".avl", "w")
            avl_f.write(avl_data)
            avl_f.close()

        try:
            proc = subprocess.Popen("./run_process" + str(n) + ".sh")  # For Mac
        except:
            proc = subprocess.Popen("run_avl_commands.bat")  # For Windows

        if st:
            while not os.path.isfile("process" + str(n) + "ST.txt"):
                if stop_requested.value == 1:
                    break
            if stop_requested.value == 1:
                break
            os.rename("process" + str(n) + "ST.txt", folder + "/ST/ST" + str(i + 1) + ".txt")
            while not os.path.isfile(folder + "/ST/ST" + str(i + 1) + ".txt"):
                pass
        if fs:
            while not os.path.isfile("process" + str(n) + "FS.txt"):
                if stop_requested.value == 1:
                    break
            if stop_requested.value == 1:
                break
            os.rename("process" + str(n) + "FS.txt", folder + "/FS/FS" + str(i + 1) + ".txt")
            while not os.path.isfile(folder + "/FS/FS" + str(i + 1) + ".txt"):
                pass

        # time.sleep(1.0)
        proc.kill()

        counter += 1
        progress[n-1] = counter

        if stop_requested.value == 1:
            break


def prepare_trade(root):
    global trade_started, stop_requested
    # Check that a trade is loaded
    # Check that no trade has been started
    # Create folders (trade, output files, AVL, mass, command)
    # Create AVL files, mass files
    # Create command files
    # Split the trade data
    # Run n processes
    if not trade_started and save_load_frame.is_ts_picked():
        trade_started = True
        stop_requested.value = 0

        ts = save_load_frame.get_ts()
        csv_data = deepcopy(ts.csv)
        csv_data.pop(0)
        avl_data = ts.avl
        if ts.mass is not None:
            mass_data = ts.mass

        date_string = datetime.datetime.now().strftime("%Y-%m-%d %H.%M.%S")
        folder = "TradeStudy" + date_string
        os.mkdir(folder)
        if commands_frame.ST_value.get():
            os.mkdir(folder + "/ST")
        if commands_frame.FS_value.get():
            os.mkdir(folder + "/FS")

        n_process = int(process_combobox.get())
        per_process = math.ceil(len(csv_data) / n_process)
        csv_idx = []

        for i in range(n_process):
            print(i + 1)
            avl_f = open("process" + str(i + 1) + ".avl", "w")
            avl_f.write(avl_data)
            avl_f.close()
            if ts.mass is not None:
                mass_f = open("process" + str(i + 1) + ".mass", "w")
                mass_f.write(mass_data)
                mass_f.close()

            commands = commands_frame.get_commands()
            commands[0] = "load process" + str(i + 1) + ".avl"
            if ts.mass is not None:
                commands[1] = "mass process" + str(i + 1) + ".mass"
            if commands_frame.ST_value.get():
                commands[commands.index("ST dataXST.txt")] = "ST process" + str(i + 1) + "ST.txt"
                print("Changing")
            if commands_frame.FS_value.get():
                commands[commands.index("FS dataXFS.txt")] = "FS process" + str(i + 1) + "FS.txt"
            commands = commands + [""]
            commands = "\n".join(commands)

            commands_f = open("commands" + str(i + 1) + ".txt", "w")
            commands_f.write(commands)
            commands_f.close()

            bash_f = open("run_process" + str(i+1) + ".sh", "w")
            bash_f.write("#!/bin/sh\ncat commands" + str(i+1) + ".txt | ./avl")
            bash_f.close()
            st = os.stat("run_process" + str(i+1) + ".sh")
            os.chmod("run_process" + str(i+1) + ".sh", st.st_mode | stat.S_IEXEC)

            batch_f = open("run_process" + str(i+1) + ".bat", "w")
            batch_f.write("@echo off\ntype commands" + str(i+1) + ".txt | avl.exe")
            batch_f.close()

            if i < n_process - 1:
                csv_idx.append([i * per_process, (i + 1) * per_process])
            else:
                csv_idx.append([i * per_process, len(csv_data)])

        processes = []
        progress = multiprocessing.Array("i", n_process)
        for i in range(n_process):
            processes.append(multiprocessing.Process(target=run_process, args=(
            ts, i+1, csv_idx[i][0], csv_idx[i][1], folder, commands_frame.ST_value.get(),
            commands_frame.FS_value.get(), progress, stop_requested)))

        for process in processes:
            process.start()

        pb = ProgressBarWindow()
        cmd = root.register(request_stop)
        pb.bind("<<Stop>>", cmd)
        root.after(100, lambda: check_trade_status(root, processes, progress, len(csv_data), pb))
        root.withdraw()


def check_trade_status(root, processes, progress, length, pb):
    global stop_requested
    # Check progress tracker
    # Update progress bar
    # Check if progress is stopped
    # Kill processes
    pb.update(sum(progress) / length * 100)
    root.update_idletasks()

    if sum(progress) == length or stop_requested.value:
        for process in processes:
            process.join()
        # time.sleep(3.0)
        stop_trade(root, processes, pb)
    else:
        root.after(100, lambda: check_trade_status(root, processes, progress, length, pb))


def request_stop():
    global stop_requested
    stop_requested.value = 1


def stop_trade(root, processes, pb):
    global trade_started

    pb.destroy()

    for i in range(1, len(processes)+1):
        if os.path.isfile("process" + str(i) + "ST.txt"):
            os.remove("process" + str(i) + "ST.txt")
        if os.path.isfile("process" + str(i) + "FS.txt"):
            os.remove("process" + str(i) + "FS.txt")
        if os.path.isfile("run_process" + str(i) + ".sh"):
            os.remove("run_process" + str(i) + ".sh")
        if os.path.isfile("run_process" + str(i) + ".bat"):
            os.remove("run_process" + str(i) + ".bat")
        if os.path.isfile("process" + str(i) + ".avl"):
            os.remove("process" + str(i) + ".avl")
        if os.path.isfile("commands" + str(i) + ".txt"):
            os.remove("commands" + str(i) + ".txt")

    trade_started = False
    root.deiconify()


if __name__ == "__main__":
    main_window = MainWindow()

    save_load_frame = SaveLoadFrame(main_window)
    save_load_frame.grid(column=0, row=1, sticky=tk.W)

    commands_frame = CommandsFrame(main_window)
    commands_frame.grid(column=0, row=2, sticky=tk.W)

    process_header = ttk.Label(main_window, text="Number of processes", font=("Helvetica Italic", 12, "bold"))
    process_header.grid(column=0, row=3, sticky=tk.W, padx=5, pady=5)
    process_combobox = ttk.Combobox(main_window, values=list(range(1, multiprocessing.cpu_count()+1)), state="readonly", width=3)
    process_combobox.current(0)
    process_combobox.grid(column=0, row=4, sticky=tk.W, padx=5)

    start_button = ttk.Button(main_window, text="Start", command=lambda: prepare_trade(main_window))
    start_button.grid(column=0, row=5, sticky=tk.W, padx=5, pady=5)


    # columnHeaderFrame = ColumnHeaderFrame(mainWindow)
    # columnHeaderFrame.grid(row=3, column=0, stick=tk.W, pady=5)
    #
    # csvPickerFrame = FilePickerFrame(mainWindow, "CSV files", "*.csv", header_displayer=columnHeaderFrame)
    # csvPickerFrame.grid(row=2, column=0, sticky=tk.W)
    #
    # avlPickerFrame = FilePickerFrame(mainWindow, "AVL files", "*.avl")
    # avlPickerFrame.grid(row=5, column=0, sticky=tk.W)
    #
    # lineEditsFrame = LineEditsFrame(mainWindow, csvPickerFrame, avlPickerFrame)
    # lineEditsFrame.grid(row=7, column=0, sticky=tk.W)
    #
    # tradeStudyStarted = False
    # def start_trade_study():
    #     global tradeStudyStarted
    #
    #     if not tradeStudyStarted and avlPickerFrame.is_file_picked() and csvPickerFrame.is_file_picked():
    #         tradeStudyStarted = True
    #
    #         pbw = ProgressBarWindow()
    #
    #         if os.path.isfile("data.txt"):
    #             os.remove("data.txt")
    #
    #         lines = avlPickerFrame.get_data().split("\n")
    #         csvData = csvPickerFrame.get_csv_data()
    #         csvData.pop(0)
    #         edits = lineEditsFrame.get_line_edits()
    #
    #         dateString = datetime.datetime.now().strftime("%Y-%m-%d %H.%M.%S")
    #         os.mkdir(dateString)
    #
    #         instructionsFile = open("avl_commands.txt", "r")
    #         instructions = instructionsFile.readlines()
    #         instructionsFile.close()
    #
    #         instructionsFile = open("avl_commands.txt", "w")
    #         instructions[0] = "load " + avlPickerFrame.f.name + "\n"
    #         instructionsFile.writelines(instructions)
    #         instructionsFile.close()
    #
    #         for i in range(len(csvData)):
    #             for edit in edits:
    #                 line = lines[int(edit.line) - 1].split()
    #                 line[int(edit.word) - 1] = str(csvData[i][int(edit.column.split("—")[0]) - 1])
    #                 line = " ".join(line)
    #                 lines[int(edit.line) - 1] = line
    #
    #             avlData = "\n".join(lines)
    #
    #             avlFile = open(avlPickerFrame.f.name, "w")
    #             avlFile.write(avlData)
    #             avlFile.close()
    #
    #             print("running!")
    #             try:
    #                 proc = subprocess.Popen("./run_avl_commands.sh") # For Mac
    #             except:
    #                 proc = subprocess.Popen("run_avl_commands_2.bat") # For Windows
    #
    #             while not os.path.isfile("data.txt"):
    #                 pass
    #
    #             time.sleep(1)
    #
    #             proc.kill()
    #
    #             new_data_file_name = dateString + "/data" + str(i + 1) + ".txt"
    #             os.rename("data.txt", new_data_file_name)
    #
    #             pbw.update((i + 1) / len(csvData) * 100)
    #             mainWindow.update_idletasks()
    #
    #         tradeStudyStarted = False
    #
    #         pbw.destroy()
    #         tk.messagebox.showinfo(message="Finished")
    #
    #
    # startButton = ttk.Button(mainWindow, text="Start", command=start_trade_study)
    # startButton.grid(row=8, column=0, sticky=tk.W, padx=5, pady=5)
    #
    # tradeDataPickerFrame = FolderPickerFrame(mainWindow)
    # tradeDataPickerFrame.grid(row=2, column=1, sticky=tk.W)
    #
    # wordPickerFrame = WordPickerFrame(mainWindow, tradeDataPickerFrame)
    # wordPickerFrame.grid(row=5, column=1, sticky=tk.W)
    #
    # def save_to_csv():
    #     if tradeDataPickerFrame.is_folder_picked():
    #         directory = tradeDataPickerFrame.get_directory()
    #         pickedData = wordPickerFrame.get_picked_data()
    #
    #         dataArray = np.array([])
    #
    #         isFinished = False
    #         count = 1
    #         while not isFinished:
    #             try:
    #                 f = open(directory + "/data" + str(count) + ".txt")
    #                 text = f.readlines()
    #                 f.close()
    #             except FileNotFoundError:
    #                 isFinished = True
    #             else:
    #                 if count == 1:
    #                     for p in pickedData:
    #                         line = text[int(p.line) - 1]
    #                         header = line.split()[int(p.word) - 1]
    #                         dataArray = np.append(dataArray, header)
    #
    #                 dataRow = np.array([])
    #                 for p in pickedData:
    #                     line = text[int(p.line) - 1]
    #                     data = float(line.split()[int(p.word) + 1])
    #                     dataRow = np.append(dataRow, data)
    #
    #                 dataArray = np.vstack((dataArray, dataRow))
    #                 count += 1
    #
    #         np.savetxt(directory + '/output.csv', dataArray, delimiter=',', fmt='%s')
    #
    #         tk.messagebox.showinfo(message="Finished")
    #
    #
    # saveButton = ttk.Button(mainWindow, text="Save to CSV", command=save_to_csv)
    # saveButton.grid(row=6, column=1, sticky=tk.W, padx=5, pady=5)

    main_window.mainloop()
