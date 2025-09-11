import os
import shutil
from tkinter import filedialog, messagebox
from tkPDFViewer2 import tkPDFViewer as pdf
from danfePDF import DanfeGenerator


class UserPDF:
    def __init__(self, pdf_frame, temp_pdf_path):
        self.pdf_frame = pdf_frame
        self.temp_pdf_path = temp_pdf_path
        self.viewer = pdf.ShowPdf()
        self.pdf_viewer = None

    def selecionar_arquivo(self, save_button):
        """Seleciona o XML, gera o DANFE em PDF e exibe na tela."""
        arquivo_xml = filedialog.askopenfilename(
            title="Selecione o arquivo XML",
            filetypes=[("Arquivos XML", "*.xml")]
        )

        if arquivo_xml:
            try:
                with open(arquivo_xml, 'rb') as f:
                    xml_content = f.read()

                danfe_generator = DanfeGenerator(xml_content)
                danfe_generator.salvaEmPDF(self.temp_pdf_path)

                self.exibir_pdf(self.temp_pdf_path)
                save_button.config(state="normal")

            except Exception as e:
                messagebox.showerror("Erro", f"Ocorreu um erro ao gerar o DANFE: {e}")

    def exibir_pdf(self, pdf_path):
        """Exibe o PDF no frame da interface."""
        self.viewer.img_object_li.clear()

        if self.pdf_viewer:
            self.pdf_viewer.destroy()

        self.pdf_viewer = self.viewer.pdf_view(
            self.pdf_frame,
            pdf_location=pdf_path,
            bar=True,
            width=100, height=120
        )
        self.pdf_viewer.pack(expand=True, fill='both')

    def salvar_pdf(self):
        """Permite salvar o PDF gerado em outro local."""
        if self.temp_pdf_path and os.path.exists(self.temp_pdf_path):
            caminho_salvar = filedialog.asksaveasfilename(
                defaultextension=".pdf",
                filetypes=[("Arquivos PDF", "*.pdf")],
                title="Salvar DANFE como..."
            )
            if caminho_salvar:
                try:
                    shutil.copy2(self.temp_pdf_path, caminho_salvar)
                    messagebox.showinfo("Sucesso", f"DANFE salvo com sucesso em:\n{caminho_salvar}")
                except Exception as e:
                    messagebox.showerror("Erro", f"Não foi possível salvar o arquivo: {e}")

    def limpar_pdf(self, save_button):
        """Remove o PDF da tela."""
        if self.pdf_viewer:
            self.viewer.img_object_li.clear()
            self.pdf_viewer.destroy()
            self.pdf_viewer = None
            save_button.config(state="disabled")
