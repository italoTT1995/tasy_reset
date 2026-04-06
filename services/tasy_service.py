import os
import time
from datetime import datetime
from playwright.sync_api import sync_playwright, Page, Browser, Playwright
from config.settings import TASY_URL, ADMIN_USER, ADMIN_PASSWORD
from utils.logger import logger

class TasyService:
    def __init__(self, headless: bool = False):
        self.playwright: Playwright = None
        self.browser: Browser = None
        self.page: Page = None
        self.headless = headless
        
    def start(self):
        """Inicializa o Playwright e o Browser."""
        logger.info("Iniciando engine do Playwright...")
        self.playwright = sync_playwright().start()
        # Argumentos básicos para rodar bem o Chromium sem engasgos
        args = ["--start-maximized", "--disable-blink-features=AutomationControlled"]
        self.browser = self.playwright.chromium.launch(headless=self.headless, args=args)
        
        # Criação de contexto customizado simulando janela grande
        context = self.browser.new_context(viewport={'width': 1920, 'height': 1080})
        self.page = context.new_page()
        
    def tirar_screenshot_erro(self, nome_passo: str):
        """Salva screenshot em caso de falha."""
        pasta = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "screenshots")
        os.makedirs(pasta, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filepath = os.path.join(pasta, f"erro_{nome_passo}_{timestamp}.png")
        
        if self.page:
            self.page.screenshot(path=filepath, full_page=True)
            logger.info(f"Screenshot salvo em: {filepath}")

    def passo_1_login(self):
        """
        PASSO 1 — LOGIN
        """
        try:
            logger.info(f"Acessando Tasy em URL: {TASY_URL}")
            self.page.goto(TASY_URL, wait_until="networkidle")
            
            logger.info("Aguardando formulário de login e preenchendo as credenciais...")
            
            # Localizar de forma flexível a janela do Tasy
            input_usuario = self.page.locator("input[type='text']:visible, input[name*='user']:visible, input[placeholder*='usuário' i]:visible").first
            input_senha = self.page.locator("input[type='password']:visible").first
            
            input_usuario.wait_for(state="visible", timeout=30000)
            input_usuario.fill(ADMIN_USER)
            
            input_senha.wait_for(state="visible", timeout=5000)
            input_senha.fill(ADMIN_PASSWORD)
            
            logger.info("Clicando em Entrar...")
            botao_entrar = self.page.locator("button:has-text('Entrar'), button[type='submit'], button:has-text('Login')").first
            
            if botao_entrar.is_visible():
                botao_entrar.click()
            else:
                input_senha.press("Enter")
            
            # Angular costuma fazer redicionamento ou bootstrap completo após submeter
            self.page.wait_for_load_state("networkidle")
            logger.info("Login realizado com sucesso.")
            
        except Exception as e:
            logger.error(f"Erro no PASSO 1 (Login): {str(e)}")
            self.tirar_screenshot_erro("passo_1_login")
            raise

    def passo_2_acessar_menu(self):
        """
        PASSO 2 — ACESSAR ADMINISTRAÇÃO
        """
        try:
            logger.info("Aguardando carregamento da tela principal...")
            # Angular renderiza os modulos assimicronamente
            self.page.wait_for_selector("text='Administração do Sistema'", state="visible", timeout=60000)
            
            logger.info("Acessando módulo 'Administração do Sistema'...")
            self.page.get_by_text("Administração do Sistema", exact=False).first.click()
            
            # Aguarda ng-router processar
            self.page.wait_for_load_state("networkidle")
            
        except Exception as e:
            logger.error(f"Erro no PASSO 2 (Acessar Menu): {str(e)}")
            self.tirar_screenshot_erro("passo_2_acessar_menu")
            raise

    def passo_3_filtrar_usuario(self, login_usuario: str):
        """
        PASSO 3 — FILTRAR USUÁRIO
        """
        try:
            logger.info(f"Localizando o campo 'Usuário' para pesquisar por: {login_usuario}")
            
            # Recupera as caixas e foca na 2ª caixa. 
            # Fisicamente no Tasy: A 1ª caixa (índice 0) é "Nome". A 2ª caixa (índice 1) é "Usuário".
            inputs = self.page.locator("input[type='text']:visible")
            inputs.first.wait_for(state="visible", timeout=20000)
            
            input_user = inputs.nth(1)
            
            logger.info("Preeenchendo login do alvo na caixa 'Usuário'...")
            input_user.click(click_count=3)
            input_user.fill(login_usuario)
            
            logger.info("Pressionando 'Filtrar' ou clique verde...")
            input_user.press("Tab")
            input_user.press("Enter")
            
            # Clique no botão verde 'Filtrar' na parte de baixo
            botao_filtrar = self.page.locator("button:has-text('Filtrar'), button[title*='Filtrar' i]").last
            if botao_filtrar.is_visible(timeout=3000):
                 botao_filtrar.click()
                 
            self.page.wait_for_load_state("networkidle") 
            
        except Exception as e:
            logger.error(f"Erro no PASSO 3 (Filtrar Usuário): {str(e)}")
            self.tirar_screenshot_erro("passo_3_filtrar_usuario")
            raise

    def passo_4_selecionar_usuario(self, login_usuario: str):
        """
        PASSO 4 — SELECIONAR USUÁRIO
        """
        try:
            logger.info(f"Aprocurando na tabela de usuários pela linha com o texto: '{login_usuario}'")
            
            # Procura pela linha dentro da tabela. 
            row_locator = self.page.locator(f"tr:has-text('{login_usuario}')").first
            
            # Aguarda a linha ficar visível, e se expirar avisa que não encontrou controladamente.
            try:
                row_locator.wait_for(state="visible", timeout=15000)
            except Exception:
                raise ValueError(f"Usuário {login_usuario} não foi encontrado no sistema ou tabela não renderizou a tempo.")
            
            logger.info("Usuário validado e encontrado. Selecionando linha...")
            row_locator.click(button="left") # Clica com esquerdo para marcar no escopo
            
            # Aguarda o active state acionar do CSS do Angular
            self.page.wait_for_timeout(500)
            
        except Exception as e:
            logger.error(f"Erro no PASSO 4 (Selecionar Usuário): {str(e)}")
            self.tirar_screenshot_erro("passo_4_selecionar_usuario")
            raise

    def passo_5_abrir_menu_acoes(self, login_usuario: str):
        """
        PASSO 5 — MENU CONTEXTUAL
        """
        try:
            logger.info("Executando clique com Botão Direito do mouse no usuário...")
            
            row_locator = self.page.locator(f"tr:has-text('{login_usuario}')").first
            # Fazer clique na linha
            row_locator.click(button="right")
            
            # Aguardar render do menu customizado sobrepondo a tela
            # Menu de ações ExtJS/Angular do tasy geralmente é desancorado.
            menu_alterar = self.page.get_by_text("Alterar senha", exact=False).last
            
            logger.info("Aguardando popup com opções expandir na tela...")
            if not menu_alterar.is_visible(timeout=5000):
               # Fallback para caso o mouseout cortou a sub-aba, usar eval / force
               row_locator.click(button="right", force=True, delay=200)
               menu_alterar.wait_for(state="visible", timeout=10000)

            # Validação solicitada antes de interagir
            if menu_alterar.is_visible():
                logger.info("Opção 'Alterar senha' localziada e visível. Clicando...")
                menu_alterar.click()
            else:
                raise ValueError("Menu de Alterar Senha explodiu e ficou invisível antes do click.")
            
        except Exception as e:
            logger.error(f"Erro no PASSO 5 (Menu Contextual): {str(e)}")
            self.tirar_screenshot_erro("passo_5_abrir_menu_acoes")
            raise

    def passo_6_alterar_senha(self, nova_senha: str):
        """
        PASSO 6 — ALTERAÇÃO DE SENHA
        """
        try:
            logger.info("Aguardando carregamento da modal de troca de senha...")
            
            # A modal deve conter campos password. 
            inputs_senha = self.page.locator("input[type='password']:visible")
            inputs_senha.first.wait_for(state="visible", timeout=10000)
            
            n_fields = inputs_senha.count()
            logger.info(f"Localizados {n_fields} campos de senha. Inserindo nova senha em ambos.")
            
            if n_fields == 0:
                raise ValueError("Modal abriu mas não há boxes de senha visíveis.")
            
            # Preenche iterativamente as boxes existentes
            for i in range(n_fields):
                box = inputs_senha.nth(i)
                box.click(click_count=3)
                box.fill(nova_senha)

            # Localizar confirmar/salvar cruzando labels
            btn_salvar = self.page.locator("button:has-text('Salvar'), button:has-text('Confirmar'), button:has-text('OK')").first
            
            if not btn_salvar.is_visible():
                 raise Exception("Botão de Salvar/Confirmar não foi localizado no popup.")

            logger.info("Salvando nova senha no banco...")
            btn_salvar.click()
            
            # Aguarda a toast message ou loading mask
            self.page.wait_for_load_state("networkidle")
            
        except Exception as e:
            logger.error(f"Erro no PASSO 6 (Alteração de Senha): {str(e)}")
            self.tirar_screenshot_erro("passo_6_alterar_senha")
            raise

    def logout_e_encerrar(self):
        """
        PASSO 7 — FINALIZAÇÃO (Deslogar e encerrar Browser)
        """
        logger.info("Finalizando processo: Fechando Tasy e Browser de forma segura.")
        try:
            if self.page and not self.page.is_closed():
                # Tenta localizar o user icon/menu de sair se possivel
                btn_sair = self.page.locator("text='Sair', button[title*='Sair' i], i[class*='sign-out']").first
                if btn_sair.is_visible(timeout=3000):
                    btn_sair.click()
                self.page.close()
                
        except Exception:
            pass # Silencia erros no teardown
        
        finally:
            if self.browser:
                self.browser.close()
            if self.playwright:
                self.playwright.stop()
            logger.info("Sessão finalizada controladamente.")

def run_tasy_reset(usuario: str, nova_senha: str) -> bool:
    """Função orquestradora (Retry + Execução + Passo 7 Log/Validação)."""
    service = TasyService(headless=False)
    sucesso = False
    
    # Retry Simples
    tentativas = 2
    for tentativa in range(1, tentativas + 1):
        try:
            logger.info(f"==== INICIANDO RUN (TENTATIVA {tentativa}/{tentativas}) PARA: {usuario} ====")
            service.start()
            
            service.passo_1_login()
            service.passo_2_acessar_menu()
            service.passo_3_filtrar_usuario(usuario)
            service.passo_4_selecionar_usuario(usuario)
            service.passo_5_abrir_menu_acoes(usuario)
            service.passo_6_alterar_senha(nova_senha)
            
            sucesso = True
            break
            
        except Exception as e:
            logger.error(f"Falha na tentativa {tentativa}: {str(e)}")
            if tentativa == tentativas:
                logger.critical("Todas as tentativas falharam. Abortando processo total.")
        finally:
            service.logout_e_encerrar()
            
    # Validar sucesso no step final (Passo 7 - Validar operação)
    if sucesso:
         logger.info(f"==== SUCESSO: Senha do usuário [{usuario}] alterada no sistema ====")
         return True
    else:
         logger.error(f"==== ERRO: Operação falhou para [{usuario}] ====")
         return False
