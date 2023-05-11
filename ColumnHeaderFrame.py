import tkinter as tk
import tkinter.ttk as ttk


class ColumnHeaderFrame(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)

    def update_headers(self, csv_data):
        headers = csv_data[0]

        ttk.Label(self, text="Columns").grid(column=0, columnspan=len(headers), row=0, padx=5)

        for h, header in enumerate(headers):
            label = str(h + 1) + "—" + header
            ttk.Label(self, text=label).grid(column=h, row=1, padx=5)