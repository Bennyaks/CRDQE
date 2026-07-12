from crdqe.core.engine import CRDQEEngine
from PySide6.QtGui import QIcon

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QLineEdit,
    QTextEdit,
    QProgressBar,
    QFileDialog,
    QStatusBar,
)


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle(
            "Civil Registration Data Quality Engine (CRDQE)"
        )
        self.setWindowIcon(QIcon("assets/logo.ico"))
        self.resize(1000, 700)

        self.build_ui()

    def build_ui(self):

        central = QWidget()
        layout = QVBoxLayout()

        # --------------------------------------------------
        # Title
        # --------------------------------------------------

        title = QLabel("Civil Registration Data Quality Engine")

        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        title.setStyleSheet(
            "font-size:22px;"
            "font-weight:bold;"
            "padding:10px;"
        )

        layout.addWidget(title)

        # --------------------------------------------------
        # File Selection
        # --------------------------------------------------

        file_layout = QHBoxLayout()

        self.file_path = QLineEdit()
        self.file_path.setPlaceholderText("Select an Excel workbook...")

        browse_button = QPushButton("Browse")
        browse_button.clicked.connect(self.select_file)

        file_layout.addWidget(self.file_path)
        file_layout.addWidget(browse_button)

        layout.addLayout(file_layout)

        # --------------------------------------------------
        # Run Button
        # --------------------------------------------------

        self.run_button = QPushButton("Run Validation")
        self.run_button.setEnabled(False)
        self.run_button.clicked.connect(self.run_validation)

        layout.addWidget(self.run_button)

        # --------------------------------------------------
        # Progress Bar
        # --------------------------------------------------

        self.progress = QProgressBar()
        self.progress.setValue(0)

        layout.addWidget(self.progress)

        # --------------------------------------------------
        # Log Window
        # --------------------------------------------------

        self.log = QTextEdit()
        self.log.setReadOnly(True)

        layout.addWidget(self.log)

        # --------------------------------------------------
        # Finalize Layout
        # --------------------------------------------------

        central.setLayout(layout)

        self.setCentralWidget(central)

        self.setStatusBar(QStatusBar())
        self.statusBar().showMessage("Ready")

    # ======================================================
    # Browse Workbook
    # ======================================================

    def select_file(self):

        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Select Workbook",
            "",
            "Excel Files (*.xlsx *.xls)"
        )

        if not filename:
            return

        self.file_path.setText(filename)

        self.log.append(f"Selected workbook:\n{filename}\n")

        self.run_button.setEnabled(True)

    # ======================================================
    # Run Validation
    # ======================================================

    def run_validation(self):

        self.run_button.setEnabled(False)

        self.progress.setValue(0)

        self.log.clear()

        self.statusBar().showMessage("Running validation...")

        engine = CRDQEEngine()

        engine.run(
            self.file_path.text(),
            callback=self.log.append
        )

        self.progress.setValue(100)

        self.log.append("")
        self.log.append("✔ Validation completed successfully.")

        self.statusBar().showMessage("Finished")

        self.run_button.setEnabled(True)