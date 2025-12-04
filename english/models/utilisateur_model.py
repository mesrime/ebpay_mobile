# ==========================================================
# Importations des bibliothèques nécessaires
# ==========================================================
import hashlib, os, binascii, hmac  # Pour le hashage et la vérification sécurisée des mots de passe
from datetime import datetime  # Pour ajouter la date d'inscription
from database.pool import get_conn_cursor  # Pour exécuter des requêtes SQL sécurisées via le pool de connexions

# ==========================================================
# Paramètres de sécurité pour le hashage des mots de passe
# ==========================================================
HASH_NAME = "sha256"  # Algorithme utilisé (SHA-256)
ITERATIONS = 200_000  # Nombre d'itérations pour PBKDF2 (plus élevé = plus sécurisé)
SALT_BYTES = 16  # Taille du sel aléatoire (en octets)
DKLEN = 32  # Taille du hash dérivé (en octets)

# Définition des rôles autorisés dans le système
ROLES = {"CLIENT", "MARCHAND", "ADMIN"}


# ==========================================================
# Fonction : hash_password
# ==========================================================
def hash_password(password: str) -> str:
    """
    Hache un mot de passe avec un sel unique en utilisant PBKDF2-HMAC-SHA256.

    Args:
        password (str): mot de passe en clair à hacher

    Returns:
        str: chaîne formatée sous forme "iterations$salt_hex$hash_hex"
    """
    # Génère un sel cryptographique aléatoire
    salt = os.urandom(SALT_BYTES)

    # Calcule le hash du mot de passe avec PBKDF2 (Password-Based Key Derivation Function 2)
    dk = hashlib.pbkdf2_hmac(HASH_NAME, password.encode(), salt, ITERATIONS, DKLEN)

    # Convertit le sel et le hash en chaîne hexadécimale pour stockage en base de données
    return f"{ITERATIONS}${binascii.hexlify(salt).decode()}${binascii.hexlify(dk).decode()}"


# ==========================================================
# Fonction : verify_password
# ==========================================================
def verify_password(stored: str, attempt: str) -> bool:
    """
    Vérifie si le mot de passe fourni correspond au hash enregistré en base.

    Args:
        stored (str): le hash complet stocké (format "iterations$salt$hash")
        attempt (str): mot de passe entré par l'utilisateur

    Returns:
        bool: True si les mots de passe correspondent, sinon False
    """
    try:
        # Découpe le hash stocké pour récupérer le nombre d'itérations, le sel et le hash
        iters, salt_hex, hash_hex = stored.split("$")

        # Reconstruit le sel binaire à partir de sa forme hexadécimale
        salt = binascii.unhexlify(salt_hex)

        # Recalcule le hash du mot de passe saisi avec le même sel et le même nombre d'itérations
        dk = hashlib.pbkdf2_hmac(HASH_NAME, attempt.encode(), salt, int(iters), DKLEN)

        # Compare les deux hash de manière sécurisée (évite les attaques par timing)
        return hmac.compare_digest(binascii.hexlify(dk).decode(), hash_hex)
    except Exception:
        # Si le format est invalide ou une erreur survient, on retourne False
        return False


# ==========================================================
# Classe principale : UtilisateurModel
# ----------------------------------------------------------
# Gère toutes les opérations liées aux utilisateurs :
# - Création d’un utilisateur
# - Recherche d’un utilisateur par email
# - Vérification de connexion
# ==========================================================
class UtilisateurModel:

    # ------------------------------------------------------
    # Méthode : creer_utilisateur
    # ------------------------------------------------------
    @staticmethod
    def creer_utilisateur(nom, prenom, email, mot_de_passe, numero, date_naissance, adresse, role="CLIENT"):
        """
        Crée un nouvel utilisateur dans la base de données.
        Les mots de passe sont toujours hachés avant d’être enregistrés.

        Args:
            nom, prenom, email, mot_de_passe, numero, date_naissance, adresse, role
        """
        # Si le rôle fourni n'est pas reconnu, on le remplace par "CLIENT"
        if role not in ROLES:
            role = "CLIENT"

        # Hachage sécurisé du mot de passe avant insertion
        mot_hash = hash_password(mot_de_passe)

        # Ouverture d’une connexion sécurisée via le pool
        with get_conn_cursor() as (conn, cur):
            # Requête SQL d’insertion d’un nouvel utilisateur
            query = """
                INSERT INTO public.utilisateur (
                    nom, prenom, email, mot_de_passe,
                    numero_telephone, date_naissance, adresse,
                    kyc_status, role, niveau_verification, date_inscription
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, 'EN_ATTENTE', %s, 0, %s)
            """

            # Exécution de la requête avec des valeurs paramétrées (protège contre l’injection SQL)
            cur.execute(query, (
                nom, prenom, email, mot_hash, numero, date_naissance,
                adresse, role, datetime.now()
            ))

            # Validation (commit) des changements dans la base
            conn.commit()

    # ------------------------------------------------------
    # Méthode : trouver_par_email
    # ------------------------------------------------------
    @staticmethod
    def trouver_par_email(email):
        """
        Recherche un utilisateur en base à partir de son adresse email.

        Args:
            email (str): l'adresse email de l'utilisateur

        Returns:
            dict | None: un dictionnaire contenant les infos de l'utilisateur,
                         ou None si aucun utilisateur trouvé.
        """
        with get_conn_cursor(dict_cursor=True) as (conn, cur):
            cur.execute("SELECT * FROM public.utilisateur WHERE email = %s", (email,))
            return cur.fetchone()

    # ------------------------------------------------------
    # Méthode : verifier_connexion
    # ------------------------------------------------------
    @staticmethod
    def verifier_connexion(email, mot_de_passe):
        """
        Vérifie les identifiants de connexion (email + mot de passe).

        Args:
            email (str): email de l'utilisateur
            mot_de_passe (str): mot de passe en clair entré par l'utilisateur

        Returns:
            dict | None: renvoie les infos de l'utilisateur si succès, sinon None.
        """
        # Recherche de l’utilisateur par email
        user = UtilisateurModel.trouver_par_email(email)

        # Si l'utilisateur n'existe pas, on renvoie None
        if not user:
            return None

        # Vérification du mot de passe haché
        if verify_password(user["mot_de_passe"], mot_de_passe):
            return user  # Connexion réussie

        # Sinon, échec de la vérification
        return None
