import os
import webbrowser
import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox

from config import DIFFICULTIES, WOW_CLASSES, CLASS_COLORS, TRANSLATIONS
from api import APIClient

def load_env():
    """Carrega credenciais do arquivo .env se existir."""
    env_path = os.path.join(os.path.dirname(__file__), ".env")
    env = {}
    if os.path.exists(env_path):
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, _, value = line.partition("=")
                    env[key.strip()] = value.strip()
    return env

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("WoW WCL Talent Fetcher")
        self.geometry("650x820")

        self.api_client = None
        self.difficulties = DIFFICULTIES
        self.wow_classes = WOW_CLASSES
        self.class_colors = CLASS_COLORS
        self.translations = TRANSLATIONS
        
        self.zones = []
        self.current_lang = "en"
        
        # Carregar credenciais do .env se existir
        env = load_env()
        self._env_cid = env.get("WCL_CLIENT_ID", "")
        self._env_sec = env.get("WCL_CLIENT_SECRET", "")
        
        # --- Top Bar (Language Selector) ---
        self.frame_top = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_top.pack(fill="x", padx=20, pady=(10, 0))
        
        self.lang_menu = ctk.CTkOptionMenu(
            self.frame_top, 
            values=["English", "Português"],
            command=self.change_language,
            width=120
        )
        self.lang_menu.pack(side="right")
        self.lang_menu.set("English")

        # --- Frame 1: API Credentials (oculto se .env existir) ---
        self.frame_api = ctk.CTkFrame(self)
        self.frame_api.pack(pady=(10, 0), padx=20, fill="x")
        
        self.lbl_api = ctk.CTkLabel(self.frame_api, text=self.translations[self.current_lang]["api_setup"], font=("Arial", 14, "bold"))
        self.lbl_api.pack(pady=(8, 4))
        
        self.entry_cid = ctk.CTkEntry(self.frame_api, placeholder_text=self.translations[self.current_lang]["client_id"], width=400)
        self.entry_cid.pack(pady=3)
        
        self.entry_sec = ctk.CTkEntry(self.frame_api, placeholder_text=self.translations[self.current_lang]["client_secret"], width=400, show="*")
        self.entry_sec.pack(pady=(3, 8))
        
        # Pré-preencher se .env existir e esconder o frame
        if self._env_cid and self._env_sec:
            self.entry_cid.insert(0, self._env_cid)
            self.entry_sec.insert(0, self._env_sec)
            self.frame_api.pack_forget()

        # --- Frame 2: Character Config ---
        self.frame_char = ctk.CTkFrame(self)
        self.frame_char.pack(pady=10, padx=20, fill="x")
        
        self.lbl_char = ctk.CTkLabel(self.frame_char, text=self.translations[self.current_lang]["char_setup"], font=("Arial", 16, "bold"))
        self.lbl_char.pack(pady=(10, 0))

        # Dropdowns side-by-side
        self.dropdown_frame = ctk.CTkFrame(self.frame_char, fg_color="transparent")
        self.dropdown_frame.pack(pady=10)

        self.class_var = ctk.StringVar(value="Mage")
        self.class_menu = ctk.CTkOptionMenu(self.dropdown_frame, variable=self.class_var, values=list(self.wow_classes.keys()), command=self.update_specs)
        self.class_menu.pack(side="left", padx=10)
        
        self.spec_var = ctk.StringVar(value="Fire")
        self.spec_menu = ctk.CTkOptionMenu(self.dropdown_frame, variable=self.spec_var, values=self.wow_classes["Mage"])
        self.spec_menu.pack(side="left", padx=10)
        
        self.diff_var = ctk.StringVar(value="Heroic")
        self.diff_menu = ctk.CTkOptionMenu(self.dropdown_frame, variable=self.diff_var, values=list(self.difficulties.keys()))
        self.diff_menu.pack(side="left", padx=10)

        self.connect_btn = ctk.CTkButton(self.frame_char, text=self.translations[self.current_lang]["connect_btn"], command=self.on_connect)
        self.connect_btn.pack(pady=(10, 20))

        self.frame_list = ctk.CTkScrollableFrame(self, label_text=self.translations[self.current_lang]["raids_title"])
        self.frame_list.pack(pady=10, padx=20, fill="both", expand=True)

        # Result string
        self.result_textbox = ctk.CTkTextbox(self, height=120)
        self.result_textbox.pack(pady=10, padx=20, fill="x")

        # Log link button
        self.link_button = ctk.CTkButton(self, text=self.translations[self.current_lang]["open_log"], command=self.open_log, state="disabled", fg_color="gray")
        self.link_button.pack(pady=5, padx=20)
        
    def change_language(self, language_choice):
        self.current_lang = "en" if language_choice == "English" else "pt"
        
        # O Update na UI requer que nós atualizemos os placeholders de textos
        self.lbl_char.configure(text=self.translations[self.current_lang]["char_setup"])
        self.connect_btn.configure(text=self.translations[self.current_lang]["connect_btn"])
        self.frame_list.configure(label_text=self.translations[self.current_lang]["raids_title"])
        self.link_button.configure(text=self.translations[self.current_lang]["open_log"])
        
        # Redraw
        self.update()

    def open_log(self):
        if hasattr(self, 'current_url') and self.current_url:
            webbrowser.open_new(self.current_url)

    def update_specs(self, selected_class):
        specs = self.wow_classes.get(selected_class, [])
        self.spec_menu.configure(values=specs)
        if specs:
            self.spec_var.set(specs[0])

    def on_connect(self):
        cid = self.entry_cid.get().strip()
        sec = self.entry_sec.get().strip()
        
        if not cid or not sec:
            messagebox.showerror("Erro", self.translations[self.current_lang]["cred_err"])
            return
        
        self.api_client = APIClient(cid, sec)
        
        # Limpar a lista anterior
        for widget in self.frame_list.winfo_children():
            widget.destroy()
            
        self.result_textbox.delete("1.0", "end")
        self.result_textbox.insert("1.0", self.translations[self.current_lang]["auth_msg"])
        self.update()
        
        try:
            self.zones = self.api_client.get_latest_zones()
            self.result_textbox.delete("1.0", "end")
            self.result_textbox.insert("1.0", f"Conexão estabelecida! {len(self.zones)} zonas/raides recentes carregadas.\nSelecione seu encontro acima para puxar os talentos.")
            
            for zone in self.zones:
                zone_label = ctk.CTkLabel(self.frame_list, text=f"🔥 {zone['name']} 🔥", font=("Arial", 16, "bold"), text_color="#F3A010")
                zone_label.pack(pady=(15, 5), anchor="center")
                
                for encounter in zone['encounters']:
                    btn = ctk.CTkButton(self.frame_list, text=encounter['name'], fg_color="#2B2B2B", hover_color="#3B3B3B",
                                        command=lambda e_id=encounter['id'], e_name=encounter['name']: self.on_encounter_click(e_id, e_name))
                    btn.pack(pady=3, padx=20, anchor="center", fill="x")
                    
        except Exception as e:
            self.result_textbox.delete("1.0", "end")
            self.result_textbox.insert("1.0", f"Erro crítico na comunicação com WCL: {str(e)}")

    def on_encounter_click(self, encounter_id, encounter_name):
        cls = self.class_var.get().strip()
        spc = self.spec_var.get().strip()
        diff_name = self.diff_var.get()
        diff_id = self.difficulties.get(diff_name, 4)
        
        if not cls or not spc:
            messagebox.showerror("Erro", "Preencha a Classe e Especialização (ex: Warlock, Demonology) antes de clicar.")
            return

        self.result_textbox.delete("1.0", "end")
        self.result_textbox.insert("1.0", self.translations[self.current_lang]["search_msg"].format(cls, spc, encounter_name, diff_name))
        self.link_button.configure(state="disabled", fg_color="gray")
        self.update()
        
        try:
            top_player, api_error = self.api_client.fetch_top_talents(encounter_id, cls, spc, diff_id)
            if api_error:
                self.result_textbox.delete("1.0", "end")
                self.result_textbox.insert("end", self.translations[self.current_lang]["fetch_err"].format(api_error))
                return
            elif not top_player:
                self.result_textbox.delete("1.0", "end")
                self.result_textbox.insert("end", self.translations[self.current_lang]["rank_err"])
                return
                
            name = top_player.get('name')
            amount = top_player.get('amount')
            report_code = top_player.get('report', {}).get('code')
            fight_id = top_player.get('report', {}).get('fightID')
            actor_id, a_err = self.api_client.fetch_actor_id(report_code, name)
            
            if actor_id:
                url = f"https://www.warcraftlogs.com/reports/{report_code}#fight={fight_id}&type=summary&source={actor_id}"
                talents = "🔗 Link Direto Gerado com Sucesso!\n\n1. Clique no botão azul 'Acessar Log Completo' abaixo.\n2. O Warcraft Logs vai abrir diretamente nos talentos deste jogador.\n3. Basta clicar no botão 'Copy Talent String' no site da WCL!"
            else:
                url = f"https://www.warcraftlogs.com/reports/{report_code}#fight={fight_id}&type=summary"
                talents = self.translations[self.current_lang]["talents_err"] + f"\n(Erro ao isolar jogador: {a_err})"
                
            formatted_amount = f"{float(amount):,.1f}" if amount else "N/A"
            
            c_color = self.class_colors.get(cls, "#FFFFFF")
            self.result_textbox.tag_config("color_class", foreground=c_color)
            self.result_textbox.tag_config("color_dmg", foreground="#a6ff4d")
            
            self.result_textbox.delete("1.0", "end")
            
            self.result_textbox.insert("end", "===== RANK 1 =====\n")
            self.result_textbox.insert("end", self.translations[self.current_lang]["player"])
            self.result_textbox.insert("end", f"{name}", "color_class")
            self.result_textbox.insert("end", self.translations[self.current_lang]["throughput"])
            self.result_textbox.insert("end", f"{formatted_amount}\n\n", "color_dmg")
            
            self.result_textbox.insert("end", f"{self.translations[self.current_lang]['talent_header']}\n{talents}\n======================================")

            self.current_url = url
            self.link_button.configure(state="normal", fg_color="#1F6AA5")
            
        except Exception as e:
            self.result_textbox.delete("1.0", "end")
            self.result_textbox.insert("end", f"Erro: {str(e)}")

if __name__ == "__main__":
    app = App()
    app.mainloop()
