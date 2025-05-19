'''''
import os
from cryptography.fernet import Fernet

def dechiffrer_fichiers(liste_fichiers, cle_chiffrement):
    """
    Déchiffre le contenu des fichiers spécifiés en utilisant la clé fournie.

    Args:
        liste_fichiers (list): Une liste des chemins de fichiers à déchiffrer.
        cle_chiffrement (bytes): La clé de chiffrement utilisée pour chiffrer les fichiers.
    """
    f = Fernet(cle_chiffrement)

    for chemin_fichier in liste_fichiers:
        try:
            with open(chemin_fichier, 'rb') as fichier_chiffre:
                contenu_chiffre = fichier_chiffre.read()

            contenu_original = f.decrypt(contenu_chiffre)

            with open(chemin_fichier, 'wb') as fichier_original:
                fichier_original.write(contenu_original)

            print(f"Le fichier '{chemin_fichier}' a été déchiffré.")

        except FileNotFoundError:
            print(f"Erreur: Le fichier '{chemin_fichier}' n'a pas été trouvé.")
        except Exception as e:
            print(f"Une erreur s'est produite lors du déchiffrement de '{chemin_fichier}': {e}")

if __name__ == "__main__":
    # Remplace cette clé par la clé que tu as utilisée pour le chiffrement !
    CLE_DE_CHIFFREMENT = b'ton_unique_cle_de_chiffrement_ici'

    # Exemple d'utilisation : déchiffrer tous les fichiers .py et .html du répertoire courant
    fichiers_a_dechiffrer = [f for f in os.listdir('.') if f.endswith(('.py', '.html'))]
    dechiffrer_fichiers(fichiers_a_dechiffrer, CLE_DE_CHIFFREMENT)
'''

import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from tkinter import messagebox

def charger_cle():
    """Charge la clé AES-256 depuis un fichier."""
    try:
        with open("cle.key", "rb") as cle_fichier:
            return cle_fichier.read()
    except FileNotFoundError:
        messagebox.showerror("Erreur", "Clé de chiffrement introuvable. Veuillez générer une clé.")
        return None

def dechiffrer_fichier(chemin_fichier, cle):
    """Déchiffre un fichier en utilisant AES-256 en mode CBC."""
    with open(chemin_fichier, 'rb') as f:
        donnees = f.read()
    
    iv = donnees[:16]  # Les 16 premiers octets sont l'IV
    donnees_chiffrees = donnees[16:]  # Le reste est le texte chiffré
    
    cipher = AES.new(cle, AES.MODE_CBC, iv)
    try:
        donnees_dechiffrees = unpad(cipher.decrypt(donnees_chiffrees), AES.block_size)
        with open(f"{chemin_fichier}_dechiffre", 'wb') as f:
            f.write(donnees_dechiffrees)
        print(f"Le fichier '{chemin_fichier}' a été déchiffré avec succès.")
    except ValueError:
        print(f"Erreur lors du déchiffrement de '{chemin_fichier}': données corrompues ou clé incorrecte.")

def dechiffrer_tous_les_fichiers():
    """Déchiffre tous les fichiers du répertoire courant."""
    cle = charger_cle()
    if cle:
        for fichier in os.listdir('.'):
            if os.path.isfile(fichier) and not fichier.endswith('_dechiffre'):
                try:
                    dechiffrer_fichier(fichier, cle)
                except Exception as e:
                    print(f"Erreur lors du traitement de '{fichier}': {e}")

if __name__ == "__main__":
    dechiffrer_tous_les_fichiers()
