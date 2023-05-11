import tkinter as tk
import tkinter.ttk as ttk
from tkinter.simpledialog import Dialog


class LineEditsFrame(ttk.Frame):
    def __init__(self, container, csv_picker, avl_picker):
        super().__init__(container)

        # buttons
        self.buttonFrame = ttk.Frame(self)
        self.add_button = ttk.Button(self.buttonFrame, text="Add line edit")
        self.preview_button = ttk.Button(self.buttonFrame, text="Preview edits")
        self.delete_button = ttk.Button(self.buttonFrame, text="Delete all")

        # line edits
        self.editsFrame = ttk.Frame(self)
        self.edits = []

        self.csvPicker = csv_picker
        self.avlPicker = avl_picker

        self.csvPicker.readButton.bind("<ButtonRelease-1>", self.delete_line_edits)
        self.avlPicker.readButton.bind("<ButtonRelease-1>", self.delete_line_edits)

        self.create_widgets()

    def create_widgets(self):
        self.add_button['command'] = self.add_line_edit
        self.preview_button['command'] = self.preview_line_edits
        self.delete_button['command'] = self.delete_line_edits

        self.add_button.grid(column=0, row=0, sticky=tk.W, padx=5, pady=5)
        self.preview_button.grid(column=1, row=0, sticky=tk.W, padx=5, pady=5)
        self.delete_button.grid(column=2, row=0, sticky=tk.W, padx=5, pady=5)
        self.buttonFrame.grid(column=0, row=0, sticky=tk.W)

        self.editsFrame.grid(column=0, row=1, sticky=tk.W)

    def add_line_edit(self):
        if self.csvPicker.is_file_picked() and self.avlPicker.is_file_picked():
            headers = self.csvPicker.get_csv_data()[0]
            headers = [str(h + 1) + ": " + header for h, header in enumerate(headers)]

            line_edit_parameters = LineEditDialog(self.editsFrame, headers, self.avlPicker.get_data())

            if line_edit_parameters.result is not None:
                line, word, column = line_edit_parameters.result
                self.edits.append(LineEdit(line, word, column))

                ttk.Label(self.editsFrame, text="Line").grid(row=0, column=0, sticky=tk.W, padx=5)
                ttk.Label(self.editsFrame, text="Word").grid(row=0, column=1, sticky=tk.W, padx=5)
                ttk.Label(self.editsFrame, text="Data Column").grid(row=0, column=2, sticky=tk.W, padx=5)

                for e, edit in enumerate(self.edits):
                    ttk.Label(self.editsFrame, text=edit.line).grid(row=e + 1, column=0, sticky=tk.W, padx=5)
                    ttk.Label(self.editsFrame, text=edit.word).grid(row=e + 1, column=1, sticky=tk.W, padx=5)
                    ttk.Label(self.editsFrame, text=edit.column).grid(row=e + 1, column=2, sticky=tk.W, padx=5)

    def preview_line_edits(self):
        pass

    def delete_line_edits(self, event=None):
        self.edits = []
        for widget in self.editsFrame.winfo_children():
            widget.destroy()




class LineEdit:
    def __init__(self, line, word, column):
        self.line = line
        self.word = word
        self.column = column


class LineEditDialog(Dialog):
    def __init__(self, container, data_columns, avl_data):
        self.dataColumns = data_columns
        self.avlData = avl_data

        super().__init__(container)

    def body(self, container):
        ttk.Label(container, text="Line").grid(row=0, column=0, sticky=tk.W)
        ttk.Label(container, text="Word").grid(row=1, column=0, sticky=tk.W)
        ttk.Label(container, text="Data column").grid(row=2, column=0, sticky=tk.W)

        self.e1 = ttk.Entry(container)
        self.e2 = ttk.Entry(container)
        self.e3 = ttk.Combobox(container)
        self.e3['values'] = self.dataColumns
        self.e3['state'] = 'readonly'

        self.e1.grid(row=0, column=1, sticky=tk.E)
        self.e2.grid(row=1, column=1, sticky=tk.E)
        self.e3.grid(row=2, column=1, sticky=tk.E)

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

        lines = self.avlData.split("\n")
        n_lines = len(self.avlData.split("\n"))

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

        if not self.e3.get():
            tk.messagebox.showwarning(
                message="Select a data column" + "\nPlease try again",
                parent=self
            )
            return 0

        return 1

    def apply(self):
        line = self.e1.get()
        word = self.e2.get()
        data_column = self.e3.get()
        self.result = (line, word, data_column)


