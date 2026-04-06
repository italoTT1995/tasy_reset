import sys
from loguru import logger
import os
from datetime import datetime

logger.remove()

# Formatação limpa de terminal
logger.add(sys.stdout, format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{message}</cyan>", level="INFO")

# Arquivo na pasta logs com rotation
log_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "logs")
os.makedirs(log_dir, exist_ok=True)

arquivo = os.path.join(log_dir, f"tasy_reset_{datetime.now().strftime('%Y%m%d')}.log")
logger.add(arquivo, rotation="10 MB", retention="10 days", level="INFO", encoding='utf-8')
