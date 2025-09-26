import os
import shutil
from tkinter import filedialog, messagebox, Canvas, Scrollbar
import fitz
from PIL import Image, ImageTk
from danfePDF import DanfeGenerator

class UserPDF:
    def __init__(self, pdf_frame):
        self.pdf_frame = pdf_frame
        self.temp_pdf_path = None
        self.pdf_document = None
        self.current_page = 0
        self.total_pages = 0
        self.zoom_percent = 100

        self.canvas = Canvas(self.pdf_frame, bg="gray70")
        v_scroll = Scrollbar(self.pdf_frame, orient="vertical", command=self.canvas.yview)
        h_scroll = Scrollbar(self.pdf_frame, orient="horizontal", command=self.canvas.xview)
        self.canvas.configure(yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)

        v_scroll.grid(row=0, column=1, sticky="ns")
        h_scroll.grid(row=1, column=0, sticky="ew")
        self.canvas.grid(row=0, column=0, sticky="nsew")

        self.pdf_frame.grid_rowconfigure(0, weight=1)
        self.pdf_frame.grid_columnconfigure(0, weight=1)
        
        self.canvas_image_item = None
        self.zoom_label_ui = None
        self.page_label_ui = None

    def set_zoom_label(self, label):
        self.zoom_label_ui = label

    def set_page_label(self, label):
        self.page_label_ui = label

    def selecionar_arquivo(self, temp_pdf_path):
        self.temp_pdf_path = temp_pdf_path
        arquivo_xml = filedialog.askopenfilename(
            title="Selecione o arquivo XML",
            filetypes=[("Arquivos XML", "*.xml")]
        )
        if not arquivo_xml:
            return False

        try:
            with open(arquivo_xml, 'rb') as f:
                xml_content = f.read()
            danfe_generator = DanfeGenerator(xml_content)
            danfe_generator.salvaEmPDF(self.temp_pdf_path)
            self.abrir_pdf(self.temp_pdf_path)
            return True
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro ao gerar o DANFE: {e}")
            return False

    def abrir_pdf(self, pdf_path):
        if self.pdf_document:
            self.fechar_pdf()
        
        self.pdf_document = fitz.open(pdf_path)
        self.total_pages = len(self.pdf_document)
        self.current_page = 0
        self.zoom_percent = 100
        self.render_page()

    def render_page(self):
        if not self.pdf_document:
            return
        
        zoom_float = self.zoom_percent / 100.0
        mat = fitz.Matrix(zoom_float, zoom_float)
        page = self.pdf_document.load_page(self.current_page)
        pix = page.get_pixmap(matrix=mat)

        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        self.photo = ImageTk.PhotoImage(image=img)

        if self.canvas_image_item:
            self.canvas.itemconfig(self.canvas_image_item, image=self.photo)
        else:
            self.canvas_image_item = self.canvas.create_image(0, 0, anchor="nw", image=self.photo)

        self.canvas.config(scrollregion=self.canvas.bbox("all"))

        self.atualizar_ui_labels()
        
    def atualizar_ui_labels(self):
        if self.zoom_label_ui:
            self.zoom_label_ui.config(text=f"Zoom: {self.zoom_percent}%")
        if self.page_label_ui and self.total_pages > 0:
            self.page_label_ui.config(text=f"Página: {self.current_page + 1}/{self.total_pages}")
        else:
            self.page_label_ui.config(text="Página: -/-")

    def zoom_in(self):
        if self.pdf_document:
            self.zoom_percent += 20
            self.render_page()

    def zoom_out(self):
        if self.pdf_document and self.zoom_percent >= 40:
            self.zoom_percent -= 20
            self.render_page()
            
    def next_page(self):
        if self.pdf_document and self.current_page < self.total_pages - 1:
            self.current_page += 1
            self.render_page()

    def previous_page(self):
        if self.pdf_document and self.current_page > 0:
            self.current_page -= 1
            self.render_page()

    def salvar_pdf(self):
        if not self.temp_pdf_path or not os.path.exists(self.temp_pdf_path):
            messagebox.showwarning("Aviso", "Nenhum PDF foi gerado para salvar.")
            return
            
        caminho_salvar = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("Arquivos PDF", "*.pdf")]
        )
        if caminho_salvar:
            try:
                shutil.copy2(self.temp_pdf_path, caminho_salvar)
                messagebox.showinfo("Sucesso", f"DANFE salvo com sucesso em:\n{caminho_salvar}")
            except Exception as e:
                messagebox.showerror("Erro", f"Não foi possível salvar o arquivo: {e}")

    def fechar_pdf(self):
        if self.pdf_document:
            self.pdf_document.close()
            self.pdf_document = None