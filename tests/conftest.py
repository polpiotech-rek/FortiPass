import sys
from pathlib import Path

def pytest_addoption(parser):
    parser.addoption(
        "--password-length", action="store", default=12, type=int, help="Set the password length"
    )

# Dodanie katalogu src do ścieżki Pythona
sys.path.append(str(Path(__file__).resolve().parent.parent / "src"))