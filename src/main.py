# fortipass/main.py
#
# Copyright (c) 2024 Piotr Bodych
# Licensed under the MIT License. See LICENSE file in the project root for details.


import tkinter as tk, threading, logging, secrets, string, sys, random
from tkinter import messagebox, Toplevel, PhotoImage
from pathlib import Path
from lock import AppLocker

class PasswordGeneratorApp:
    def __init__(self, root):
        """Inicjalizacja aplikacji z głównym oknem"""
        self.root = root
        self.root.title("FortiPass®")
        self.root.geometry("375x555")
        self.root.resizable(False, False)

        self.chunk_size = 1000  
        self.current_offset = 0

        try:
            self.setup_logging()
            logging.debug("Starting the program:".upper())

            # Inicjalizacja tłumaczeń
            self.translations = self.setup_translations()

            # Ustawienia języka (domyślny to angielski)
            self.current_language = "EN"

            logging.warning("Initiating the program startup process.")

            # Tworzenie instancji lockera
            self.locker = AppLocker()

            # Próba zablokowania instancji
            self.locker.lock_instance()

            # Inicjalizacja ustawień
            self.setup_ui()
            self.setup_menu()
            self.setup_icon()

            # Obsługa klawisza Enter
            self.root.bind("<Return>", self.handle_enter_key)

            # Logowanie poszczególnych etapów inicjalizacji
            logging.info("User Interface has been launched successfully.")
            logging.info("Shortcut icon settings have been loaded successfully.")
            logging.info("Menu settings have been loaded successfully.")
            logging.info("Workflow monitoring settings have been loaded successfully.")
            logging.info("The default language has been set in the program.")
            
        except Exception as e:
            logging.error(f"Startup Error: {str(e)}!")
            messagebox.showerror("FortiPass® - Error", "An error occurred during the program startup!")
            sys.exit(1)
  
        logging.info("The program was started successfully.")

    def setup_icon(self):
        # Tworzenie katalogu "img" w katalogu nadrzędnym
        try:
            parent_dir = Path(__file__).resolve().parent.parent
            img_dir = parent_dir / "img"
            img_dir.mkdir(exist_ok=True)
            img_file = img_dir / "icon.png"

            # Sprawdzanie, czy ikona istnieje
            if img_file.exists():
                icon = PhotoImage(file=img_file)
                self.root.iconphoto(True, icon)
        except Exception as e:
            logging.error(f"Setting up icon: {str(e)}!")
            messagebox.showerror("FortiPass® - Error", "Failed to load the icon!")

    def setup_logging(self):
        """Ustawienia loggowania"""
        # Tworzenie katalogu logs w katalogu nadrzędnym
        try:
            parent_dir = Path(__file__).resolve().parent.parent
            log_dir = parent_dir / "logs"
            log_dir.mkdir(exist_ok=True)
            log_file = log_dir / "password_generator.log"
            self.log_file = log_file

            # Sprawdzanie, czy plik istnieje
            if not log_file.exists():
                # Tworzenie nowego pliku log (jeśli nie istnieje)
                log_file.touch()

            # Konfiguracja loggowania
            logging.basicConfig(
                filename=log_file,
                level=logging.DEBUG,
                format="%(asctime)s - %(levelname)s - %(message)s"
            )

        except Exception as e:
            logging.error(f"Setting up logging: {str(e)}!")
            messagebox.showerror("FortiPass® - Error", "An error occurred while starting the program related to logging events to the log file!")

    def handle_enter_key(self, event):
        """Przechwytuje naciśnięcie klawisza Enter dla aktywnego przycisku lub pola tekstowego"""
        widget = self.root.focus_get()  # Zwraca widget, który ma fokus
        
        if isinstance(widget, tk.Button):
            widget.invoke()  # Wywołuje funkcję przypisaną do przycisku
        elif isinstance(widget, tk.Entry):
            # Jeśli pole tekstowe jest aktywne, uruchamia generowanie hasła
            self.generate_password()

    def setup_translations(self):
        """Słownik z tłumaczeniami"""
        return {
            "EN": {
                "title": "FortiPass®",
                "language_menu": "Language",
                "password_length": "Password length:",
                "letters": "Letters (a-Z)",
                "digits": "Digits (0-9)",
                "special_chars": "Special characters (!@#)",
                "generated_password": "Generated password:",
                "generate_btn": "Generate Password",
                "copy_btn": "Copy to Clipboard",
                "log_btn": "Show Log",
                "password_strength": "Password strength: ",
                "strong": "Strong",
                "medium": "Medium",
                "weak": "Weak",
                "english": "English",
                "polish": "Polish",
                "password_copied": "Password copied to clipboard!",
                "empty_password": "No generated password to copy.",
                "input_error": "Password length must be greater than zero.",
                "select_option": "You must select at least one option!",
            },
            "PL": {
                "title": "FortiPass®",
                "language_menu": "Język",
                "password_length": "Długość hasła:",
                "letters": "Litery (a-Z)",
                "digits": "Cyfry (0-9)",
                "special_chars": "Znaki specjalne (!@#)",
                "generated_password": "Wygenerowane hasło:",
                "generate_btn": "Generuj Hasło",
                "copy_btn": "Skopiuj do Schowka",
                "log_btn": "Pokaż Log",
                "password_strength": "Siła hasła: ",
                "strong": "Silne",
                "medium": "Średnie",
                "weak": "Słabe",
                "english": "Angielski",
                "polish": "Polski",
                "password_copied": "Hasło skopiowane do schowka!",
                "empty_password": "Brak wygenerowanego hasła do skopiowania.",
                "input_error": "Długość hasła musi być większa od zera.",
                "select_option": "Musisz wybrać co najmniej jedną opcję!",
            },
        }

    def setup_menu(self):
        """Tworzy menu z wyborem języka"""
        self.menu = tk.Menu(self.root)
        self.language_menu = tk.Menu(self.menu, tearoff=0)

        # Dodaj języki do menu wyboru z dynamicznymi tłumaczeniami
        translations = self.translations[self.current_language]
        self.language_menu.add_command(label=translations["english"], command=lambda: self.set_language("EN"))
        self.language_menu.add_command(label=translations["polish"], command=lambda: self.set_language("PL"))

        # Dodaj podmenu z wyborem języka do głównego menu
        self.menu.add_cascade(label=translations["language_menu"], menu=self.language_menu)
        self.root.config(menu=self.menu)
        
    def set_language(self, language):
        """Ustawia język aplikacji"""
        logging.debug(f"Language setting change:".upper())
        try:
            logging.warning("Initializing the language change process.")
            # Przechowywanie poprzedniego języka
            previous_language = self.current_language

            # Aktualizacja języka i interfejsu
            self.current_language = language
            self.update_ui_texts()
            self.password_entry.delete(0, tk.END)
            self.update_password_strength(None)
            self.strength_bar.delete("all")
            self.strength_bar.create_oval(5, 5, 20, 20, fill="white")

            # Dodawanie informacji do logów
            logging.info(f"Change from: {previous_language}")
            logging.info(f"Change to: {language}")
            logging.info("The language setting was changed successfully.")
        except Exception as e:
            logging.error(f"Setting language: {str(e)}!")
            messagebox.showerror("FortiPass® - Error", "An error occurred while changing the language setting!")

    def update_ui_texts(self):
        """Aktualizuje teksty w interfejsie na podstawie wybranego języka"""
        translations = self.translations[self.current_language]
        
        # Aktualizacja tekstów w interfejsie
        self.root.title(translations["title"])
        self.password_length_label.config(text=translations["password_length"])
        self.letters_checkbutton.config(text=translations["letters"])
        self.digits_checkbutton.config(text=translations["digits"])
        self.special_checkbutton.config(text=translations["special_chars"])
        self.generated_password_label.config(text=translations["generated_password"])
        self.generate_button.config(text=translations["generate_btn"])
        self.copy_button.config(text=translations["copy_btn"])
        self.log_button.config(text=translations["log_btn"])
        
        # Przebudowanie menu dla dynamicznej aktualizacji tekstu
        self.setup_menu()

    def setup_ui(self):
        """Tworzenie elementów interfejsu użytkownika"""
        self.password_length_label = tk.Label(self.root, text=self.translations[self.current_language]["password_length"], font=("Courier", 12, "bold"))
        self.password_length_label.pack(pady=(20, 0))
        self.length_entry = tk.Entry(self.root, justify="center", font=("Courier", 13, "bold"), width=6)
        self.length_entry.pack(pady=10)

        self.letters_var = tk.BooleanVar(value=True)
        self.numbers_var = tk.BooleanVar(value=True)
        self.special_var = tk.BooleanVar(value=True)

        options_frame = tk.Frame(self.root)
        options_frame.pack(pady=10)

        self.letters_checkbutton = tk.Checkbutton(options_frame, text=self.translations[self.current_language]["letters"], variable=self.letters_var)
        self.letters_checkbutton.pack(anchor="center", pady=5)
        self.digits_checkbutton = tk.Checkbutton(options_frame, text=self.translations[self.current_language]["digits"], variable=self.numbers_var)
        self.digits_checkbutton.pack(anchor="center", pady=5)
        self.special_checkbutton = tk.Checkbutton(options_frame, text=self.translations[self.current_language]["special_chars"], variable=self.special_var)
        self.special_checkbutton.pack(anchor="center", pady=5)

        self.generated_password_label = tk.Label(self.root, text=self.translations[self.current_language]["generated_password"], font=("Courier", 12, "bold"))
        self.generated_password_label.pack(pady=(20, 0))
        self.password_entry = tk.Entry(self.root, justify="center", font=("Courier", 13, "bold"), width=32)
        self.password_entry.pack(pady=10)

        self.strength_label = tk.Label(self.root, text=self.translations[self.current_language]["password_strength"], font=("Courier", 12, "bold"))
        self.strength_label.pack(padx=(20, 0))

        self.strength_bar = tk.Canvas(self.root, width=20, height=20)
        self.strength_bar.pack(anchor="center")
        self.strength_bar.create_oval(5, 5, 20, 20, fill="white")

        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=20)

        self.generate_button = tk.Button(button_frame, text=self.translations[self.current_language]["generate_btn"], command=self.generate_password, width=15)
        self.generate_button.pack(side="top", pady=5)
        self.copy_button = tk.Button(button_frame, text=self.translations[self.current_language]["copy_btn"], command=self.copy_to_clipboard, width=15)
        self.copy_button.pack(side="top", pady=5)
        self.log_button = tk.Button(button_frame, text=self.translations[self.current_language]["log_btn"], command=self.show_log, width=15)
        self.log_button.pack(side="top", pady=5)
    
        self.footer_label = tk.Label(self.root, text="© 2024 FortiPass", font=("Courier", 8, "bold"), fg="gray")
        self.footer_label.pack(side=tk.BOTTOM, pady=5)

    def generate_password(self):
        """Generowanie hasła na podstawie wybranych opcji"""
        try:
            # Logowanie rozpoczęcia generowania hasła
            logging.debug("Starting the password generation.".upper())

            # Pobranie i sprawdzenie długości hasła
            length = int(self.length_entry.get() or 12)

            # Inicjalizacja procesu generowania hasła.
            logging.warning("Initializing the password generation process.")

            if length < 4:
                raise ValueError("Password length must be at least 4 characters.")
            if length > 128:
                raise ValueError("Password length must be no more than 128 characters.")

            # Sprawdzanie opcji
            use_letters = self.letters_var.get()
            use_numbers = self.numbers_var.get()
            use_special = self.special_var.get()

            # Logowanie składników hasła
            composition = []
            if use_letters:
                composition.append("letters")
            if use_numbers:
                composition.append("numbers")
            if use_special:
                composition.append("special characters")

            if not composition:
                error_message = "You must select at least one option!"
                logging.error("Component error: No component was selected to generate the password!")
                messagebox.showerror("FortiPass® - Error", error_message)
                return

            if not any([use_letters, use_numbers, use_special]):
                raise ValueError("You must select at least one option!")

            # Tworzenie bazy znaków na podstawie zaznaczonych opcji
            characters = ""
            if use_letters:
                characters += string.ascii_letters
            if use_numbers:
                characters += string.digits
            if use_special:
                characters += string.punctuation

            if not characters:
                raise ValueError("No characters available for password generation!")

            # Wykluczanie podobnych znaków
            similar_chars = "O0l1I"
            characters = ''.join(c for c in characters if c not in similar_chars)

            # Inicjalizowanie listy do hasła
            password = []

            # Dodanie po jednym znaku z każdej wybranej opcji
            if use_letters:
                password.append(secrets.choice(string.ascii_letters))
            if use_numbers:
                password.append(secrets.choice(string.digits))
            if use_special:
                password.append(secrets.choice(string.punctuation))

            # Wypełnianie reszty hasła losowymi znakami z dostępnych opcji
            remaining_length = length - len(password)
            all_selected_characters = ""
            if use_letters:
                all_selected_characters += string.ascii_letters
            if use_numbers:
                all_selected_characters += string.digits
            if use_special:
                all_selected_characters += string.punctuation

            # Generowanie pozostałych znaków
            password += [secrets.choice(all_selected_characters) for _ in range(remaining_length)]

            # Mieszanie znaków w haśle
            random.shuffle(password)

            # Finalne hasło
            password = ''.join(password)

            # Wyświetlanie hasła i jego siły
            self.password_entry.delete(0, tk.END)
            self.password_entry.insert(0, password)

            # Ocena złożoności wygenerowanego hasła (siła hasła)
            strength, color = self.evaluate_password_strength(password)
            self.update_strength_bar(strength, color)

            # Automatyczne zaznaczenie wygenerowanego hasła
            self.password_entry.select_range(0, tk.END)

            # Informacje o wygenerowanym haśle
            logging.info(f"Length: {length}.")
            logging.info(f"Include: {', '.join(composition)}.")
            logging.info(f"Strength: {strength}.")
            logging.info(f"The password generated successfully.")

        except ValueError as e:
            logging.error(f"Input error: {str(e)}!")
            messagebox.showerror("FortiPass® - Error", str(e))
        except Exception as e:
            logging.error(f"Generating the password: {str(e)}!")
            messagebox.showerror("FortiPass® - Error", "There was a problem generating the password!")

    def update_password_strength(self, strength_value):
        """Aktualizuje etykietę siły hasła i jej wartość"""
        translations = self.translations[self.current_language]
        if strength_value == "strong":
            strength_text = translations["strong"]
        elif strength_value == "medium":
            strength_text = translations["medium"]
        elif strength_value == "weak":
            strength_text = translations["weak"]
        else:
            strength_text = ""  # Brak tekstu dla pustego hasła

        # Aktualizacja tekstu siły hasła
        self.strength_label.config(text=f"{translations['password_strength']}{strength_text}")

    def evaluate_password_strength(self, password):
        """Ocena siły hasła na podstawie długości i różnych typów znaków"""
        length = len(password)
        has_letters = any(c.isalpha() for c in password)
        has_digits = any(c.isdigit() for c in password)
        has_specials = any(c in string.punctuation for c in password)

        # Kryteria siły hasła oraz wyświetlanej nazwy według ustawionego języka
        if length >= 12 and has_letters and has_digits and has_specials:
            return "Strong".lower(), "green"
        elif length >= 8 and (has_letters and has_digits or has_specials):
            return "Medium".lower(), "orange"
        else:
            return "Weak".lower(), "red"

    def update_strength_bar(self, strength, color):
        """Aktualizacja koła siły hasła i tekstu"""
        # Zaktualizowanie koła siły hasła
        self.strength_bar.delete("all")
        self.strength_bar.create_oval(5, 5, 20, 20, fill=color)  # Rysowanie koła z określonym kolorem
        
        # Zaktualizowanie tekstu siła hasła według ustawionego języka
        if self.current_language == "EN":
            self.strength_label.config(text=f"Password strength: {strength}")
        else:
            self.strength_label.config(text=f"Siła hasła: {strength}")

    def copy_to_clipboard(self):
        """Kopiowanie wygenerowanego hasła do schowka (Tkinter Clipboard)"""
        logging.debug("Copying to the clipboard:".upper())
        password = self.password_entry.get()
        logging.warning("Initializing the password copy to clipboard process.")
        if password:
            try:
                # Użycie Tkintera do kopiowania do schowka
                self.root.clipboard_clear()  # Czyszczenie schowka
                self.root.clipboard_append(password)  # Kopiowanie do schowka
                self.root.update()  # Zaktualizowanie schowka w systemie
                logging.info("The password was copied successfully.")
                messagebox.showinfo("FortiPass® - Success", "Password copied to clipboard!")
            except Exception as e:
                logging.error(f"Copying to clipboard: {str(e)}!")
                messagebox.showerror("FortiPass® - Error", "There was a problem copying the password to the clipboard!")
        else:
            logging.error("The attempt to copy an empty password was made!")
            messagebox.showerror("FortiPass® - Error", "There is no generated password to copy!")

    def on_scroll(self, event, log_text):
        """Reakcja na przewijanie"""
        if log_text.yview()[1] >= 1.0:  # Przewinięto do końca
            self.load_more_logs(log_text)

    def on_resize(self, log_text):
        """Reakcja na zmianę rozmiaru okna"""
        if log_text.yview()[1] >= 1.0:
                self.load_more_logs(log_text)

    def load_more_logs(self, log_text):
        """Wczytuje kolejne logi do wyświetlenia"""
        try:
            with open(self.log_file, "r") as f:
                f.seek(self.current_offset)
                lines = [f.readline() for _ in range(self.chunk_size)]
                if not lines:
                    return  # Brak więcej logów do wczytania

                for line in lines:
                    log_text.insert("end", line)

                self.current_offset = f.tell()

        except Exception as e:
            logging.error(f"Loading more the logs: {str(e)}!")
            messagebox.showerror("FortiPass® - Error", "The event log file could not be opened!")

    def show_log(self):
        """Otworzenie logu w nowym oknie w oddzielnym wątku"""
        logging.debug("Loading the event log:".upper())

        def open_log():
            try:
                logging.warning("Initiating the process of starting the event log.")
                logging.info("Loading and partitioning the log into chunks.")

                # Wczytywanie i dzielenie logu na partie
                log_content = ""
                with open(self.log_file, "r") as f:
                    # Wczytywanie logu w kawałkach
                    while True:
                        lines = []
                        for _ in range(self.chunk_size):
                            line = f.readline()
                            if not line:
                                break
                            lines.append(line)
                        if not lines:
                            break
                        log_content += ''.join(lines)

                self.show_log_window(log_content, None, None)

            except FileNotFoundError as fnf_error:
                logging.error(f"Loading the log file: {str(fnf_error)}!")
                messagebox.showerror("FortiPass® - Error", "The log file could not be found!")

            except PermissionError as perm_error:
                logging.error(f"Loading the log file: {str(perm_error)}!")
                messagebox.showerror("FortiPass® - Error", "You don't have the required permissions to access the log file.!")

            except Exception as e:
                logging.error(f"Error loading the event log file: {str(e)}!")
                messagebox.showerror("FortiPass® - Error", "The event log file could not be opened!")

        try:
            # Uruchomienie nowego wątku.
            threading.Thread(target=open_log, daemon=True).start()
            logging.info("The event log window was started in new thread successfully.")
        except Exception as e:
            logging.error("Starting a new thread: An error occurred while trying to start a new thread!")
            messagebox.showerror("FortiPass® - Error", "An error occurred while trying to open event log in a new thread!")

    def show_log_window(self, log_content, log_text, scrollbar):
        """Pokazuje zawartość logu w nowym oknie"""
        try:
            log_window = tk.Toplevel(self.root)
            log_window.title("FortiPass® - Event Log")

            # Wymiary ekranu
            screen_width = self.root.winfo_screenwidth()
            screen_height = self.root.winfo_screenheight()

            # Wymiary okna logu
            window_width = 1160
            window_height = 520

            # Obliczanie pozycji okna, aby było wyśrodkowane na ekranie
            position_top = (screen_height - window_height) // 2
            position_left = (screen_width - window_width) // 2

            # Ustawienie pozycji okna
            log_window.geometry(f'{window_width}x{window_height}+{position_left}+{position_top}')

            # Tworzenie kontenera na tekst z paskiem przewijania
            text_frame = tk.Frame(log_window)
            text_frame.pack(fill="both", expand=True)

            # Tworzenie paska przewijania w dół
            scrollbar = tk.Scrollbar(text_frame, orient="vertical")
            scrollbar.pack(side="right", fill="y")

            # Tworzenie widgetu Text do wyświetlania logu
            log_text = tk.Text(text_frame, wrap="word", font=("Courier", 11), width=175, height=40, yscrollcommand=scrollbar.set)
            log_text.pack(side="left", fill="both", expand=True, padx=10, pady=10)

            # Dodanie tagów dla stylizacji
            log_text.tag_config("DEBUG", foreground="blue")
            log_text.tag_config("INFO", foreground="green")
            log_text.tag_config("WARNING", foreground="orange")
            log_text.tag_config("FortiPass® - Error", foreground="red")

            # Wstawienie zawartości logu z kolorowaniem
            for line in log_content.splitlines():
                if "INFO" in line:
                    log_text.insert("end", line + "\n", "INFO")
                elif "WARNING" in line:
                    log_text.insert("end", line + "\n", "WARNING")
                elif "ERROR" in line:
                    log_text.insert("end", line + "\n", "ERROR")
                elif "DEBUG" in line:
                    log_text.insert("end", line + "\n", "DEBUG")
                else:
                    log_text.insert("end", line + "\n")  # Domyślny kolor

            log_text.config(state=tk.DISABLED)  # Zablokowanie edytowania tekstu

            # Ustawienie paska przewijania
            scrollbar.config(command=log_text.yview)

            # Dynamiczne ładowanie logów po przewinięciu do końca
            log_text.bind("<Configure>", lambda event: self.on_resize(log_text))
            log_text.bind("<MouseWheel>", lambda event: self.on_scroll(event, log_text))

            logging.info("The event log was displayed successfully.")

        except Exception as e:
            logging.error(f"Displaying the event log window: {str(e)}!")
            messagebox.showerror("FortiPass® - Error", "Failed to display the event log!")

    def shutdown_program_window(self, title, message):
        """Wyświetla okno dialogowe z pytaniem o zamknięcie programu 'Yes/No'."""
        
        logging.warning("Initiating the process of shutting down the program.")
        
        dialog = Toplevel(self.root)
        dialog.title(title)
        dialog.geometry("350x140")
        dialog.transient(self.root)  # Okno modalne
        dialog.grab_set()  # Blokujemy interakcje z innymi oknami

        # Dodajemy etykietę z wiadomością
        tk.Label(dialog, text=message, wraplength=250, font=("Courier", 13, "bold")).pack(pady=20)

        result = tk.BooleanVar(value=False)

        def on_yes():
            result.set(True)
            dialog.destroy()

        def on_no():
            result.set(False)
            dialog.destroy()

        tk.Button(dialog, text="Yes", command=on_yes, width=10).pack(side="left", padx=32, pady=10)
        tk.Button(dialog, text="No", command=on_no, width=10).pack(side="right", padx=32, pady=10)

        dialog.wait_window()  # Oczekuj na zamknięcie okna
        return result.get()

    def shutdown_program(self):
        """Zamyka program po potwierdzeniu użytkownika."""
        try:
            logging.debug("Shutting down the program:".upper())

            answer = self.shutdown_program_window("FortiPass® - Exit program", "Do you really want to exit the program?")
            if answer:
                self.locker.unlock_instance()
                root.quit()
                logging.info("The program shutdown successfully.")
            else:
                logging.info("The program shutdown cancelled by the user.")
        except Exception as e:
            logging.error(f"Shutting down the program: {str(e)}!")
            messagebox.showerror("FortiPass® - Error", "The program faced an issue that stopped it from closing properly!")
            sys.exit(1)
        finally:
            """ Upewnij się, że po zakończeniu działania aplikacji odblokujesz ją"""
            self.locker.unlock_instance()


# Utworzenie głównego okna aplikacji
if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordGeneratorApp(root)
    root.protocol("WM_DELETE_WINDOW", app.shutdown_program)
    root.mainloop()
