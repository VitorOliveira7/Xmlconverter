from brazilfiscalreport.danfe import Danfe


class DanfeGenerator:
    def __init__(self, xml_content: bytes):
        
        try:
            self.xml_content = xml_content
            self.danfe = Danfe(self.xml_content)
        except Exception as e:
            raise ValueError(f"Erro ao inicializar Danfe: {e}")
        
    def salvaEmPDF(self, output_pdf: str):
        try:
            self.danfe.output(output_pdf)
        except Exception as e:
            raise IOError(f"Erro ao salvar PDF: {e}")