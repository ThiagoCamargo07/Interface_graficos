
import tkinter as tk
from tkinter import messagebox, filedialog
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# === CONFIGURAÇÕES DE ESTILO (AZUL ESCURO + CIANO TECNOLÓGICO) ===
fonte_titulo = ("Segoe UI", 22, "bold")
fonte_labels = ("Segoe UI", 12)
cor_fundo = "#0f172a"          # Azul escuro
cor_texto = "#E0F7FA"          # Ciano claro
cor_entry = "#1e293b"          # Cinza escuro
cor_botao = "#06b6d4"          # Ciano vivo
cor_hover = "#0891b2"          # Ciano escuro

usuarios_permitidos = ["USUARIO1", "ADMIN"]
senhas_permitidas = ["123456", "admin123"]

def on_enter(e):
    e.widget['background'] = cor_hover

def on_leave(e):
    e.widget['background'] = cor_botao

# === INTERFACE DE LOGIN ===
class Login(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Login - Sistema de Análises")
        self.geometry("400x350")
        self.configure(bg=cor_fundo)
        self.resizable(False, False)
        self.create_widgets()

    # Campos e botões da tela de login
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

        # Validação usuário e senha
        if usuario in usuarios_permitidos:
            if senha in senhas_permitidas:
                messagebox.showinfo("Bem-vindo", "Olá Sr. Thiago!\nBem-vindo ao sistema.")
                self.destroy()
                MenuPrincipal()
            else:
                messagebox.showerror("Error password", "Senha errada, tente novamente.")
        elif usuario == "ADM":
            if senha == "123":
                messagebox.showinfo("Administrador", "Olá, adm\nAcesso autorizado.")
                self.destroy()
                MenuPrincipal()
            else:
                messagebox.showerror("Error password", "Senha errada, tente novamente.")
        else:
            messagebox.showerror("Acesso negado", "Você não possui permissão para acessar esse programa.")


# === MENU PRINCIPAL APÓS LOGIN ===

class MenuPrincipal(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Análises")
        self.geometry("400x300")
        self.configure(bg=cor_fundo)
        self.resizable(False, False)
        self.create_widgets()
        self.mainloop()

    # Botões para escolher tipo de gráfico
    def create_widgets(self):
        
        tk.Label(self, text="Escolha o tipo de gráfico", font=fonte_titulo, bg=cor_fundo, fg=cor_texto).pack(pady=30)
        btn_barra = tk.Button(self, text="Gráfico de Barra", font=fonte_labels, bg=cor_botao, fg=cor_texto, relief="flat", command=self.abrir_grafico_barra)
        btn_barra.pack(pady=15, ipadx=10, ipady=5)
        btn_barra.bind("<Enter>", on_enter)
        btn_barra.bind("<Leave>", on_leave)
        btn_linha = tk.Button(self, text="Gráfico de Linhas", font=fonte_labels, bg=cor_botao, fg=cor_texto, relief="flat", command=self.abrir_grafico_linha)
        btn_linha.pack(pady=15, ipadx=10, ipady=5)
        btn_linha.bind("<Enter>", on_enter)
        btn_linha.bind("<Leave>", on_leave)

    def abrir_grafico_barra(self):
        self.destroy()
        Grafico(tipo="barra")

    def abrir_grafico_linha(self):
        self.destroy()
        Grafico(tipo="linha")

# === TELA PARA GERAR GRÁFICO COM BASE NO EXCEL ===

class Grafico(tk.Tk):
    def __init__(self, tipo="barra"):
        super().__init__()
        self.title(f"Gráfico de {tipo.capitalize()}")
        self.geometry("600x500")
        self.configure(bg=cor_fundo)
        self.resizable(False, False)
        self.df = None
        self.tipo = tipo
        self.create_widgets()
        self.mainloop()

    # Campos para escolher e gerar gráfico a partir de Excel
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
        btn_gerar.pack(pady=20, ipadx=15, ipady=8)
        btn_gerar.bind("<Enter>", on_enter)
        btn_gerar.bind("<Leave>", on_leave)

    def selecionar_arquivo(self):
        file_path = filedialog.askopenfilename(title="Selecione arquivo Excel", filetypes=[("Excel files", "*.xlsx *.xls")])
        if file_path:
            self.entry_arquivo.delete(0, tk.END)
            self.entry_arquivo.insert(0, file_path)

    # Lê o arquivo Excel e chama a função de gráfico apropriada
    def gerar_grafico(self):
      
        caminho = self.entry_arquivo.get()
        if not caminho:
            messagebox.showwarning("Aviso", "Selecione um arquivo Excel.")
            return
        try:
            self.df = pd.read_excel(caminho)
            if self.df.empty:
                messagebox.showerror("Erro", "O arquivo Excel está vazio.")
                return
            if self.df.shape[1] < 2:
                messagebox.showerror("Erro", "O arquivo deve conter pelo menos duas colunas.")
                return
            x = self.df.iloc[:, 0]
            y = self.df.iloc[:, 1]
            if self.tipo == "barra":
                abrir_interface_grafico_barras(x, y, titulo="Gráfico de Barras", xlabel=self.df.columns[0], ylabel=self.df.columns[1])
            else:
                abrir_interface_grafico_linhas(x, y, titulo="Gráfico de Linhas", xlabel=self.df.columns[0], ylabel=self.df.columns[1])
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao ler arquivo:\n{e}")

# === GRÁFICO DE BARRAS COM ESTILO TECNOLÓGICO ===
def abrir_interface_grafico_barras(x, y, titulo="Gráfico de Barras", xlabel="Categoria", ylabel="Valor"):
    janela = tk.Toplevel()
    janela.title(titulo)
    janela.geometry("900x600")
    janela.configure(bg=cor_fundo)
    fig, ax = plt.subplots(figsize=(10, 5))
    bars = ax.bar(x, y, color=cor_botao)
    ax.set_title(titulo, fontsize=16)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.tick_params(axis='x', rotation=45)
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, height, f'{height:.0f}', ha='center', va='bottom', fontsize=10, color='white')
    canvas = FigureCanvasTkAgg(fig, master=janela)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

# === GRÁFICO DE LINHAS COM ESTILO TECNOLÓGICO ===
def abrir_interface_grafico_linhas(x, y, titulo="Gráfico de Linhas", xlabel="Categoria", ylabel="Valor"):
    janela = tk.Toplevel()
    janela.title(titulo)
    janela.geometry("900x600")
    janela.configure(bg=cor_fundo)
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(x, y, marker='o', linestyle='-', color=cor_botao)
    for i, val in enumerate(y):
        ax.text(i, val, f'{val:.0f}', ha='center', va='bottom', fontsize=10, color='white')
    ax.set_title(titulo, fontsize=16)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.tick_params(axis='x', rotation=45)
    canvas = FigureCanvasTkAgg(fig, master=janela)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

# === EXECUÇÃO ===
if __name__ == "__main__":
    app = Login()
    app.mainloop()
