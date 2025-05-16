import os
import random
import tkinter as tk
from tkinter import filedialog, messagebox
from pathlib import Path
import pandas as pd
import json


FILE_GENERATORS = {
    'Binaire': lambda filename, size: generate_binary_file(filename, size),
    'Texte': lambda filename, size: generate_text_file(filename, size),
    'CSV': lambda filename, size: generate_csv_file(filename, size),
    'JSON': lambda filename, size: generate_json_file(filename, size),
    'Excel': lambda filename, size: generate_excel_file(filename, size),
}

def generate_binary_file(filename, size):
    with open(filename, 'wb') as f:
        for _ in range(size):
            f.write(os.urandom(1))
            f.write(random.randint(0, 255).to_bytes(1, byteorder='big'))
    return filename

def generate_text_file(filename, size):
    with open(filename, 'w') as f:
        for _ in range(size):
            f.write(os.urandom(1).decode('latin-1'))
    return filename

def generate_csv_file(filename, size):
    with open(filename, 'w') as f:
        for i in range(size):
            f.write(f"{i},{random.randint(0, 100)}\n")
    return filename

def generate_json_file(filename, size):
    data = {f"key_{i}": random.randint(0, 100) for i in range(size)}
    with open(filename, 'w') as f:
        json.dump(data, f)
    return filename

def generate_excel_file(filename, size):
    data = {
        'A': [random.randint(0, 100) for _ in range(size)],
        'B': [random.randint(0, 100) for _ in range(size)],
        'C': [random.randint(0, 100) for _ in range(size)],
    }
    df = pd.DataFrame(data)
    df.to_excel(filename, index=False)
    return filename

def generate_file(file_type, filename, size):
    try:
        return FILE_GENERATORS[file_type](filename, size)
    except KeyError:
        raise ValueError(f"Type de fichier '{file_type}' non pris en charge.")

def save_file_dialog():
    initial_dir = str(Path.home() / 'Documents')
    file_path = filedialog.asksaveasfilename(
        initialdir=initial_dir,
        title="Enregistrer le fichier",
        defaultextension=".txt",
        filetypes=[("Tous les fichiers", "*.*")]
    )
    return file_path

def on_generate():
    file_type = file_type_var.get()
    size = int(size_entry.get())
    filename = save_file_dialog()
    if filename:
        try:
            generated_file = generate_file(file_type, filename, size)
            messagebox.showinfo("Succès", f"Fichier '{generated_file}' généré avec succès !")
        except ValueError as e:
            messagebox.showerror("Erreur", str(e))

# Interface graphique avec Tkinter
root = tk.Tk()
root.title("Générateur de fichiers")
root.geometry("400x300")

file_type_var = tk.StringVar(value="Binaire")

file_type_label = tk.Label(root, text="Type de fichier")
file_type_label.pack()

file_type_menu = tk.OptionMenu(root, file_type_var, *FILE_GENERATORS.keys())
file_type_menu.pack()

size_label = tk.Label(root, text="Taille du fichier (en octets)")
size_label.pack()

size_entry = tk.Entry(root)
size_entry.pack()

generate_button = tk.Button(root, text="Générer le fichier", command=on_generate)
generate_button.pack()

root.mainloop()
