import tkinter as tk
from tkinter import messagebox, filedialog
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os
import sys

# PyInstaller cria uma pasta temporária e armazena o caminho em _MEIPASS
def resource_path(relative_path):
    """Retorna o caminho absoluto do recurso, mesmo quando empacotado com PyInstaller."""
    try:
        
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


# === CONFIGURAÇÕES DE ESTILO (AZUL ESCURO + CIANO TECNOLÓGICO) ===
fonte_titulo = ("Segoe UI", 22, "bold")
fonte_labels = ("Segoe UI", 12)
cor_fundo = "#0f172a"          # Azul escuro
cor_texto = "#E0F7FA"          # Ciano claro
cor_entry = "#1e293b"          # Cinza escuro
cor_botao = "#06b6d4"          # Ciano vivo
cor_hover = "#0891b2"          # Ciano escuro

def on_enter(e):
    e.widget['background'] = cor_hover

def on_leave(e):
    e.widget['background'] = cor_botao

# === INTERFACE DE LOGIN ===
class Login(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Login - Sistema de Análises")
        self.iconbitmap(resource_path("analise.ico")) # Ícone personalizado
        self.geometry("400x350")
        self.configure(bg=cor_fundo)
        self.resizable(False, False)
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="LOGIN", font=fonte_titulo, bg=cor_fundo, fg=cor_texto).pack(pady=20)
        tk.Label(self, text="Usuário:", font=fonte_labels, bg=cor_fundo, fg=cor_texto).pack(anchor="w", padx=40)
        self.entry_usuario = tk.Entry(self, bg=cor_entry, fg=cor_texto, insertbackground=cor_texto, relief="flat", font=fonte_labels)
        self.entry_usuario.pack(fill="x", padx=40, pady=5)
        tk.Label(self, text="Senha:", font=fonte_labels, bg=cor_fundo, fg=cor_texto).pack(anchor="w", padx=40)
        self.entry_senha = tk.Entry(self, show="*", bg=cor_entry, fg=cor_texto, insertbackground=cor_texto, relief="flat", font=fonte_labels)
        self.entry_senha.pack(fill="x", padx=40, pady=5)
        btn_entrar = tk.Button(self, text="Entrar", font=fonte_labels, bg=cor_botao, fg=cor_texto, relief="flat", command=self.validar_usuario)
        btn_entrar.pack(pady=30, ipadx=10, ipady=5)
        btn_entrar.bind("<Enter>", on_enter)
        btn_entrar.bind("<Leave>", on_leave)

    def validar_usuario(self):
        usuario = self.entry_usuario.get().strip().lower().upper()
        senha = self.entry_senha.get()

        usuarios_permitidos = ["TFCAMARGO", "TFCAMARGO@MERCADOCAR.COM.BR", "THIFCAMARGO04@GMAIL.COM"]
        senhas_permitidas =["THIago070404", "THI070404"]

        if usuario in usuarios_permitidos and senha in senhas_permitidas:
            messagebox.showinfo("Bem-vindo", "Olá Sr. Thiago!\nBem-vindo ao sistema.")
            self.destroy()
            MenuPrincipal()
        elif usuario == "ADM" and senha == "123":
            messagebox.showinfo("Administrador", "Olá, adm\nAcesso autorizado.")
            self.destroy()
            MenuPrincipal()
        else:
            messagebox.showerror("Acesso negado", "Usuário ou senha inválidos.")

