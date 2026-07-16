"""
CRDQE Application Entry Point
"""

from .main_window import MainWindow


def run():
    window = MainWindow()
    window.mainloop()