# To start commend: pytest tests/ --password-length 16

import pytest
from tkinter import Tk
from unittest.mock import patch, MagicMock
import sys
from pathlib import Path
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent / "src"))
from main import PasswordGeneratorApp



@pytest.fixture
def app():
    """Fixture inicjujący aplikację Tkinter."""
    root = Tk()
    app = PasswordGeneratorApp(root)
    yield app
    root.destroy()


# Fixture, która umożliwia przekazanie parametru z wiersza poleceń
@pytest.fixture
def password_length(request):
    return int(request.config.getoption("--password-length"))

def test_generate_password_length(app, password_length):
    """Test generowania hasła o określonej długości."""
    app.length_entry.delete(0, "end")
    app.length_entry.insert(0, str(password_length))  # Ustaw długość hasła
    app.letters_var.set(True)
    app.numbers_var.set(True)
    app.special_var.set(True)

    app.generate_password()  # Wywołanie funkcji generowania hasła
    generated_password = app.password_entry.get()
    
    assert len(generated_password) == password_length, f"Password length should be {password_length}, but got {len(generated_password)}"
    
def test_generate_password_content(app):
    """Test zawartości wygenerowanego hasła."""
    app.length_entry.insert(0, "16")
    app.letters_var.set(True)
    app.numbers_var.set(True)
    app.special_var.set(True)

    app.generate_password()
    generated_password = app.password_entry.get()

    assert any(c.isdigit() for c in generated_password), "Password should contain digits"
    assert any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in generated_password), "Password should contain special characters"
    assert any(c.isalpha() for c in generated_password), "Password should contain letters"


def test_copy_to_clipboard(app):
    """Test kopiowania hasła do schowka."""
    app.password_entry.insert(0, "TestPassword123!")
    app.copy_to_clipboard()

    # Sprawdź, czy schowek zawiera skopiowane hasło
    clipboard_content = app.root.clipboard_get()
    assert clipboard_content == "TestPassword123!", "Clipboard content should match the password"


def test_password_strength(app):
    """Test siły hasła."""
    app.password_entry.insert(0, "StrongPass123!")
    strength, color = app.evaluate_password_strength(app.password_entry.get())

    assert strength == "strong", "Password strength should be 'strong'"
    assert color == "green", "Color for strong password should be green"

    app.password_entry.delete(0, "end")
    app.password_entry.insert(0, "Weak123")
    strength, color = app.evaluate_password_strength(app.password_entry.get())

    assert strength == "medium", "Password strength should be 'medium'"
    assert color == "orange", "Color for medium password should be orange"

    app.password_entry.delete(0, "end")
    app.password_entry.insert(0, "123")
    strength, color = app.evaluate_password_strength(app.password_entry.get())

    assert strength == "weak", "Password strength should be 'weak'"
    assert color == "red", "Color for weak password should be red"


@patch("src.main.logging")
def test_logging(mock_logging, app):
    """Test logowania działań."""
    app.length_entry.insert(0, "12")
    app.generate_password()

    # Sprawdź, czy funkcje logowania zostały wywołane
    assert mock_logging.info.called, "Logging should log info messages"
    assert mock_logging.debug.called, "Logging should log debug messages"