# === MENU PRINCIPAL APÓS LOGIN ===
class MenuPrincipal(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Análises")
        self.geometry("400x350")
        self.configure(bg=cor_fundo)
        self.resizable(False, False)
        self.create_widgets()
        self.mainloop()

    def create_widgets(self):
        tk.Label(self, text="Escolha o tipo de gráfico", font=fonte_titulo, bg=cor_fundo, fg=cor_texto).pack(pady=30)

        btn_barra = tk.Button(self, text="Gráfico de Barra", font=fonte_labels, bg=cor_botao, fg=cor_texto, relief="flat", command=self.abrir_grafico_barra)
        btn_barra.pack(pady=10, ipadx=10, ipady=5)
        btn_barra.bind("<Enter>", on_enter)
        btn_barra.bind("<Leave>", on_leave)

        btn_linha = tk.Button(self, text="Gráfico de Linhas", font=fonte_labels, bg=cor_botao, fg=cor_texto, relief="flat", command=self.abrir_grafico_linha)
        btn_linha.pack(pady=10, ipadx=10, ipady=5)
        btn_linha.bind("<Enter>", on_enter)
        btn_linha.bind("<Leave>", on_leave)

        btn_dashboard = tk.Button(self, text="Dashboard Completo", font=fonte_labels, bg=cor_botao, fg=cor_texto, relief="flat", command=self.abrir_dashboard)
        btn_dashboard.pack(pady=10, ipadx=10, ipady=5)
        btn_dashboard.bind("<Enter>", on_enter)
        btn_dashboard.bind("<Leave>", on_leave)

    def abrir_grafico_barra(self):
        self.withdraw()
        Grafico(self, tipo="barra")

    def abrir_grafico_linha(self):
        self.withdraw()
        Grafico(self, tipo="linha")

    def abrir_dashboard(self):
        self.withdraw()
        abrir_dashboard_completo(self)

# === INTERFACE DE GRÁFICO PADRÃO ===
class Grafico(tk.Toplevel):
    def __init__(self, master, tipo="barra"):
        super().__init__(master)
        self.master = master
        self.title(f"Gráfico de {tipo.capitalize()}")
        self.geometry("600x500")
        self.configure(bg=cor_fundo)
        self.resizable(False, False)
        self.df = None
        self.tipo = tipo
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text=f"Gráfico de {self.tipo.capitalize()}", font=fonte_titulo, bg=cor_fundo, fg=cor_texto).pack(pady=20)
        frame = tk.Frame(self, bg=cor_fundo)
        frame.pack(pady=10)
        tk.Label(frame, text="Selecione o arquivo Excel:", font=fonte_labels, bg=cor_fundo, fg=cor_texto).grid(row=0, column=0, sticky="w")
        self.entry_arquivo = tk.Entry(frame, width=40, bg=cor_entry, fg=cor_texto, relief="flat", font=fonte_labels)
        self.entry_arquivo.grid(row=0, column=1, padx=10)
        btn_browse = tk.Button(frame, text="Selecionar", bg=cor_botao, fg=cor_texto, relief="flat", command=self.selecionar_arquivo)
        btn_browse.grid(row=0, column=2)
        btn_browse.bind("<Enter>", on_enter)
        btn_browse.bind("<Leave>", on_leave)

        btn_gerar = tk.Button(self, text="Gerar Gráfico", bg=cor_botao, fg=cor_texto, relief="flat", font=fonte_labels, command=self.gerar_grafico)
        btn_gerar.pack(pady=10, ipadx=15, ipady=8)
        btn_gerar.bind("<Enter>", on_enter)
        btn_gerar.bind("<Leave>", on_leave)

        btn_voltar = tk.Button(self, text="← Voltar ao Menu", font=fonte_labels, bg=cor_botao, fg=cor_texto, relief="flat", command=self.voltar_para_menu)
        btn_voltar.pack(pady=10)
        btn_voltar.bind("<Enter>", on_enter)
        btn_voltar.bind("<Leave>", on_leave)

    def selecionar_arquivo(self):
        file_path = filedialog.askopenfilename(title="Selecione arquivo Excel", filetypes=[("Excel files", "*.xlsx *.xls")])
        if file_path:
            self.entry_arquivo.delete(0, tk.END)
            self.entry_arquivo.insert(0, file_path)

    def gerar_grafico(self):
        caminho = self.entry_arquivo.get()
        if not caminho:
            messagebox.showwarning("Aviso", "Selecione um arquivo Excel.")
            return
        try:
            self.df = pd.read_excel(caminho)
            if self.df.empty or self.df.shape[1] < 2:
                messagebox.showerror("Erro", "O arquivo deve conter pelo menos duas colunas.")
                return
            x = self.df.iloc[:, 0]
            y = self.df.iloc[:, 1]
            if self.tipo == "barra":
                abrir_interface_grafico_barras(x, y)
            else:
                abrir_interface_grafico_linhas(x, y)
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao ler arquivo:\n{e}")

    def voltar_para_menu(self):
        self.destroy()
        self.master.deiconify()

