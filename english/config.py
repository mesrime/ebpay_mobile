# ==========================================================
# Importations nécessaires
# ==========================================================

# 'os' permet d'accéder aux variables d'environnement du système
import os

# 'dotenv' permet de charger automatiquement les variables définies dans le fichier .env
from dotenv import load_dotenv


# ==========================================================
# Chargement des variables d'environnement
# ----------------------------------------------------------
# Cette fonction lit le fichier .env situé à la racine du projet
# et ajoute les valeurs qu'il contient aux variables d'environnement du système.
#
# Exemple de .env :
#   PG_HOST=localhost
#   PG_DBNAME=ebpay
#   PG_USER=postgres
#   PG_PASSWORD=mon_mot_de_passe
# ==========================================================
load_dotenv()


# ==========================================================
# Classe de configuration globale : Config
# ----------------------------------------------------------
# Cette classe regroupe toutes les variables nécessaires
# à la connexion et à la gestion du pool PostgreSQL.
# Les valeurs sont lues depuis les variables d'environnement,
# ce qui évite de stocker des informations sensibles en clair dans le code.
# ==========================================================
class Config:
    # Adresse du serveur PostgreSQL (souvent localhost)
    PG_HOST = os.getenv("PG_HOST")

    # Port d'écoute de PostgreSQL (par défaut 5432)
    PG_PORT = int(os.getenv("PG_PORT", 5432))

    # Nom de la base de données à laquelle on veut se connecter
    PG_DBNAME = os.getenv("PG_DBNAME")

    # Nom d'utilisateur PostgreSQL
    PG_USER = os.getenv("PG_USER")

    # Mot de passe associé à l'utilisateur PostgreSQL
    PG_PASSWORD = os.getenv("PG_PASSWORD")

    # Mode SSL (utile pour les connexions distantes sécurisées)
    # 'disable' = aucune sécurité SSL (local)
    # 'require' = impose une connexion sécurisée SSL
    PG_SSLMODE = os.getenv("PG_SSLMODE", "disable")

    # Taille minimale du pool de connexions
    # (nombre minimum de connexions gardées ouvertes)
    PG_POOL_MIN = int(os.getenv("PG_POOL_MIN", 1))

    # Taille maximale du pool de connexions
    # (nombre maximum de connexions simultanées autorisées)
    PG_POOL_MAX = int(os.getenv("PG_POOL_MAX", 5))
