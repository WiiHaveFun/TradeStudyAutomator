import pickle
import tkinter as tk
import tkinter.ttk as ttk
from tkinter.filedialog import asksaveasfilename, asksaveasfile

from FilePickerFrame2 import FilePickerFrame
from LineEditsFrame2 import LineEditsFrame
from TradeStudy import TradeStudy


class NewTradeFrame(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)

        self.csv_header = ttk.Label(self, text="Select trade study data")
        self.csv_picker_frame = FilePickerFrame(self, "CSV files", "*.csv")

        self.avl_header = ttk.Label(self, text="Select avl file")
        self.avl_picker_frame = FilePickerFrame(self, "AVL files", "*.avl")

        self.mass_header = ttk.Label(self, text="Select mass file (optional)")
        self.mass_picker_frame = FilePickerFrame(self, "Mass files", "*.mass")

        self.line_edit_header = ttk.Label(self, text="Line edits")
        self.line_edits_frame = LineEditsFrame(self, self.csv_picker_frame, self.avl_picker_frame)

        self.save_button = ttk.Button(self, text="Save")

        self.create_widgets()

    def create_widgets(self):
        # Place widgets in frame
        self.csv_header.grid(column=0, row=0, sticky=tk.W, padx=5, pady=5)
        self.csv_picker_frame.grid(column=0, row=1, sticky=tk.W, padx=5, pady=5)

        self.avl_header.grid(column=0, row=2, sticky=tk.W, padx=5, pady=5)
        self.avl_picker_frame.grid(column=0, row=3, sticky=tk.W, padx=5, pady=5)

        self.mass_header.grid(column=0, row=4, sticky=tk.W, padx=5, pady=5)
        self.mass_picker_frame.grid(column=0, row=5, sticky=tk.W, padx=5, pady=5)

        self.line_edit_header.grid(column=0, row=6, sticky=tk.W, padx=5, pady=5)
        self.line_edits_frame.grid(column=0, row=7, sticky=tk.W, padx=5, pady=5)

        self.save_button['command'] = self.save_ts
        self.save_button.grid(column=0, row=8, sticky=tk.W, padx=5, pady=5)

        # Place frame in window
        self.grid(column=0, row=0, sticky=tk.W)

    def save_ts(self):
        if self.csv_picker_frame.is_file_picked() and self.avl_picker_frame.is_file_picked() and self.line_edits_frame.get_line_edits():
            # file type
            file_types = {
                ("Trade Study files", ".trade"),
            }

            # open file dialog
            f = asksaveasfile(mode="wb", filetypes=file_types)

            if f:
                ts = TradeStudy(self.csv_picker_frame.get_data(), self.avl_picker_frame.get_data(),
                                self.mass_picker_frame.get_data(), self.line_edits_frame.get_line_edits())
                pickle.dump(ts, f)
                f.close()
                self.event_generate("<<Saved>>", data=f.name)
    #
    # def get_save_filename(self):
    #     return self.f.name