# === FUNÇÕES DE GRÁFICOS ===
def abrir_interface_grafico_barras(x, y):
    janela = tk.Toplevel()
    janela.title("Gráfico de Barras")
    janela.geometry("900x600")
    janela.configure(bg=cor_fundo)
    fig, ax = plt.subplots(figsize=(10, 5))
    bars = ax.bar(x, y, color=cor_botao)
    ax.set_title("Gráfico de Barras")
    ax.set_xlabel("Categoria")
    ax.set_ylabel("Valor")
    ax.tick_params(axis='x', rotation=45)
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, height, f'{height:.0f}', ha='center', va='bottom', fontsize=10, color='white')
    canvas = FigureCanvasTkAgg(fig, master=janela)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

def abrir_interface_grafico_linhas(x, y):
    janela = tk.Toplevel()
    janela.title("Gráfico de Linhas")
    janela.geometry("900x600")
    janela.configure(bg=cor_fundo)
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(x, y, marker='o', linestyle='-', color=cor_botao)
    for i, val in enumerate(y):
        ax.text(i, val, f'{val:.0f}', ha='center', va='bottom', fontsize=10, color='white')
    ax.set_title("Gráfico de Linhas")
    ax.set_xlabel("Categoria")
    ax.set_ylabel("Valor")
    ax.tick_params(axis='x', rotation=45)
    canvas = FigureCanvasTkAgg(fig, master=janela)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

# === DASHBOARD ===
def abrir_dashboard_completo(janela_anterior):
    caminho = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx *.xls")])
    if not caminho:
        janela_anterior.deiconify()
        return
    try:
        df = pd.read_excel(caminho)
        if df.shape[1] < 2:
            messagebox.showerror("Erro", "O arquivo deve conter pelo menos duas colunas.")
            janela_anterior.deiconify()
            return
        janela_anterior.withdraw()
        janela = tk.Toplevel()
        janela.title("Dashboard Completo")
        janela.geometry("1200x700")
        janela.configure(bg=cor_fundo)

        col_y = df.columns[1]
        stats = {
            "Média": df[col_y].mean(),
            "Mediana": df[col_y].median(),
            "Máximo": df[col_y].max(),
            "Mínimo": df[col_y].min(),
            "Soma": df[col_y].sum(),
            "Contagem": df[col_y].count()
        }

        frame_cards = tk.Frame(janela, bg=cor_fundo)
        frame_cards.pack(pady=20)

        for i, (nome, valor) in enumerate(stats.items()):
            card = tk.Frame(frame_cards, bg=cor_entry, padx=20, pady=10)
            card.grid(row=0, column=i, padx=10)
            tk.Label(card, text=nome, font=("Segoe UI", 12, "bold"), fg=cor_botao, bg=cor_entry).pack()
            tk.Label(card, text=f"{valor:.2f}", font=("Segoe UI", 14), fg=cor_texto, bg=cor_entry).pack()

        fig, axs = plt.subplots(1, 2, figsize=(12, 5))
        fig.patch.set_facecolor(cor_fundo)
        axs[0].bar(df[df.columns[0]], df[df.columns[1]], color=cor_botao)
        axs[0].set_title("Gráfico de Barras", color='white')
        axs[0].tick_params(axis='x', colors='white', rotation=45)
        axs[0].tick_params(axis='y', colors='white')
        axs[0].set_facecolor(cor_entry)
        axs[1].plot(df[df.columns[0]], df[df.columns[1]], color='lime', marker='o')
        axs[1].set_title("Gráfico de Linhas", color='white')
        axs[1].tick_params(axis='x', colors='white', rotation=45)
        axs[1].tick_params(axis='y', colors='white')
        axs[1].set_facecolor(cor_entry)

        canvas = FigureCanvasTkAgg(fig, master=janela)
        canvas.draw()
        canvas.get_tk_widget().pack(pady=10)

        btn_voltar = tk.Button(janela, text="← Voltar ao Menu", font=fonte_labels, bg=cor_botao, fg=cor_texto, relief="flat", command=lambda: voltar_para_menu_dashboard(janela, janela_anterior))
        btn_voltar.pack(pady=10)
        btn_voltar.bind("<Enter>", on_enter)
        btn_voltar.bind("<Leave>", on_leave)

    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao abrir arquivo:\n{e}")
        janela_anterior.deiconify()


def voltar_para_menu_dashboard(janela_atual, janela_menu):
    janela_atual.destroy()
    janela_menu.deiconify()

# === EXECUÇÃO ===
if __name__ == "__main__":
    app = Login()
    app.mainloop()