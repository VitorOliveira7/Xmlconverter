
import os
import tkinter as tk
import tempfile
import shutil
from userPDF import UserPDF

print("teste de commit")
class DanfeApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Gerador e Visualizador de DANFE")
        self.geometry("800x700")

        self.temp_dir = tempfile.mkdtemp()
        self.temp_pdf_path = os.path.join(self.temp_dir, "danfe_temp.pdf")

        self.frame_botoes = tk.Frame(self)
        self.frame_botoes.pack(pady=10)

        self.pdf_frame = tk.Frame(self)
        self.pdf_frame.pack(pady=10, expand=True, fill='both')

        self.userPDF = UserPDF(self.pdf_frame, self.temp_pdf_path)

        # Botões
        self.select_button = tk.Button(
            self.frame_botoes, text="Selecionar Arquivo XML",
            command=lambda: self.userPDF.selecionar_arquivo(self.save_button)
        )
        self.select_button.pack(side=tk.LEFT, padx=5)

        self.save_button = tk.Button(
            self.frame_botoes, text="Salvar PDF Como...",
            command=self.userPDF.salvar_pdf, state=tk.DISABLED
        )
        self.save_button.pack(side=tk.LEFT, padx=5)



    def on_closing(self):
        if self.temp_dir and os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
        self.destroy()


if __name__ == "__main__":
    app = DanfeApp()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()
