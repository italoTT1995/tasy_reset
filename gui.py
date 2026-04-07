import customtkinter as ctk
import threading
from utils.logger import logger
from services.tasy_service import run_tasy_reset

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Tasy Password Reset v1.0")
        self.geometry("450x780")
        self.resizable(False, False)

        # Header
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.pack(pady=16, padx=20, fill="x")
        self.lbl_title = ctk.CTkLabel(self.header_frame, text="Tasy EMR\nReset Automático", font=ctk.CTkFont(size=24, weight="bold"))
        self.lbl_title.pack()

        # ── Seção: Seu Acesso (Operador T.I) ───────────────────────────
        self.frame_admin = ctk.CTkFrame(self)
        self.frame_admin.pack(pady=(0, 10), padx=20, fill="x")

        self.lbl_admin_title = ctk.CTkLabel(self.frame_admin, text="🔑  Seu Acesso (Operador T.I)", font=ctk.CTkFont(weight="bold"))
        self.lbl_admin_title.pack(pady=(10, 4), padx=20, anchor="w")

        self.lbl_admin_user = ctk.CTkLabel(self.frame_admin, text="Seu usuário:")
        self.lbl_admin_user.pack(pady=(4, 0), padx=20, anchor="w")
        self.ent_admin_user = ctk.CTkEntry(self.frame_admin, placeholder_text="Ex: seunome", width=300)
        self.ent_admin_user.pack(pady=(0, 8), padx=20)

        self.lbl_admin_pass = ctk.CTkLabel(self.frame_admin, text="Sua senha:")
        self.lbl_admin_pass.pack(pady=(0, 0), padx=20, anchor="w")
        self.ent_admin_pass = ctk.CTkEntry(self.frame_admin, placeholder_text="Sua senha do Tasy", width=300, show="*")
        self.ent_admin_pass.pack(pady=(0, 14), padx=20)

        # ── Seção: Usuário Alvo (Reset) ──────────────────────────────────
        self.input_frame = ctk.CTkFrame(self)
        self.input_frame.pack(pady=10, padx=20, fill="x")

        self.lbl_alvo = ctk.CTkLabel(self.input_frame, text="🎯  Redefinição de Senha", font=ctk.CTkFont(weight="bold"))
        self.lbl_alvo.pack(pady=(10, 4), padx=20, anchor="w")

        self.lbl_user = ctk.CTkLabel(self.input_frame, text="Login do usuário alvo:")
        self.lbl_user.pack(pady=(4, 0), padx=20, anchor="w")
        self.ent_user = ctk.CTkEntry(self.input_frame, placeholder_text="Ex: itlsilva", width=300)
        self.ent_user.pack(pady=(0, 8), padx=20)

        self.lbl_pass = ctk.CTkLabel(self.input_frame, text="Nova senha:")
        self.lbl_pass.pack(pady=(0, 0), padx=20, anchor="w")
        self.ent_pass = ctk.CTkEntry(self.input_frame, placeholder_text="Digite a nova senha", width=300, show="*")
        self.ent_pass.pack(pady=(0, 14), padx=20)

        # Botão
        self.btn_run = ctk.CTkButton(self, text="▶ Executar Redefinição", height=40, font=ctk.CTkFont(weight="bold"), command=self.start_automation)
        self.btn_run.pack(pady=10, padx=20, fill="x")

        # Barra de progresso
        self.progress_bar = ctk.CTkProgressBar(self, width=400, height=12, mode="indeterminate")
        self.progress_bar.pack(pady=(0, 4), padx=20, fill="x")
        self.progress_bar.set(0)

        self.lbl_status = ctk.CTkLabel(self, text="Aguardando execução...", font=ctk.CTkFont(size=11), text_color="gray")
        self.lbl_status.pack(pady=(0, 6))

        # Terminal de logs
        self.terminal_label = ctk.CTkLabel(self, text="Terminal de Execução:", font=ctk.CTkFont(size=12, slant="italic"))
        self.terminal_label.pack(pady=(6, 0), padx=20, anchor="w")

        self.log_box = ctk.CTkTextbox(self, width=400, height=140, state="disabled", fg_color="#121212", text_color="#00FF00")
        self.log_box.pack(pady=(5, 16), padx=20, fill="both", expand=True)

        logger.add(self.log_to_gui, format="{time:HH:mm:ss} | {level} | {message}")

    def log_to_gui(self, message):
        self.log_box.configure(state="normal")
        self.log_box.insert("end", message)
        self.log_box.see("end")
        self.log_box.configure(state="disabled")

    def worker_thread(self, admin_user, admin_pwd, user, pwd):
        try:
            logger.info("=========================================")
            sucesso = run_tasy_reset(user, pwd, admin_user=admin_user, admin_password=admin_pwd)
            if sucesso:
                logger.info("✨ PROCESSO FINALIZADO COM SUCESSO! ✨")
                self._set_status("✅ Concluído com sucesso!", "#2ecc71")
            else:
                logger.error("❌ PROCESSO TERMINADO COM FALHA.")
                self._set_status("❌ Falha na execução. Veja os logs.", "#e74c3c")
        except Exception as e:
            logger.error(f"Erro Crítico: {str(e)}")
            self._set_status("❌ Erro crítico. Veja os logs.", "#e74c3c")
        finally:
            self.progress_bar.stop()
            self.progress_bar.set(1 if "Concluído" in self.lbl_status.cget("text") else 0)
            self._set_inputs_state("normal")
            self.btn_run.configure(state="normal", text="▶ Executar Redefinição")

    def _set_status(self, texto, cor):
        self.lbl_status.configure(text=texto, text_color=cor)

    def _set_inputs_state(self, state):
        self.ent_admin_user.configure(state=state)
        self.ent_admin_pass.configure(state=state)
        self.ent_user.configure(state=state)
        self.ent_pass.configure(state=state)

    def start_automation(self):
        admin_user = self.ent_admin_user.get().strip()
        admin_pwd  = self.ent_admin_pass.get()
        user       = self.ent_user.get().strip()
        pwd        = self.ent_pass.get()

        if not admin_user or not admin_pwd or not user or not pwd:
            logger.warning("Preencha todos os campos (Seu acesso e Reset).")
            return

        self._set_status("🔄 Robô em execução...", "#3498db")
        self.progress_bar.set(0)
        self.progress_bar.start()
        
        self._set_inputs_state("disabled")
        self.btn_run.configure(state="disabled", text="⏳ Rodando (Veja os Logs)...")

        threading.Thread(target=self.worker_thread, args=(admin_user, admin_pwd, user, pwd), daemon=True).start()

if __name__ == "__main__":
    app = App()
    app.mainloop()
