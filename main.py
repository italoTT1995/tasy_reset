import argparse
import sys
from utils.logger import logger
from services.tasy_service import run_tasy_reset

def main():
    parser = argparse.ArgumentParser(description="Automação Tasy EMR - Redefinição de Senha")
    parser.add_argument("--usuario", type=str, required=True, help="Login do usuário alvo")
    parser.add_argument("--nova_senha", type=str, required=True, help="A nova senha a ser registrada")
    
    args = parser.parse_args()
    
    logger.info("Iniciando script de Reset via CLI...")
    logger.info(f"Parâmetros recebidos: Usuário={args.usuario}")
    
    sucesso = run_tasy_reset(args.usuario, args.nova_senha)
    
    if sucesso:
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()
