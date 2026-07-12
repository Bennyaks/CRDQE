import sys
from PySide6.QtWidgets import QApplication, QLabel

app = QApplication(sys.argv)

label = QLabel("Hello CRDQE")
label.resize(300, 100)
label.show()

print("Window should now be visible")

sys.exit(app.exec())