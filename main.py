import os
import sys  
import tkinter as tk
import tempfile
import shutil
from userPDF import UserPDF

def resource_path(relative_path):

    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class DanfeApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Gerador e Visualizador de DANFE")
        
        try:
        
            icon_path = resource_path("icone.png")
            self.icon_image = tk.PhotoImage(file=icon_path)
            self.iconphoto(True, self.icon_image)
        except tk.TclError:
            print("Aviso: Não foi possível carregar o ícone da aplicação.")
        
        self.geometry("850x800")
        
        self.temp_dir = tempfile.mkdtemp()
        self.temp_pdf_path = os.path.join(self.temp_dir, "danfe_temp.pdf")

        self.frame_botoes = tk.Frame(self)
        self.frame_botoes.pack(pady=5, padx=10, fill='x')

        self.pdf_frame = tk.Frame(self, bg="gray70")
        self.pdf_frame.pack(pady=10, padx=10, expand=True, fill='both')

        self.userPDF = UserPDF(self.pdf_frame)

        botoes_inner_frame = tk.Frame(self.frame_botoes)

        self.select_button = tk.Button(botoes_inner_frame, text="Selecionar XML", command=self.selecionar_e_exibir)
        self.select_button.pack(side=tk.LEFT, padx=(0, 5))

        self.save_button = tk.Button(botoes_inner_frame, text="Salvar PDF", command=self.userPDF.salvar_pdf, state=tk.DISABLED)
        self.save_button.pack(side=tk.LEFT, padx=5)
        
        separator = tk.Frame(botoes_inner_frame, width=20)
        separator.pack(side=tk.LEFT)

        self.zoom_out_button = tk.Button(botoes_inner_frame, text="-", command=self.userPDF.zoom_out, state=tk.DISABLED, width=3)
        self.zoom_out_button.pack(side=tk.LEFT, padx=(0, 2))
        
        self.zoom_label = tk.Label(botoes_inner_frame, text="Zoom: --%")
        self.userPDF.set_zoom_label(self.zoom_label)
        self.zoom_label.pack(side=tk.LEFT, padx=2)

        self.zoom_in_button = tk.Button(botoes_inner_frame, text="+", command=self.userPDF.zoom_in, state=tk.DISABLED, width=3)
        self.zoom_in_button.pack(side=tk.LEFT, padx=(2, 5))
        
        separator2 = tk.Frame(botoes_inner_frame, width=20)
        separator2.pack(side=tk.LEFT)
        
        self.prev_page_button = tk.Button(botoes_inner_frame, text="< Ant", command=self.userPDF.previous_page, state=tk.DISABLED)
        self.prev_page_button.pack(side=tk.LEFT, padx=2)

        self.page_label = tk.Label(botoes_inner_frame, text="Página: -/-")
        self.userPDF.set_page_label(self.page_label)
        self.page_label.pack(side=tk.LEFT, padx=2)
        
        self.next_page_button = tk.Button(botoes_inner_frame, text="Próx >", command=self.userPDF.next_page, state=tk.DISABLED)
        self.next_page_button.pack(side=tk.LEFT, padx=2)

        botoes_inner_frame.pack()

    def selecionar_e_exibir(self):
        pdf_gerado = self.userPDF.selecionar_arquivo(self.temp_pdf_path)
        if pdf_gerado:
            self.save_button.config(state="normal")
            self.zoom_in_button.config(state="normal")
            self.zoom_out_button.config(state="normal")
            self.prev_page_button.config(state="normal")
            self.next_page_button.config(state="normal")

    def on_closing(self):
        if self.temp_dir and os.path.exists(self.temp_dir):
            self.userPDF.fechar_pdf()
            shutil.rmtree(self.temp_dir)
        self.destroy()

if __name__ == "__main__":
    app = DanfeApp()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()