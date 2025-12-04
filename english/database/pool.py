# ==========================================================
# Importations nécessaires
# ==========================================================

# 'pool' : permet de gérer un ensemble (pool) de connexions réutilisables à PostgreSQL
# 'OperationalError' : pour intercepter les erreurs liées à la base de données (mauvais identifiants, serveur injoignable, etc.)
from psycopg2 import pool, OperationalError

# 'contextmanager' : permet de créer des blocs "with" pour gérer proprement les connexions et curseurs
from contextlib import contextmanager

# 'Config' : contient les paramètres de connexion stockés dans le fichier .env (importés via config.py)
from config import Config

# 'psycopg2.extras' : permet d’utiliser des curseurs spéciaux comme 'RealDictCursor' pour récupérer les résultats sous forme de dictionnaires
import psycopg2.extras


# ==========================================================
# Variable globale pour stocker le pool de connexions
# ==========================================================
_conn_pool = None
# Elle sera initialisée une seule fois et réutilisée pendant toute la durée du programme


# ==========================================================
# Fonction : init_pool()
# ----------------------------------------------------------
# Initialise le pool de connexions PostgreSQL à partir des
# paramètres définis dans le fichier .env via la classe Config.
# ==========================================================
def init_pool():
    global _conn_pool

    # Si le pool n'est pas encore créé, on l'initialise
    if _conn_pool is None:
        try:
            # Création d’un pool de connexions multithreadé
            _conn_pool = pool.ThreadedConnectionPool(
                minconn=Config.PG_POOL_MIN,   # Nombre minimum de connexions actives
                maxconn=Config.PG_POOL_MAX,   # Nombre maximum de connexions simultanées
                host=Config.PG_HOST,           # Hôte PostgreSQL (souvent localhost)
                port=Config.PG_PORT,           # Port (par défaut 5432)
                database=Config.PG_DBNAME,     # Nom de la base de données
                user=Config.PG_USER,           # Nom d'utilisateur PostgreSQL
                password=Config.PG_PASSWORD,   # Mot de passe PostgreSQL
                sslmode=Config.PG_SSLMODE      # Mode SSL (disable, require, etc.)
            )

            # Si la création réussit, on confirme à l'utilisateur
            print("✅ Connexion PostgreSQL sécurisée établie.")

        # Si une erreur survient (serveur non accessible, identifiants incorrects, etc.)
        except OperationalError as e:
            # On élève une exception personnalisée avec un message clair
            raise RuntimeError(f"Échec de la connexion à PostgreSQL : {e}")


# ==========================================================
# Fonction : get_conn_cursor()
# ----------------------------------------------------------
# Fournit automatiquement une connexion et un curseur à la base
# via un bloc 'with', et gère leur libération proprement.
#
# Exemple d’utilisation :
#   with get_conn_cursor(dict_cursor=True) as (conn, cur):
#       cur.execute("SELECT * FROM utilisateur")
#       result = cur.fetchall()
#
# ==========================================================
@contextmanager
def get_conn_cursor(dict_cursor=False):
    global _conn_pool

    # Si le pool n’a pas encore été initialisé, on le fait maintenant
    if _conn_pool is None:
        init_pool()

    # On récupère une connexion disponible dans le pool
    conn = _conn_pool.getconn()

    try:
        # Création d’un curseur :
        # Si dict_cursor=True → les résultats seront sous forme de dictionnaire (clé = nom de colonne)
        # Sinon → résultats classiques (tuple)
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor if dict_cursor else None)

        # On "donne" la connexion et le curseur au bloc "with"
        yield conn, cur

    except Exception:
        # En cas d’erreur SQL ou autre, on annule la transaction pour éviter les incohérences
        conn.rollback()
        raise

    finally:
        # Fermeture du curseur proprement
        cur.close()

        # On remet la connexion dans le pool (au lieu de la fermer complètement)
        _conn_pool.putconn(conn)
