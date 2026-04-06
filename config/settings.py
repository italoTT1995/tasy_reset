import os
from dotenv import load_dotenv

# Carrega do path do Tasy_reset, ou local base
load_dotenv()

TASY_URL = os.getenv("TASY_URL")
ADMIN_USER = os.getenv("ADMIN_USER")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")

if not TASY_URL or not ADMIN_USER or not ADMIN_PASSWORD:
    raise Exception("Faltam variáveis de ambiente no arquivo .env (TASY_URL, ADMIN_USER, ADMIN_PASSWORD)")
