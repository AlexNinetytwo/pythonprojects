import pafy
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import os
import threading
# import threading

default_filename = ""
path_and_name = ""
selected_path = "./"
given_name = default_filename

converting = False

def on_closing():
    convert_thread.stop()


def short_path(path):
    if len(path) > 40:
        path = path[:20] + "..." + path[-20:]
    return path

def update_path():
    global selected_path, default_filename, path_and_name, given_name
    try:
        default_filename = pafy.new(url_entry.get()).title + ".mp3"
        path_and_name = selected_path + default_filename
        path_label.configure(text=short_path(path_and_name))
    except:
        selected_path = selected_path.replace(given_name,"")
        path_label.configure(text=short_path(selected_path))
        print(given_name)

def start():
    global converting, convert_label
    # Püfe ob nicht Konvertiert wird
    if not converting:
        
        convert_thread.start()
        # Konvertiert...
        convert_label.configure(text="Konvertiert...")
        # Deaktiviere die Buttons während des Konvertiervorganges
        convert_button.configure(state=tk.DISABLED)
        select_path_button.configure(state=tk.DISABLED)


def convert_to_mp3():
    # Setze den Konvertierstatus
    global converting, path_and_name
    converting = True
    
    # Hole das YouTube-Video
    video = pafy.new(url_entry.get())
    # Hole den besten Audio-Stream
    try:
        best_audio = video.getbestaudio()
        # Lade den Audio-Stream herunter und speichere ihn an dem von dem Benutzer ausgewählten Ort
        best_audio.download(filepath=path_and_name)
        # Reaktiviere die Buttons nach dem Kovertiervorgang
        messagebox.showinfo("YouTube to MP3 Converter", "Konvertierung abgeschlossen.")
        convert_button.configure(state=tk.NORMAL)
        select_path_button.configure(state=tk.NORMAL)
        # Setze den Konvertierstatus
        converting = False
        # Entferne "Konvertiert..."
        convert_label.configure(text="")
    except:
        messagebox.showinfo("YouTube to MP3 Converter", "Konvertierung fehlgeschlagen.")
        convert_button.configure(state=tk.NORMAL)
        select_path_button.configure(state=tk.NORMAL)
        converting = False

convert_thread = threading.Thread(target=convert_to_mp3)

def select_path():
    global selected_path, default_filename, given_name, path_and_name
    # Hole das YouTube-Video
    video = pafy.new(url_entry.get())
    # Setze den Standardnamen für die heruntergeladene mp3-Datei auf den Titel des YouTube-Videos
    default_filename = video.title + ".mp3"
    default_filename = default_filename.replace("?","")
    # Öffne einen Dateiauswahl-Dialog, um den Speicherpfad auszuwählen
    path_and_name = filedialog.asksaveasfilename(
        title="Speicherort auswählen", initialfile=default_filename, defaultextension=".mp3", filetypes=[("MP3 files", "*.mp3")])
    given_name = os.path.basename(path_and_name)
    selected_path = path_and_name.replace(given_name,"")
    # Aktualisiere das path_label mit dem ausgewählten Pfad
    update_path()


# Erstelle ein neues tkinter-Fenster
window = tk.Tk()
window.title("YouTube to MP3 Converter")

# Setze die Hintergrundfarbe des Fensters
window.configure(bg="#f0f0f0")

# Erstelle ein Label für die YouTube-URL
url_label = tk.Label(text="YouTube URL:", font=(
    "Arial", 14), fg="#000000", bg="#f0f0f0")

# Erstelle ein Eingabefeld für die YouTube-URL
url_entry = tk.Entry(font=("Arial", 14), bg="#ffffff")

# Erstelle einen Button zum Starten der Konvertierung
convert_button = tk.Button(text="Convert", font=(
    "Arial", 14), fg="#ffffff", bg="#0000ff", command=start)

# Erstelle einen Button zum Auswählen des Speicherpfads
select_path_button = tk.Button(text="Select Save Location", font=(
    "Arial", 14), fg="#ffffff", bg="#0000ff", command=select_path)

# Erstelle ein Label zum Anzeigen des ausgewählten Pfads
path_label = tk.Label(text="", font=("Arial", 14), fg="#000000", bg="#f0f0f0")

# Erstelle ein Label zum Anzeigen des Konvertierstatus
convert_label = tk.Label(text="", font=("Arial", 14), fg="#000000", bg="#f0f0f0")

# Verwende das grid-Geometry-Manager, um die widgets im Fenster zu organisieren
url_label.grid(row=0, column=0, padx=5, pady=5)
url_entry.grid(row=0, column=1, padx=5, pady=5)
convert_label.grid(row=1, column=0, padx=5, pady=5)
convert_button.grid(row=1, column=1, padx=5, pady=5)
path_label.grid(row=2, column=0, padx=5, pady=5)
select_path_button.grid(row=2, column=1, padx=5, pady=5)

# Registriere den Event-Handler für das Schließen des Fensters
window.protocol("WM_DELETE_WINDOW", on_closing)


def is_valid_url(url):
    # Prüfe, ob die URL mit "https://www.youtube.com/watch?v=" beginnt
    if not url.startswith("https://www.youtube.com/watch?v="):
        return False
    # Prüfe, ob die URL 11 Zeichen nach "https://www.youtube.com/watch?v=" enthält (der YouTube-Video-ID)
    if len(url) != 43:
        return False
    return True


def update_buttons():
    update_path()
    # Hole den Inhalt des Eingabefelds
    url = url_entry.get()
    # Prüfe, ob der Inhalt eine gültige YouTube-URL ist
    if is_valid_url(url):
        # Aktiviere die Buttons, wenn eine gültige URL eingegeben wurde
        convert_button.configure(state=tk.NORMAL)
        select_path_button.configure(state=tk.NORMAL)
    else:
        # Deaktiviere die Buttons, wenn keine gültige URL eingegeben wurde
        convert_button.configure(state=tk.DISABLED)
        select_path_button.configure(state=tk.DISABLED)


# Füge einen Eingabe-Event-Handler hinzu, um die Buttons bei jeder Eingabe im Eingabefeld zu aktualisieren
url_entry.bind("<KeyRelease>", lambda event: update_buttons())

# Aktualisiere die Buttons zu Beginn
update_buttons()

window.mainloop()
