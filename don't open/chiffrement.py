import os
from cryptography.fernet import Fernet

def serialiser_fichiers(liste_fichiers):
    """
    Chiffre le contenu des fichiers spécifiés.

    Args:
        liste_fichiers (list): Une liste des chemins de fichiers à chiffrer.
    """
    # Générer une clé de chiffrement. Il est CRUCIAL de conserver cette clé en sécurité !
    key = Fernet.generate_key()
    f = Fernet(key)

    print(f"Clé de chiffrement générée (à conserver en sécurité !): {key.decode()}")

    for chemin_fichier in liste_fichiers:
        try:
            with open(chemin_fichier, 'rb') as fichier:
                contenu_original = fichier.read()

            contenu_chiffre = f.encrypt(contenu_original)

            with open(chemin_fichier, 'wb') as fichier_chiffre:
                fichier_chiffre.write(contenu_chiffre)

            print(f"Le fichier '{chemin_fichier}' a été chiffré.")

        except FileNotFoundError:
            print(f"Erreur: Le fichier '{chemin_fichier}' n'a pas été trouvé.")
        except Exception as e:
            print(f"Une erreur s'est produite lors du traitement de '{chemin_fichier}': {e}")

if __name__ == "__main__":
    # Exemple d'utilisation : chiffrer tous les fichiers .py et .html du répertoire courant
    fichiers_a_chiffrer = [f for f in os.listdir('.') if f.endswith(('.py', '.html'))]
    serialiser_fichiers(fichiers_a_chiffrer)