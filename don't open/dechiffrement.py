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