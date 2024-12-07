<div align="center">
    <h1>🔍 Instrukcja uruchamiania testów w projekcie FortiPass</h1>
</div>

---

<h3>🚀 Krok 1: Przygotowanie środowiska</h3>

<h4>1.1. Zainstaluj wymagane zależności</h4>

Najpierw upewnij się, że masz zainstalowane wszystkie wymagane zależności, w tym `pytest` i inne niezbędne pakiety. Możesz to zrobić, instalując zależności za pomocą `pip`.

Jeśli masz plik `requirements.txt`, możesz zainstalować wszystkie wymagane pakiety jednocześnie:
- <b>pip install -r requirements.txt</b>

Jeśli nie masz requirements.txt, możesz ręcznie zainstalować pytest i pytest-mock:
- <b>pip install pytest pytest-mock</b>

<h4>1.2. Utwórz wirtualne środowisko (opcjonalnie)</h4>
Jeśli chcesz pracować w izolowanym środowisku, zaleca się utworzenie wirtualnego środowiska Pythona:
python3 -m venv venv

*Następnie aktywuj środowisko:*
- **source venv/bin/activate**

*Na systemie Windows:*
<li> **.\venv\Scripts\activate**</li>

---

<h3>🏗️ Krok 2: Przygotowanie struktury katalogów</h3>
Upewnij się, że struktura Twojego projektu wygląda tak:

<b>FortiPass/</b><br>
├── <b>src/</b><br>
│   ├── <i>main.py</i><br>
├── <b>tests/</b><br>
│   ├── <i>test_generate_password.py</i><br>
└── <i>README.md</i><br>

Plik testowy, np. test_generate_password.py, powinien znajdować się w katalogu tests.
Kod aplikacji powinien znajdować się w katalogu src.

<h3>🔧 Krok 3: Dodanie katalogu src do ścieżki Pythona</h3>
Aby upewnić się, że Python będzie mógł znaleźć kod w katalogu src, musisz dodać go do ścieżki Pythona.

Dodaj katalog src do ścieżki Pythona, używając zmiennej PYTHONPATH:

Uruchom testy, ustawiając PYTHONPATH na katalog src:
PYTHONPATH=src pytest tests/

Dzięki temu Python będzie wiedział, gdzie szukać modułów w katalogu src.

<h3>🏃‍♂️ Krok 4: Uruchamianie testów</h3>
Uruchom testy za pomocą pytest:

W katalogu głównym projektu uruchom pytest, aby uruchomić wszystkie testy znajdujące się w katalogu tests:
pytest tests/

Jeśli chcesz uruchomić testy w jednym pliku, możesz podać ścieżkę do tego pliku:
pytest tests/test_generate_password.py

<h4>4.1. Opcjonalnie: Dodaj argumenty do pytest</h4>
Aby uzyskać bardziej szczegółowy raport o testach, użyj flagi -v (verbose):
pytest -v tests/

Aby uruchomić tylko testy, które zmieniły się od ostatniego uruchomienia:
pytest --maxfail=1 --disable-warnings -q

Aby zignorować błędy i kontynuować testowanie:
pytest --continue-on-collection-errors

<h3>📊 Krok 5: Sprawdzanie wyników</h3>

<h4>5.1. Wyniki testów</h4>
Po uruchomieniu testów, pytest wyświetli raport w terminalu. Jeśli wszystkie testy przejdą pomyślnie, zobaczysz coś w rodzaju:

============================= test session starts ==============================
collected 5 items

tests/test_generate_password.py .....                                    [100%]

=============================== 5 passed in 1.23s ===============================

<h4>5.2. Błędy</h4>
Jeśli niektóre testy zawiodą, pytest pokaże szczegóły błędów, które pomogą Ci zdiagnozować problem.
