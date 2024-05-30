import tkinter as tk
import tkinter.ttk as ttk


class CommandsFrame(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)

        self.commands_prefix = ["load AVL_file", "oper"]
        self.commands_suffix = ["x", "", "quit"]

        self.commands_header = ttk.Label(self, text="AVL commands", font=("Helvetica Italic", 12, "bold"))
        self.commands_prefix_label = ttk.Label(self, text=join_commands(self.commands_prefix))
        self.commands_suffix_label = ttk.Label(self, text=join_commands(self.commands_suffix))

        self.commands_body_editor = tk.Text(self, height=10, width=20, highlightthickness=0)

        self.ST_value = tk.IntVar()
        self.FS_value = tk.IntVar()

        self.options_frame = ttk.Frame(self)
        self.ST_button = ttk.Checkbutton(self.options_frame, variable=self.ST_value, onvalue=1, offvalue=0, text="Save Stability Derivatives")
        self.FS_button = ttk.Checkbutton(self.options_frame, variable=self.FS_value, onvalue=1, offvalue=0, text="Save Strip Forces")

        cmd = self.register(self.update_commands)
        container.bind("<<Loaded>>", cmd + " %d")

        self.create_widgets()

    def create_widgets(self):
        self.commands_header.grid(column=0, row=0, sticky=tk.W, padx=5, pady=5)
        self.commands_prefix_label.grid(column=0, row=1, sticky=tk.W, padx=5)
        self.commands_suffix_label.grid(column=0, row=3, sticky=tk.W, padx=5)

        self.commands_body_editor.grid(column=0, row=2, sticky=tk.W)

        self.options_frame.grid(column=1, row=1, rowspan=2)
        self.ST_button.grid(column=0, row=1, sticky=tk.W, padx=5)
        self.FS_button.grid(column=0, row=2, sticky=tk.W, padx=5)

        self.ST_button['command'] = self.update_commands
        self.FS_button['command'] = self.update_commands

    def update_commands(self, is_mass=None):
        if is_mass is not None:
            if int(is_mass):
                self.commands_prefix = ["load AVL_file.avl", "load mass_file.mass", "mset 0", "oper"]
            else:
                self.commands_prefix = ["load AVL_file.avl", "oper"]
            self.commands_prefix_label['text'] = join_commands(self.commands_prefix)

        self.commands_suffix = ["x"]

        if self.ST_value.get():
            self.commands_suffix.append("ST dataX.st")
        if self.FS_value.get():
            self.commands_suffix.append("FS dataX.fs")

        self.commands_suffix.append("")
        self.commands_suffix.append("quit")
        self.commands_suffix_label['text'] = join_commands(self.commands_suffix)

    def get_commands(self):
        commands_body = self.commands_body_editor.get("1.0", "end-1c").split("\n")

        return self.commands_prefix + commands_body + self.commands_suffix


def join_commands(commands):
    return "\n".join(command for command in commands)
