import tkinter as tk
import tkinter.ttk as ttk
from tkinter.simpledialog import Dialog
import math


class WordPickerFrame(ttk.Frame):
    def __init__(self, container, folder_picker):
        super().__init__(container)

        # buttons
        self.buttonFrame = ttk.Frame(self)
        self.add_button = ttk.Button(self.buttonFrame, text="Add data to read")
        self.preview_button = ttk.Button(self.buttonFrame, text="Preview picked data")
        self.delete_button = ttk.Button(self.buttonFrame, text="Delete all")

        # line pickedWords
        self.pickerFrame = ttk.Frame(self)
        self.pickedWords = []

        self.folderPicker = folder_picker

        self.folderPicker.readButton.bind("<ButtonRelease-1>", self.delete_line_edits)

        self.previewWindow = None

        self.create_widgets()

    def create_widgets(self):
        self.add_button['command'] = self.add_line_edit
        self.preview_button['command'] = self.preview_line_edits
        self.delete_button['command'] = self.delete_line_edits

        self.add_button.grid(column=0, row=0, sticky=tk.W, padx=5, pady=5)
        self.preview_button.grid(column=1, row=0, sticky=tk.W, padx=5, pady=5)
        self.delete_button.grid(column=2, row=0, sticky=tk.W, padx=5, pady=5)
        self.buttonFrame.grid(column=0, row=0, sticky=tk.W)

        self.pickerFrame.grid(column=0, row=1, sticky=tk.W)

    def add_line_edit(self):
        if self.folderPicker.is_folder_picked():
            line_edit_parameters = LineEditDialog(self.pickerFrame, self.folderPicker.get_data())

            if line_edit_parameters.result is not None:
                line, word = line_edit_parameters.result
                self.pickedWords.append(PickedWord(line, word))

                ttk.Label(self.pickerFrame, text="Line").grid(row=0, column=0, sticky=tk.W, padx=5)
                ttk.Label(self.pickerFrame, text="Word").grid(row=0, column=1, sticky=tk.W, padx=5)

                for e, edit in enumerate(self.pickedWords):
                    ttk.Label(self.pickerFrame, text=edit.line).grid(row=e + 1, column=0, sticky=tk.W, padx=5)
                    ttk.Label(self.pickerFrame, text=edit.word).grid(row=e + 1, column=1, sticky=tk.W, padx=5)

    def preview_line_edits(self):
        if self.previewWindow is None and self.folderPicker.is_folder_picked():
            self.previewWindow = tk.Toplevel()
            self.previewWindow.geometry("750x375")
            self.previewWindow.title("Data picker preview")
            self.previewWindow.protocol('WM_DELETE_WINDOW', self.remove_window)

            # Add line numbers
            lines = self.folderPicker.get_data().split("\n")
            order = math.floor(math.log(len(lines), 10))

            edit_indices = []
            for edit in self.pickedWords:
                start_index = 0
                line = lines[int(edit.line) - 1].split()
                word = line[int(edit.word) - 1]
                print(line)
                for i in range(int(edit.word) - 1):
                    start_index += len(line[i]) + 1

                start_index = lines[int(edit.line) - 1].find(word)

                start_index += order + 2
                end_index = start_index + len(word)
                edit_indices.append([str(edit.line) + "." + str(start_index), str(edit.line) + "." + str(end_index)])

            for i in range(len(lines)):
                lines[i] = str(i + 1).rjust(order + 1, " ") + "\t" + lines[i]
            numbered_data = "\n".join(lines)

            self.previewWindow.columnconfigure(0, weight=1)
            self.previewWindow.rowconfigure(0, weight=1)

            text = tk.Text(self.previewWindow)
            text.grid(column=0, row=0, sticky=tk.NSEW)
            text.insert(tk.END, numbered_data)
            text.configure(state=tk.DISABLED)

            for editIndex in edit_indices:
                text.tag_add("highlight", editIndex[0], editIndex[1])
                text.tag_config("highlight", background="yellow", foreground="black")

    def remove_window(self):
        self.previewWindow.destroy()
        self.previewWindow = None

    def delete_line_edits(self, event=None):
        self.pickedWords = []
        for widget in self.pickerFrame.winfo_children():
            widget.destroy()

    def get_line_edits(self):
        return self.pickedWords


class PickedWord:
    def __init__(self, line, word):
        self.line = line
        self.word = word


class LineEditDialog(Dialog):
    def __init__(self, container, trade_results):
        self.tradeResults = trade_results

        super().__init__(container)

    def body(self, container):
        ttk.Label(container, text="Line").grid(row=0, column=0, sticky=tk.W)
        ttk.Label(container, text="Word").grid(row=1, column=0, sticky=tk.W)

        self.e1 = ttk.Entry(container)
        self.e2 = ttk.Entry(container)

        self.e1.grid(row=0, column=1, sticky=tk.E)
        self.e2.grid(row=1, column=1, sticky=tk.E)

        return self.e1

    def validate(self):
        try:
            line = int(self.e1.get())
        except ValueError:
            tk.messagebox.showwarning(
                message="Line is not an integer" + "\nPlease try again",
                parent=self
            )
            return 0

        lines = self.tradeResults.split("\n")
        n_lines = len(self.tradeResults.split("\n"))

        if line < 1 or line > n_lines:
            tk.messagebox.showwarning(
                message="Line is out of bounds" + "\nPlease try again",
                parent=self
            )
            return 0

        try:
            word = int(self.e2.get())
        except ValueError:
            tk.messagebox.showwarning(
                message="Word is not an integer" + "\nPlease try again",
                parent=self
            )
            return 0

        if word < 1:
            tk.messagebox.showwarning(
                message="Word is not a valid index" + "\nPlease try again",
                parent=self
            )
            return 0

        try:
            word_value = lines[line - 1].split()[word - 1]
        except IndexError:
            tk.messagebox.showwarning(
                message="Word is not a valid index" + "\nPlease try again",
                parent=self
            )
            return 0

        return 1

    def apply(self):
        line = self.e1.get()
        word = self.e2.get()
        self.result = (line, word)


