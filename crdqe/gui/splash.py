"""
===========================================================
CRDQE Splash Screen
===========================================================
"""

import tkinter as tk
from PIL import Image, ImageTk


class SplashScreen(tk.Toplevel):

    def __init__(self, parent):

        super().__init__(parent)

        self.overrideredirect(True)

        self.configure(bg="white")

        width = 700
        height = 420

        background = Image.open("assets/background.png")
        background = background.resize((width, height), Image.LANCZOS)

        self.background = ImageTk.PhotoImage(background)

        # -------------------------
        # Background
        # -------------------------

        background = Image.open("assets/background.png")

        background = background.resize(
            (700, 420),
            Image.LANCZOS
        )

        self.background = ImageTk.PhotoImage(background)

        bg = tk.Label(
            self,
            image=self.background,
            borderwidth=0
        )

        bg.place(
            x=0,
            y=0,
            relwidth=1,
            relheight=1
        )
        # -------------------------
        # Logo
        # -------------------------

        self.logo = tk.PhotoImage(
            file="assets/logo.png"
        )

        logo = tk.Label(
            self,
            image=self.logo,
            bg="white"
        )

        logo.pack(
            pady=(40, 10)
        )

        # -------------------------
        # Title
        # -------------------------

        tk.Label(

            self,

            text="Civil Registration Data Quality Engine",

            font=("Segoe UI", 22, "bold"),

            bg="white",

            fg="#003366"

        ).pack()

        # -------------------------

        tk.Label(

            self,

            text="Version 1.0.0",

            font=("Segoe UI", 11),

            bg="white",

            fg="gray40"

        ).pack(
            pady=(5, 15)
        )

        # -------------------------

        self.message = tk.Label(

            self,

            text="Loading validation engine...",

            font=("Segoe UI", 10),

            bg="white",

            fg="#00796B"

        )

        self.message.pack()

        # -------------------------

        self.after(
            2500,
            self.close
        )

    def close(self):

        self.destroy()