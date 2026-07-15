"""
===========================================================
CRDQE Theme

Central styling for the application.
===========================================================
"""

from tkinter import ttk


class Theme:

    # --------------------------------------------------
    # Colors
    # --------------------------------------------------

    PRIMARY = "#1E3A8A"        # Deep Blue

    SECONDARY = "#2563EB"      # Blue

    SUCCESS = "#16A34A"

    WARNING = "#D97706"

    DANGER = "#DC2626"

    LIGHT = "#F8FAFC"

    BACKGROUND = "#FFFFFF"

    BORDER = "#D1D5DB"

    TEXT = "#111827"

    MUTED = "#6B7280"

    # --------------------------------------------------
    # Fonts
    # --------------------------------------------------

    TITLE_FONT = (
        "Segoe UI",
        18,
        "bold"
    )

    HEADER_FONT = (
        "Segoe UI",
        11,
        "bold"
    )

    NORMAL_FONT = (
        "Segoe UI",
        10
    )

    SMALL_FONT = (
        "Segoe UI",
        9
    )

    BUTTON_FONT = (
        "Segoe UI",
        10,
        "bold"
    )

    # --------------------------------------------------
    # Padding
    # --------------------------------------------------

    PAD_SMALL = 5

    PAD = 10

    PAD_LARGE = 15

    PAD_XL = 20

    # --------------------------------------------------
    # Configure ttk Styles
    # --------------------------------------------------

    @classmethod
    def configure(cls):

        style = ttk.Style()

        style.theme_use("clam")

        # ------------------------
        # Window
        # ------------------------

        style.configure(

            ".",

            background=cls.BACKGROUND,

            foreground=cls.TEXT,

            font=cls.NORMAL_FONT

        )

        # ------------------------
        # Labels
        # ------------------------

        style.configure(

            "Title.TLabel",

            font=cls.TITLE_FONT,

            foreground=cls.PRIMARY,

            background=cls.BACKGROUND

        )

        style.configure(

            "Header.TLabel",

            font=cls.HEADER_FONT,

            background=cls.BACKGROUND

        )

        style.configure(

            "Normal.TLabel",

            font=cls.NORMAL_FONT,

            background=cls.BACKGROUND

        )

        # ------------------------
        # Buttons
        # ------------------------

        style.configure(

            "Primary.TButton",

            font=cls.BUTTON_FONT,

            padding=8

        )

        style.configure(

            "Secondary.TButton",

            font=cls.BUTTON_FONT,

            padding=6

        )

        # ------------------------
        # Entry
        # ------------------------

        style.configure(

            "TEntry",

            padding=5

        )

        # ------------------------
        # Combobox
        # ------------------------

        style.configure(

            "TCombobox",

            padding=4

        )

        # ------------------------
        # Treeview
        # ------------------------

        style.configure(

            "Treeview",

            rowheight=28,

            font=cls.NORMAL_FONT

        )

        style.configure(

            "Treeview.Heading",

            font=cls.HEADER_FONT

        )

        # ------------------------
        # Progress Bar
        # ------------------------

        style.configure(

            "TProgressbar",

            thickness=18

        )

        return style