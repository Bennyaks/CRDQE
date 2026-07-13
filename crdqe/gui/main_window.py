import os
import traceback
from pathlib import Path
from PySide6.QtWidgets import QComboBox
from openpyxl import load_workbook

from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QFileDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QProgressBar,
    QTextEdit,
    QStatusBar,
    QVBoxLayout,
    QWidget,
)

from crdqe.core.engine import CRDQEEngine


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.engine = None

        self.setWindowTitle(
            "Civil Registration Data Quality Engine (CRDQE)"
        )

        self.setWindowIcon(
            QIcon("assets/logo.ico")
        )

        self.resize(1100, 760)

        self.build_ui()
        self.apply_styles()

    # =====================================================
    # BUILD USER INTERFACE
    # =====================================================

    def build_ui(self):

        central = QWidget()

        self.setCentralWidget(central)

        self.main_layout = QVBoxLayout()

        self.main_layout.setContentsMargins(
            20,
            20,
            20,
            20
        )

        self.main_layout.setSpacing(15)

        central.setLayout(self.main_layout)

        # -------------------------------------------------
        # TITLE
        # -------------------------------------------------

        title = QLabel(
            "Civil Registration Data Quality Engine"
        )

        title.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        title.setStyleSheet("""
            QLabel{
                font-size:28px;
                font-weight:bold;
                color:#1F4E78;
                padding:10px;
            }
        """)

        subtitle = QLabel(
            "Automated Civil Registration Data Validation System"
        )

        subtitle.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        subtitle.setStyleSheet("""
            QLabel{
                color:gray;
                font-size:13px;
            }
        """)

        self.main_layout.addWidget(title)
        self.main_layout.addWidget(subtitle)

        # -------------------------------------------------
        # FILE SELECTION
        # -------------------------------------------------

        file_frame = QFrame()

        file_frame.setFrameShape(QFrame.Shape.StyledPanel)

        file_layout = QHBoxLayout(file_frame)

        self.file_path = QLineEdit()

        self.file_path.setPlaceholderText(
            "Browse for an Excel workbook..."
        )

        self.file_path.setReadOnly(True)

        self.file_path.setMinimumHeight(38)

        browse_button = QPushButton("Browse")

        browse_button.setMinimumHeight(38)

        browse_button.clicked.connect(
            self.select_file
        )

        file_layout.addWidget(self.file_path)

        file_layout.addWidget(browse_button)

        self.main_layout.addWidget(file_frame)

        # -------------------------------------------------
        # Worksheet Selection
        # -------------------------------------------------

        worksheet_label = QLabel("Worksheet")

        worksheet_label.setStyleSheet(
            "font-weight:bold;"
        )

        self.main_layout.addWidget(
            worksheet_label
        )

        self.sheet_combo = QComboBox()

        self.sheet_combo.setMinimumHeight(38)

        self.sheet_combo.setEnabled(False)

        self.main_layout.addWidget(
            self.sheet_combo
        )

        # -------------------------------------------------
        # BUTTONS
        # -------------------------------------------------

        button_layout = QHBoxLayout()

        self.run_button = QPushButton(
            "Run Validation"
        )

        self.run_button.setMinimumHeight(42)

        self.run_button.setEnabled(False)

        self.run_button.clicked.connect(
            self.run_validation
        )

        self.output_button = QPushButton(
            "Open Output Folder"
        )

        self.output_button.setMinimumHeight(42)

        self.output_button.setEnabled(False)

        self.output_button.clicked.connect(
            self.open_output_folder
        )

        button_layout.addWidget(
            self.run_button
        )

        button_layout.addWidget(
            self.output_button
        )

        self.main_layout.addLayout(
            button_layout
        )

        # -------------------------------------------------
        # DASHBOARD
        # -------------------------------------------------

        dashboard = QHBoxLayout()

        self.dataset_label = QLabel("Dataset\n-")

        self.records_label = QLabel("Records\n0")

        self.issues_label = QLabel("Issues\n0")

        for card in (
            self.dataset_label,
            self.records_label,
            self.issues_label,
        ):

            card.setAlignment(
                Qt.AlignmentFlag.AlignCenter
            )

            card.setMinimumHeight(90)

            card.setStyleSheet("""
                QLabel{
                    border:1px solid #C7D3DD;
                    border-radius:8px;
                    background:white;
                    font-size:15px;
                    font-weight:bold;
                    padding:15px;
                }
            """)

            dashboard.addWidget(card)

        self.main_layout.addLayout(
            dashboard
        )

        # -------------------------------------------------
        # PROGRESS BAR
        # -------------------------------------------------

        self.progress = QProgressBar()

        self.progress.setRange(0, 100)
        self.progress.setValue(0)

        self.progress.setMinimumHeight(28)

        self.main_layout.addWidget(
            self.progress
        )

        # -------------------------------------------------
        # LOG WINDOW
        # -------------------------------------------------

        self.log = QTextEdit()

        self.log.setReadOnly(True)

        self.log.setPlaceholderText(
            "Validation logs will appear here..."
        )

        self.main_layout.addWidget(
            self.log
        )

        # -------------------------------------------------
        # STATUS BAR
        # -------------------------------------------------

        self.setStatusBar(
            QStatusBar()
        )

        self.statusBar().showMessage(
            "Ready"
        )
    # =====================================================
    # SELECT WORKBOOK
    # =====================================================

    def select_file(self):

        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Select Excel Workbook",
            "",
            "Excel Workbook (*.xlsx *.xls)"
        )

        if not filename:
            return
        self.selected_file = filename
        workbook = load_workbook(
            filename,
            read_only=True
        )

        self.sheet_combo.clear()

        for sheet in workbook.sheetnames:

            self.sheet_combo.addItem(sheet)

        workbook.close()

        self.sheet_combo.setEnabled(True)

        self.file_path.setText(
            Path(filename).name
        )
        print("Textbox contains:", self.file_path.text())

        
        self.dataset_label.setText("Dataset\n-")
        self.records_label.setText("Records\n0")
        self.issues_label.setText("Issues\n0")

        self.progress.setRange(0, 100)
        self.progress.setValue(0)

        self.run_button.setEnabled(True)

        self.statusBar().showMessage(
                "Workbook selected"
        )

        self.log.clear()

        self.log.append(
            f"Workbook selected:\n{filename}"
        )

    # =====================================================
    # RUN VALIDATION
    # =====================================================

    def run_validation(self):

        workbook = getattr(self, "selected_file", "")

        if not workbook:

            self.log.append("Please select a workbook first.")
            return

        worksheet = self.sheet_combo.currentText()

        self.run_button.setEnabled(False)

        self.output_button.setEnabled(False)

        self.progress.setValue(10)

        self.log.clear()

        self.statusBar().showMessage(
            "Running validation..."
        )

        self.log.append(
            f"Workbook : {Path(workbook).name}"
        )

        self.log.append(
            f"Worksheet : {worksheet}"
        )

        self.log.append("")
        self.log.append("Starting validation...")
        self.log.append("-" * 50)

        try:

            self.engine = CRDQEEngine()

            result = self.engine.run(
                workbook_path=workbook,
                worksheet=worksheet,
                callback=self.log.append
            )

            self.progress.setValue(70)

            self.dataset_label.setText(
                f"Dataset\n{self.engine.dataset}"
            )

            self.records_label.setText(
                f"Records\n{self.engine.records}"
            )

            self.issues_label.setText(
                f"Issues\n{self.engine.issue_count}"
            )

            self.output_button.setEnabled(True)

            self.progress.setValue(100)

            self.statusBar().showMessage(
                "Validation completed successfully."
            )

            self.log.append("")
            self.log.append("=" * 50)
            self.log.append("Validation completed successfully.")
            self.log.append(f"Dataset : {self.engine.dataset}")
            self.log.append(f"Records : {self.engine.records}")
            self.log.append(f"Issues  : {self.engine.issue_count}")
            self.log.append("=" * 50)

        except Exception as e:

            self.progress.setValue(0)
            traceback.print_exc()

            self.log.append("")
            self.log.append("=" * 50)
            self.log.append(f"ERROR: {e}")
            self.log.append("=" * 50)

            self.statusBar().showMessage(
                "Validation failed"
            )

        finally:

            self.run_button.setEnabled(True)

    # =====================================================
    # OPEN OUTPUT FOLDER
    # =====================================================

    def open_output_folder(self):

        output_folder = os.path.abspath(
            os.path.join(
                os.getcwd(),
                "data",
                "output"
            )
        )
        print(output_folder)
        print(os.path.exists(output_folder))
    

        if os.path.exists(output_folder):

            os.startfile(output_folder)

        else:

            self.log.append("Output folder not found.")
        
            
    # =====================================================
    # APPLICATION STYLES
    # =====================================================

    def apply_styles(self):

        self.setStyleSheet("""

        QMainWindow{
            background:#F4F6F9;
        }

        QLabel{
            color:#202020;
            font-size:12px;
        }

        QLabel#titleLabel{
            color:#1F4E78;
            font-size:22px;
            font-weight:bold;
        }

        QLabel#subtitleLabel{
            color:#6B7785;
            font-size:12px;
        }

        QLineEdit{
            border:1px solid #C9D1D9;
            border-radius:6px;
            padding:8px;
            background:white;
            font-size:12px;
            color:#202020;
        }

        QLineEdit:focus{
            border:1px solid #1F4E78;
        }

        QPushButton{
            background:#1F4E78;
            color:white;
            border:none;
            border-radius:6px;
            padding:8px 18px;
            font-size:12px;
            font-weight:bold;
        }

        QPushButton:hover{
            background:#2E6DA4;
        }

        QPushButton:pressed{
            background:#163B5C;
        }

        QPushButton:disabled{
            background:#A8B6C5;
            color:black;
        }

        QTextEdit{
            background:white;
            color:black;
            border:1px solid #C9D1D9;
            border-radius:6px;
            font-family:Consolas;
            font-size:11px;
        }

        QProgressBar{
            border:1px solid #C9D1D9;
            border-radius:6px;
            text-align:center;
            background:white;
            color:#202020;
            height:20px;
        }

        QProgressBar::chunk{
            background:#1F4E78;
            border-radius:5px;
        }

        QStatusBar{
            background:white;
            color:#202020;
            border-top:1px solid #C9D1D9;
        }

        QComboBox{
            border:1px solid #C9D1D9;
            border-radius:6px;
            padding:8px;
            background:#EDF1F5;
            color:#202020;
            font-size:12px;
        }

        QComboBox:hover{
            border:1px solid #1F4E78;
            background:#E3E9EF;
        }

        QComboBox:on{
            border:1px solid #1F4E78;
            background:#E3E9EF;
        }

        QComboBox::drop-down{
            subcontrol-origin: padding;
            subcontrol-position: top right;
            width:28px;
            border-left:1px solid #C9D1D9;
            border-top-right-radius:6px;
            border-bottom-right-radius:6px;
            background:transparent;
        }

        QComboBox::down-arrow{
            image: none;
            width:0px;
            height:0px;
            border-left: 5px solid transparent;
            border-right: 5px solid transparent;
            border-top: 7px solid #1F4E78;
            margin-right: 10px;
        }

        QComboBox::down-arrow:on{
            border-top: 7px solid #163B5C;
        }

        QComboBox QAbstractItemView{
            background:#EDF1F5;
            color:#202020;
            border:1px solid #C9D1D9;
            border-radius:6px;
            selection-background-color:#1F4E78;
            selection-color:white;
            outline:none;
            padding:4px;
        }

        QComboBox QAbstractItemView::item{
            min-height:26px;
            padding:4px 8px;
            border-radius:4px;
        }

        /* --- Other widgets that will otherwise fall back to OS default --- */
        QCheckBox, QRadioButton{
            color:#202020;
            font-size:12px;
            spacing:6px;
        }

        QTabWidget::pane{
            border:1px solid #C9D1D9;
            border-radius:6px;
            background:white;
        }

        QTabBar::tab{
            background:#E7ECF1;
            color:#202020;
            padding:6px 14px;
            border-top-left-radius:6px;
            border-top-right-radius:6px;
        }

        QTabBar::tab:selected{
            background:#1F4E78;
            color:white;
        }

        QScrollBar:vertical{
            background:#F4F6F9;
            width:10px;
            margin:0px;
        }

        QScrollBar::handle:vertical{
            background:#C9D1D9;
            border-radius:5px;
            min-height:20px;
        }

        QScrollBar::handle:vertical:hover{
            background:#A8B6C5;
        }

        """)