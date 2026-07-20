from pathlib import Path
import sys

# Running as a PyInstaller executable
if getattr(sys, "frozen", False):
    BASE_DIR = Path(sys._MEIPASS)
else:
    # Running from source
    BASE_DIR = Path(__file__).resolve().parents[2]

ASSETS_DIR = BASE_DIR / "assets"
CONFIG_DIR = BASE_DIR / "config"
REFERENCE_DIR = BASE_DIR / "reference"