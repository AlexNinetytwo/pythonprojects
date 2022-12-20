import pafy
import tkinter as tk
from tkinter import filedialog
import threading

selected_path = "./"
event = threading.Event()



def start_threading(): 
    threading.Thread(target=convert_message).start()
    convert_to_mp3()


def convert_message():
    message = tk.Tk()
    label = tk.Label(message,text="Converting...")
    label.pack()
    message.mainloop()


def convert_to_mp3():
    # Informiere über den Convertierungvorgang
    threading.Thread(target=convert_message).start()
    # Hole das YouTube-Video
    video = pafy.new(url_entry.get())
    # Hole den besten Audio-Stream
    best_audio = video.getbestaudio()
    # Lade den Audio-Stream herunter und speichere ihn an dem von dem Benutzer ausgewählten Ort
    best_audio.download(filepath=selected_path)
    # Setze die Nachricht auf "Conversion complete"
    event.set()

def select_path():
    global selected_path
    # Hole das YouTube-Video
    video = pafy.new(url_entry.get())
    # Setze den Standardnamen für die heruntergeladene mp3-Datei auf den Titel des YouTube-Videos
    default_filename = video.title + ".mp3"
    # Öffne einen Dateiauswahl-Dialog, um den Speicherpfad auszuwählen
    selected_path = filedialog.asksaveasfilename(title="Select save location", initialfile=default_filename, defaultextension=".mp3", filetypes=[("MP3 files", "*.mp3")])
    # Aktualisiere das path_label mit dem ausgewählten Pfad
    path_label.configure(text=selected_path)

# Erstelle ein neues tkinter-Fenster
window = tk.Tk()
window.title("YouTube to MP3 Converter")

# Setze die Hintergrundfarbe des Fensters
window.configure(bg="#f0f0f0")

# Erstelle ein Label für die YouTube-URL
url_label = tk.Label(text="YouTube URL:", font=("Arial", 14), fg="#000000", bg="#f0f0f0")

# Erstelle ein Eingabefeld für die YouTube-URL
url_entry = tk.Entry(font=("Arial", 14), bg="#ffffff")

# Erstelle einen Button zum Starten der Konvertierung
convert_button = tk.Button(text="Convert", font=("Arial", 14), fg="#ffffff", bg="#0000ff", command=start_threading)

# Erstelle einen Button zum Auswählen des Speicherpfads
select_path_button = tk.Button(text="Select Save Location", font=("Arial", 14), fg="#ffffff", bg="#0000ff", command=select_path)

# Erstelle ein Label zum Anzeigen des ausgewählten Pfads
path_label = tk.Label(text="", font=("Arial", 14), fg="#000000", bg="#f0f0f0")

# Verwende das grid-Geometry-Manager, um die widgets im Fenster zu organisieren
url_label.grid(row=0, column=0, padx=5, pady=5)
url_entry.grid(row=0, column=1, padx=5, pady=5)
convert_button.grid(row=1, column=1, padx=5, pady=5)
select_path_button.grid(row=2, column=1, padx=5, pady=5)


def is_valid_url(url):
    # Prüfe, ob die URL mit "https://www.youtube.com/watch?v=" beginnt
    if not url.startswith("https://www.youtube.com/watch?v="):
        return False
    # Prüfe, ob die URL 11 Zeichen nach "https://www.youtube.com/watch?v=" enthält (der YouTube-Video-ID)
    if len(url) != 43:
        return False
    return True

def update_buttons():
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




