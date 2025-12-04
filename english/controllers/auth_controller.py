# On importe la classe 'UtilisateurModel' qui permet d’interagir avec la base de données (ajout, recherche, vérification…)
from models.utilisateur_model import UtilisateurModel

# On importe le module 're' pour utiliser les expressions régulières (utile pour valider l’adresse email)
import re

# On importe 'getpass' (non utilisé ici, mais utile si tu veux masquer le mot de passe pendant la saisie)
from getpass import getpass


# ------------------------------
# Fonction utilitaire : validation d’email
# ------------------------------
def valider_email(email):
    """
    Vérifie si l'email entré par l'utilisateur respecte un format valide.
    Exemple : 'nom@domaine.com'
    Retourne True si l'email est valide, sinon False.
    """
    return bool(re.match(r"[^@]+@[^@]+\.[^@]+", email))


# ------------------------------
# Classe principale : AuthController
# Elle gère toute la logique d’inscription et de connexion.
# ------------------------------
class AuthController:

    # --------------------------
    # Méthode d'inscription
    # --------------------------
    @staticmethod
    def inscription():
        """
        Gère le processus d’inscription d’un nouvel utilisateur.
        - Vérifie la validité des informations
        - Empêche les doublons d'email
        - Enregistre un nouvel utilisateur dans la base
        """
        print("\n=== INSCRIPTION ===")

        # Demande les informations de base à l’utilisateur
        nom = input("Nom : ")
        prenom = input("Prénom : ")
        email = input("Email : ").strip().lower()  # strip() supprime les espaces, lower() met en minuscule

        # Vérifie la validité de l’adresse email
        if not valider_email(email):
            print(" Email invalide.")
            return

        # Vérifie si l’email existe déjà dans la base de données
        if UtilisateurModel.trouver_par_email(email):
            print(" Cet email existe déjà.")
            return

        # Demande et confirme le mot de passe
        mot_de_passe = input("Mot de passe : ")
        confirmation = input("Confirmer : ")

        # Vérifie si les deux mots de passe correspondent
        if mot_de_passe != confirmation:
            print(" Les mots de passe ne correspondent pas.")
            return

        # Autres informations nécessaires à la création du compte
        numero = input("Numéro de téléphone : ")
        date_naissance = input("Date de naissance (YYYY-MM-DD) : ")
        adresse = input("Adresse : ")
        role = input("Rôle (CLIENT/MARCHAND/ADMIN) [CLIENT] : ").upper() or "CLIENT"

        # Appelle la méthode du modèle pour enregistrer l'utilisateur dans la base de données
        UtilisateurModel.creer_utilisateur(
            nom, prenom, email, mot_de_passe, numero, date_naissance, adresse, role
        )

        # Confirmation de création de compte
        print(" Compte créé avec succès.")


    # --------------------------
    # Méthode de connexion
    # --------------------------
    @staticmethod
    def connexion():
        """
        Gère le processus de connexion d’un utilisateur existant.
        - Vérifie l'email et le mot de passe dans la base
        - Affiche un message de bienvenue si la connexion réussit
        """
        print("\n=== CONNEXION ===")

        # Demande des identifiants à l'utilisateur
        email = input("Email : ").strip().lower()
        mot_de_passe = input("Mot de passe : ")

        # Vérifie si les identifiants sont corrects via la méthode du modèle
        user = UtilisateurModel.verifier_connexion(email, mot_de_passe)

        # Si un utilisateur est retourné, la connexion réussit
        if user:
            print(f" Bienvenue {user['prenom']} {user['nom']} ({user['role']})")

        # Sinon, message d'erreur
        else:
            print(" Identifiants invalides.")
