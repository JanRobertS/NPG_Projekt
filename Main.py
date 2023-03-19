import os

notes_dir = "notes"  # nazwa folderu, w którym będą przechowywane notatki
if not os.path.exists(notes_dir):
    os.makedirs(notes_dir)

notes = {}  # słownik, w którym przechowywane będą notatki

def save_note():
    title = input("\nPodaj tytuł notatki: ")
    note = input("\nWpisz notatkę: ")
    filename = os.path.join(notes_dir, title + ".txt")  # utwórz ścieżkę do pliku notatki
    with open(filename, "w") as f:
        f.write(note)  # zapisz notatkę do pliku
    notes[title] = filename  # dodaj notatkę do słownika
    print("\nNotatka została zapisana!\n\n")

def read_note():
    if not notes:
        print("\nBrak dostępnych notatek.\n\n")
        return
    print("\nDostępne notatki:")
    i = 0
    for title in notes:
        i += 1
        print(i, title, sep='.')
    title = input("\nPodaj tytuł notatki: ")
    if title in notes:
        filename = notes[title]
    else:
        filename = os.path.join(notes_dir, title + ".txt")  # utwórz ścieżkę do pliku notatki
    if os.path.exists(filename):
        with open(filename) as f:
            note = f.read()  # odczytaj notatkę z pliku
        print(note)  # wyświetl notatkę
    else:
        print("\nNotatka o takim tytule nie istnieje.\n")

# odczytaj istniejące notatki z folderu notes
for filename in os.listdir(notes_dir):
    if filename.endswith(".txt"):
        title = os.path.splitext(filename)[0]  # usuń rozszerzenie z nazwy pliku
        notes[title] = os.path.join(notes_dir, filename)

while True:
    print("Co chcesz zrobić?")
    print("1. Utworzyć notatkę")
    print("2. Odczytać notatkę")
    print("3. Wyjść z programu")
    choice = input("Wybierz opcję: ")
    if choice == "1":
        save_note()
    elif choice == "2":
        read_note()
    elif choice == "3":
        break
    else:
        print("\nNiepoprawny wybór. Spróbuj jeszcze raz.\n")
