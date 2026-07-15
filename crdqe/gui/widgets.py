"""
===========================================================
CRDQE Reusable Widgets
-----------------------------------------------------------
Reusable GUI components used throughout CRDQE.
===========================================================
"""

import tkinter as tk
from tkinter import ttk

from crdqe.gui.theme import Theme


# ==========================================================
# Section Frame
# ==========================================================

class SectionFrame(ttk.LabelFrame):

    def __init__(self, parent, title):

        super().__init__(
            parent,
            text=title,
            padding=10
        )

        self.pack_propagate(False)


# ==========================================================
# Label + Entry
# ==========================================================

class LabeledEntry(ttk.Frame):

    def __init__(self, parent, label, width=40):

        super().__init__(parent)

        ttk.Label(
            self,
            text=label,
            style="Header.TLabel"
        ).pack(anchor="w")

        self.variable = tk.StringVar()

        self.entry = ttk.Entry(
            self,
            textvariable=self.variable,
            width=width
        )

        self.entry.pack(
            fill="x",
            pady=(3, 0)
        )

    def get(self):

        return self.variable.get()

    def set(self, value):

        self.variable.set(value)

    def clear(self):

        self.variable.set("")


# ==========================================================
# Label + Combobox
# ==========================================================

class LabeledCombobox(ttk.Frame):

    def __init__(
        self,
        parent,
        label,
        values=None,
        width=35
    ):

        super().__init__(parent)

        ttk.Label(
            self,
            text=label,
            style="Header.TLabel"
        ).pack(anchor="w")

        self.variable = tk.StringVar()

        self.combo = ttk.Combobox(
            self,
            textvariable=self.variable,
            values=values or [],
            width=width,
            state="readonly"
        )

        self.combo.pack(
            fill="x",
            pady=(3, 0)
        )

    def get(self):

        return self.variable.get()

    def set(self, value):

        self.variable.set(value)

    def values(self, values):

        self.combo["values"] = values


# ==========================================================
# Primary Button
# ==========================================================

class PrimaryButton(ttk.Button):

    def __init__(
        self,
        parent,
        text,
        command
    ):

        super().__init__(
            parent,
            text=text,
            command=command,
            style="Primary.TButton"
        )


# ==========================================================
# Secondary Button
# ==========================================================

class SecondaryButton(ttk.Button):

    def __init__(
        self,
        parent,
        text,
        command
    ):

        super().__init__(
            parent,
            text=text,
            command=command,
            style="Secondary.TButton"
        )


# ==========================================================
# Progress Frame
# ==========================================================

class ProgressFrame(ttk.Frame):

    def __init__(self, parent):

        super().__init__(parent)

        self.label = ttk.Label(
            self,
            text="Ready",
            style="Normal.TLabel"
        )

        self.label.pack(
            anchor="w",
            pady=(0, 5)
        )

        self.progress = ttk.Progressbar(
            self,
            mode="determinate"
        )

        self.progress.pack(
            fill="x"
        )

    def start(self):

        self.progress.configure(mode="indeterminate")
        self.progress.start(10)

    def stop(self):

        self.progress.stop()
        self.progress.configure(mode="determinate")

    def set(self, value):

        self.progress["value"] = value

    def status(self, text):

        self.label.config(text=text)


# ==========================================================
# Log Console
# ==========================================================

class LogConsole(ttk.Frame):

    def __init__(self, parent):

        super().__init__(parent)

        scrollbar = ttk.Scrollbar(self)

        scrollbar.pack(
            side="right",
            fill="y"
        )

        self.text = tk.Text(

            self,

            height=12,

            wrap="word",

            font=("Consolas", 10),

            yscrollcommand=scrollbar.set
        )

        self.text.pack(
            fill="both",
            expand=True
        )

        scrollbar.config(
            command=self.text.yview
        )

    def append(self, message):

        self.text.insert(
            "end",
            str(message) + "\n"
        )

        self.text.see("end")

    def clear(self):

        self.text.delete(
            "1.0",
            "end"
        )


# ==========================================================
# Simple Information Card
# ==========================================================

class InfoCard(ttk.Frame):

    def __init__(
        self,
        parent,
        title,
        value="0"
    ):

        super().__init__(
            parent,
            padding=10
        )

        self.title = ttk.Label(
            self,
            text=title,
            style="Header.TLabel"
        )

        self.title.pack()

        self.value = ttk.Label(
            self,
            text=value,
            style="Title.TLabel"
        )

        self.value.pack(
            pady=(5, 0)
        )

    def set(self, value):

        self.value.config(text=str(value))