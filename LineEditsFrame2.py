import tkinter as tk
import tkinter.ttk as ttk
from tkinter.simpledialog import Dialog
from tkinter.filedialog import asksaveasfilename
import math
import numpy as np

from ScrollFrame import ScrollFrame


class LineEditsFrame(ttk.Frame):
    def __init__(self, container, csv_picker, avl_picker):
        super().__init__(container)

        # buttons
        self.button_frame_top = ttk.Frame(self)
        self.add_button = ttk.Button(self.button_frame_top, text="Add line edit")
        self.preview_button = ttk.Button(self.button_frame_top, text="Preview edits")
        self.delete_all_button = ttk.Button(self.button_frame_top, text="Delete all")

        self.button_frame_bottom = ttk.Frame(self)
        self.import_button = ttk.Button(self.button_frame_bottom, text="Import line edits")
        self.export_button = ttk.Button(self.button_frame_bottom, text="Export line edits")

        # line edits
        self.edits_frame = ScrollFrame(self)
        self.edits = []
        self.edit_ids = []

        self.csv_picker = csv_picker
        self.avl_picker = avl_picker

        self.csv_picker.read_button.bind("<ButtonRelease-1>", self.delete_line_edits)
        self.avl_picker.read_button.bind("<ButtonRelease-1>", self.delete_line_edits)

        self.preview_window = None

        self.create_widgets()

    def create_widgets(self):
        self.add_button['command'] = self.add_line_edit
        self.preview_button['command'] = self.preview_line_edits
        self.delete_all_button['command'] = self.delete_line_edits
        self.export_button['command'] = self.export_line_edits

        self.add_button.grid(column=0, row=0, sticky=tk.W, padx=5, pady=5)
        self.preview_button.grid(column=1, row=0, sticky=tk.W, padx=5, pady=5)
        self.delete_all_button.grid(column=2, row=0, sticky=tk.W, padx=5, pady=5)
        self.button_frame_top.grid(column=0, row=0, sticky=tk.W)

        self.import_button.grid(column=0, row=0, sticky=tk.W, padx=5, pady=5)
        self.export_button.grid(column=1, row=0, sticky=tk.W, padx=5, pady=5)
        self.button_frame_bottom.grid(column=0, row=1, sticky=tk.W)

        self.edits_frame.canvas.configure(highlightthickness=0)
        self.edits_frame.viewPort.configure(borderwidth=0)
        self.edits_frame.grid(column=0, row=2, sticky=tk.W, pady=5)

    def add_line_edit(self):
        if self.csv_picker.is_file_picked() and self.avl_picker.is_file_picked():
            headers = self.csv_picker.get_data()[0]
            headers = [str(h + 1) + "—" + header for h, header in enumerate(headers)]

            line_edit_parameters = LineEditDialog(self.edits_frame.viewPort, headers, self.avl_picker.get_data())

            if line_edit_parameters.result is not None:

                line, word, column = line_edit_parameters.result
                self.edits.append(LineEdit(line, word, column))
                if not self.edit_ids:
                    self.edit_ids.append(0)
                else:
                    self.edit_ids.append(self.edit_ids[-1] + 1)

                for widget in self.edits_frame.viewPort.winfo_children():
                    widget.destroy()

                ttk.Label(self.edits_frame.viewPort, text="Line").grid(row=0, column=0, sticky=tk.W, padx=5)
                ttk.Label(self.edits_frame.viewPort, text="Word").grid(row=0, column=1, sticky=tk.W, padx=5)
                ttk.Label(self.edits_frame.viewPort, text="Data Column").grid(row=0, column=2, sticky=tk.W, padx=5)

                for e, edit in enumerate(self.edits):
                    ttk.Label(self.edits_frame.viewPort, text=edit.line).grid(row=e + 1, column=0, sticky=tk.W, padx=5)
                    ttk.Label(self.edits_frame.viewPort, text=edit.word).grid(row=e + 1, column=1, sticky=tk.W, padx=5)
                    ttk.Label(self.edits_frame.viewPort, text=edit.column).grid(row=e + 1, column=2, sticky=tk.W, padx=5)

                    ttk.Button(self.edits_frame.viewPort, text="Delete", command=lambda id=self.edit_ids[e]: self.delete_line_edit(id)).grid(row=e + 1, column=3, sticky=tk.W, padx=5)

    # def display_line_edits(selfs):

    def preview_line_edits(self):
        if self.preview_window is None and self.avl_picker.is_file_picked():
            self.preview_window = tk.Toplevel()
            self.preview_window.geometry("750x375")
            self.preview_window.title("Line edits preview")
            self.preview_window.protocol('WM_DELETE_WINDOW', self.remove_window)

            # Add line numbers
            lines = self.avl_picker.get_data().split("\n")
            order = math.floor(math.log(len(lines), 10))

            # Replace line edits
            for edit in self.edits:
                line = lines[int(edit.line) - 1].split()
                line[int(edit.word) - 1] = edit.column
                line = "\t".join(line)
                lines[int(edit.line) - 1] = line

            edit_indices = []
            for edit in self.edits:
                start_index = 0
                line = lines[int(edit.line) - 1].split()
                for i in range(int(edit.word) - 1):
                    start_index += len(line[i]) + 1

                start_index += order + 2
                end_index = start_index + len(edit.column)
                edit_indices.append([str(edit.line) + "." + str(start_index), str(edit.line) + "." + str(end_index)])

            for i in range(len(lines)):
                lines[i] = str(i + 1).rjust(order + 1, " ") + "\t" + lines[i]
            numbered_data = "\n".join(lines)

            self.preview_window.columnconfigure(0, weight=1)
            self.preview_window.rowconfigure(0, weight=1)

            text = tk.Text(self.preview_window)
            text.grid(column=0, row=0, sticky=tk.NSEW)
            text.insert(tk.END, numbered_data)
            text.configure(state=tk.DISABLED)

            for editIndex in edit_indices:
                text.tag_add("highlight", editIndex[0], editIndex[1])
                text.tag_config("highlight", background="yellow", foreground="black")

    def remove_window(self):
        self.preview_window.destroy()
        self.preview_window = None

    def delete_line_edits(self, event=None):
        self.edits = []
        for widget in self.edits_frame.viewPort.winfo_children():
            widget.destroy()

    def delete_line_edit(self, edit_id):
        edit_idx = self.edit_ids.index(edit_id)
        self.edits.pop(edit_idx)
        self.edit_ids.pop(edit_idx)

        widgets = self.edits_frame.viewPort.winfo_children()

        if not self.edits:
            for widget in self.edits_frame.viewPort.winfo_children():
                widget.destroy()
        else:
            for i in range(4):
                widgets[(edit_idx + 1) * 4 - 1 + i].destroy()

    def export_line_edits(self):
        if self.edits:
            # show the folder select dialog
            f_name = asksaveasfilename(initialfile="Untitled.txt", defaultextension=".txt", filetypes=[("Text File", "*.txt")])
            if f_name:
                print(f_name)

                edit_array = np.zeros((len(self.edits), 3), dtype=np.ushort)

                for e, edit in enumerate(self.edits):
                    edit_array[e, 0] = edit.line
                    edit_array[e, 1] = edit.word
                    edit_array[e, 2] = edit.column

            np.savetxt(f_name, edit_array, delimiter=',', fmt='%s')

    def get_line_edits(self):
        return self.edits


class LineEdit:
    def __init__(self, line, word, column):
        self.line = line
        self.word = word
        self.column = column


class LineEditDialog(Dialog):
    def __init__(self, container, data_columns, avl_data):
        self.data_columns = data_columns
        self.avl_data = avl_data

        super().__init__(container)

    def body(self, container):
        ttk.Label(container, text="Line").grid(row=0, column=0, sticky=tk.W)
        ttk.Label(container, text="Word").grid(row=1, column=0, sticky=tk.W)
        ttk.Label(container, text="Data column").grid(row=2, column=0, sticky=tk.W)

        self.e1 = ttk.Entry(container)
        self.e2 = ttk.Entry(container)
        self.e3 = ttk.Combobox(container)
        self.e3['values'] = self.data_columns
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

        lines = self.avl_data.split("\n")
        n_lines = len(self.avl_data.split("\n"))

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
        data_column = int(self.e3.get().split("—")[0])
        self.result = (line, word, data_column)


