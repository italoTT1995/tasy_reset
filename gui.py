import customtkinter as ctk
import threading
import sys
from utils.logger import logger
from services.tasy_service import run_tasy_reset

# Configurações de Aparência do CustomTkinter
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Tasy Password Reset v1.0")
        self.geometry("450x550")
        self.resizable(False, False)

        # Header
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.pack(pady=20, padx=20, fill="x")
        
        self.lbl_title = ctk.CTkLabel(self.header_frame, text="Tasy EMR\nReset Automático", font=ctk.CTkFont(size=24, weight="bold"))
        self.lbl_title.pack()

        # Input Frame
        self.input_frame = ctk.CTkFrame(self)
        self.input_frame.pack(pady=10, padx=20, fill="x")

        self.lbl_user = ctk.CTkLabel(self.input_frame, text="Login do Usuário:")
        self.lbl_user.pack(pady=(10, 0), padx=20, anchor="w")
        self.ent_user = ctk.CTkEntry(self.input_frame, placeholder_text="Ex: itlsilva", width=300)
        self.ent_user.pack(pady=(0, 10), padx=20)

        self.lbl_pass = ctk.CTkLabel(self.input_frame, text="Nova Senha:")
        self.lbl_pass.pack(pady=(5, 0), padx=20, anchor="w")
        self.ent_pass = ctk.CTkEntry(self.input_frame, placeholder_text="Digite a senha", width=300, show="*")
        self.ent_pass.pack(pady=(0, 15), padx=20)

        # Action Botão
        self.btn_run = ctk.CTkButton(self, text="▶ Executar Redefinição", height=40, font=ctk.CTkFont(weight="bold"), command=self.start_automation)
        self.btn_run.pack(pady=10, padx=20, fill="x")

        # Terminal Box (Logs)
        self.terminal_label = ctk.CTkLabel(self, text="Terminal de Execução:", font=ctk.CTkFont(size=12, slant="italic"))
        self.terminal_label.pack(pady=(15, 0), padx=20, anchor="w")
        
        self.log_box = ctk.CTkTextbox(self, width=400, height=220, state="disabled", fg_color="#121212", text_color="#00FF00")
        self.log_box.pack(pady=(5, 20), padx=20, fill="both", expand=True)

        # Hook do loguru na interface
        logger.add(self.log_to_gui, format="{time:HH:mm:ss} | {level} | {message}")

    def log_to_gui(self, message):
        """Receptor de mensagens que vem do Loguru para jogar no painel"""
        self.log_box.configure(state="normal")
        self.log_box.insert("end", message)
        self.log_box.see("end")  # Auto-scroll pra última linha
        self.log_box.configure(state="disabled")

    def worker_thread(self, user, pwd):
        """Roda a engine pesada do Playwright offline para não travar a GUI"""
        try:
            logger.info("=========================================")
            sucesso = run_tasy_reset(user, pwd)
            if sucesso:
                logger.info("✨ PROCESSO FINALIZADO COM SUCESSO! ✨")
            else:
                logger.error("❌ PROCESSO TERMINADO COM FALHA.")
        except Exception as e:
            logger.error(f"Erro Crítico de Exceção: {str(e)}")
        finally:
            self.btn_run.configure(state="normal", text="▶ Executar Redefinição")
            self.ent_user.configure(state="normal")
            self.ent_pass.configure(state="normal")

    def start_automation(self):
        user = self.ent_user.get().strip()
        pwd = self.ent_pass.get()

        if not user or not pwd:
            logger.warning("Por favor, preencha Usuário e a Nova Senha.")
            return

        # Bloquear inputs para não causar double run
        self.btn_run.configure(state="disabled", text="⏳ Rodando (Veja os Logs)...")
        self.ent_user.configure(state="disabled")
        self.ent_pass.configure(state="disabled")

        # Chama a thread
        threading.Thread(target=self.worker_thread, args=(user, pwd), daemon=True).start()

if __name__ == "__main__":
    app = App()
    app.mainloop()
