"""
===========================================================
CRDQE Dialog Manager

Handles all application dialog windows.
===========================================================
"""

from tkinter import messagebox


class Dialogs:

    @staticmethod
    def info(title, message):

        messagebox.showinfo(
            title,
            message
        )

    @staticmethod
    def warning(title, message):

        messagebox.showwarning(
            title,
            message
        )

    @staticmethod
    def error(title, message):

        messagebox.showerror(
            title,
            message
        )

    @staticmethod
    def ask(title, message):

        return messagebox.askyesno(
            title,
            message
        )