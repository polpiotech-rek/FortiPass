# fortipass/main.py
#
# Copyright (c) 2024 Piotr Bodych
# Licensed under the MIT License. See LICENSE file in the project root for details.


import os, sys, fcntl, logging
from pathlib import Path


class AppLocker:
    def __init__(self, lock_file="/tmp/fortipass.lock"):
        self.lock_file = lock_file
        self.lock = None

        """Ustawienia logowania zdarzeń w programie"""
        try:
            # Pobranie katalogu nadrzędnego i utworzenie katalogu "logs
            parent_dir = Path(__file__).resolve().parent.parent
            log_dir = parent_dir / "logs"
            log_dir.mkdir(exist_ok=True)
            log_file = log_dir / "password_generator.log"
            self.log_file = log_file

            # Sprawdź, czy plik dziennika istnieje, utwórz go, jeśli nie
            if not log_file.exists():
                log_file.touch()

            # Konfiguracja rejestrowania
            logging.basicConfig(
                filename=log_file,
                level=logging.DEBUG,
                format="%(asctime)s - %(levelname)s - %(message)s"
            )

        except Exception as e:
            print(f"Error setting up logging: {e}!")
            sys.exit(1)

    def lock_instance(self):
        # Sprawdź, czy aplikacja jest już uruchomiona
        try:
            # Otwórz plik blokady i zapisz do niego bieżący PID
            self.lock = open(self.lock_file, 'w')
            fcntl.flock(self.lock, fcntl.LOCK_EX | fcntl.LOCK_NB)

            # Zapisanie bieżącego PID do pliku blokady
            pid = os.getpid()
            self.lock.write(str(pid))
            self.lock.flush() #Upewnij się, że PID jest zapisywany natychmiast



            logging.info(f"A unique process PID: {pid} has been assigned in the operating system.")
        except IOError:
            # Blokada jest już w posiadaniu innej instancji, odczytaj jej PID
            with open(self.lock_file, 'r') as f:
                existing_pid = f.read().strip()
            logging.error(f"The program is already running. Multiple instances are not allowed!")
            sys.exit(1)

    def unlock_instance(self):
        if self.lock:
            try:
                # Zwolnij blokadę i zamknij plik
                fcntl.flock(self.lock, fcntl.LOCK_UN)
                self.lock.close()

                # Usuń plik blokady
                os.remove(self.lock_file)

                # Sprawdź, czy plik został rzeczywiście usunięty
                if not os.path.exists(self.lock_file):
                    logging.info("The application instance has been terminated.")
                    logging.info("The lock file has been removed from the system.")
                else:
                    raise FileNotFoundError("The lock file could not be removed!")

            except (OSError, FileNotFoundError) as e:
                # Obsługuje przypadek, gdy nie udało się usunąć pliku lub plik nadal istnieje
                logging.error(f"Error during unlocking: {str(e)}!")
                sys.exit(1)
