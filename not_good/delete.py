import os
import shutil

# Répertoire cible dont les fichiers pourraient être supprimés (À MODIFIER AVEC PRUDENCE POUR DES TESTS ISOLES)
REPERTOIRE_CIBLE = "/chemin/vers/un/repertoire/de/test"  # Remplacer par un répertoire de test VIDE

# Extension de fichier à cibler pour la suppression (peut être None pour tous les fichiers)
EXTENSION_CIBLE = ".txt"  # Exemple : ne cibler que les fichiers .txt, None pour tout

# Fonction pour supprimer les fichiers correspondants dans le répertoire cible
def supprimer_fichiers(repertoire, extension=None):
    try:
        print(f"Tentative de suppression des fichiers avec l'extension '{extension}' dans le répertoire : {repertoire}")
        for nom_fichier in os.listdir(repertoire):
            chemin_fichier = os.path.join(repertoire, nom_fichier)
            if os.path.isfile(chemin_fichier):
                if extension is None or nom_fichier.endswith(extension):
                    os.remove(chemin_fichier)
                    print(f"Supprimé : {chemin_fichier}")
        print("Opération de suppression terminée.")
    except FileNotFoundError:
        print(f"Erreur : Le répertoire '{repertoire}' n'a pas été trouvé.")
    except OSError as e:
        print(f"Erreur lors de la suppression des fichiers : {e}")

# Fonction (potentiellement malveillante) qui pourrait être déclenchée par un virus
def charge_utile_destructive():
    if REPERTOIRE_CIBLE == "/chemin/vers/un/repertoire/de/test":
        print("AVERTISSEMENT : Le répertoire cible n'a pas été configuré correctement. La suppression est annulée par sécurité.")
        print("Veuillez modifier 'REPERTOIRE_CIBLE' vers un répertoire de test VIDE si vous souhaitez observer (à vos risques et périls) ce comportement.")
        return

    supprimer_fichiers(REPERTOIRE_CIBLE, EXTENSION_CIBLE)

# Simuler l'exécution de la charge utile malveillante
if __name__ == "__main__":
    print("Simulation d'une charge utile destructive (à des fins éducatives UNIQUEMENT)")
    charge_utile_destructive()
    print("Fin de la simulation.")
    