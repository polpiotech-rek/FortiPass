<div align="center">
    <h1>🔐 Password Generator</h1>
</div>

A desktop application for generating and managing passwords, created using the Tkinter library. It allows you to generate strong passwords, evaluate their strength, copy them to the clipboard, and view system logs.

---

<h3>✨ Features</h3>

- 🔒 **Password Generation**: Create strong passwords based on selected criteria (length, letters, numbers, special characters).
- 🛡️ **Password Strength Evaluation**: See how secure your password is with visual indicators (color: green, orange, red).
- 📋 **Copy to Clipboard**: Convenient one-click password copying.
- 🗒️ **View Logs**: Browse system logs in a dedicated window with scrolling and log entry loading functionality.

---

<h3>⚙️ Requirements</h3>

- 🐍 **Python**: Version 3.x
- 📦 **Tkinter**: Included in the standard Python library
- 🛠️ **Additional Modules**:
  - `logging` (for event logging)
  - `string` (for string operations)

---

<h3>🚀 Installation</h3>

1. Install Python 3.x if it's not already on your device.
2. Download the application files to your computer.
3. Run the application using the following commands:
   - **Windows**: `bash python app.py`
   - **Linux**: `bash python3 app.py`

---

<h3>🖱️ How to Use</h3>

1. 🛠️ **Generate Password**
   Enter parameters such as password length and additional options (e.g., numbers, special characters).
   Click **"Generate Password"** to see the new password and its strength rating.

2. 🔍 **Password Strength Evaluation**
   Password strength is evaluated based on its length and the characters used.
   **Color indicators**:
   - 🟢 **Green** – Strong Password
   - 🟠 **Orange** – Medium Password
   - 🔴 **Red** – Weak Password

3. 📋 **Copy to Clipboard**
   After generating a password, click **"Copy to Clipboard"** to quickly copy it.

4. 🗒️ **View Logs**
   Click **"Show Logs"** to open a window with a list of actions saved in the logs (e.g., password generation, application closure).
   Logs can be scrolled and additional entries loaded.

5. ❌ **Close the Application**
   Click the **"X"** button in the top-right corner.
   A dialog window will appear asking for confirmation. Select **"Yes"** or **"No"**.

---

<h3>📂 Logging</h3>

The application automatically saves all important events, such as:
- Password generation.
- Copying password to clipboard.
- Viewing logs.
- Attempting to close the application.

Logs are saved in a text file and can be accessed via the **"Show Logs"** option.

---

<h3>📄 License</h3>

This project is licensed under <b>the MIT License</b>. See the [<b>LICENSE</b>](LICENSE) file for details.

---

<div align="center">
    Made with ❤️ by **[<b>Piotr Bodych</b>]**
</div>
