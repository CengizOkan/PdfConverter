"""
    Converts .txt files to PDF format using pure Python (no external libraries).
"""
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../../'))

from sdks.novavision.src.base.component import Component
from sdks.novavision.src.helper.executor import Executor
from components.Package.src.utils.response import build_response
from components.Package.src.models.PackageModel import PackageModel

class Package(Component):
    def __init__(self, request, bootstrap):
        super().__init__(request, bootstrap)
        self.request.model = PackageModel(**(self.request.data))
        self.input_file_id = self.request.get_param("ConfigInputFile")
        self.output_file = None
        self.output_message = {}

    @staticmethod
    def bootstrap(config: dict) -> dict:
        return {}

    def fetch_file_path(self, file_id):
        # Şirket SDK'sına göre dosya yolunu belirle
        return f"/tmp/storage/{file_id}_uhud.txt"

    def convert_to_pdf_pure_python(self, input_path):
        """
        Saf Python ile minimalist bir PDF dosyası oluşturur.
        """
        output_path = input_path.rsplit('.', 1)[0] + ".pdf"
        
        # İçeriği oku
        try:
            with open(input_path, "r", encoding="utf-8") as f:
                lines = f.readlines()
        except:
            lines = ["Dosya icerigi okunamadi."]

        # PDF objelerini manuel olarak oluşturuyoruz
        # BT = Begin Text, ET = End Text, Td = Text Position, Tf = Text Font
        text_content = ""
        y_position = 750 # Sayfanın üstünden başla
        for line in lines:
            clean_line = line.strip().replace("(", "\\(").replace(")", "\\)")
            text_content += f"1 0 0 1 50 {y_position} Tm ({clean_line}) Tj\n"
            y_position -= 15 # Satır aralığı
            if y_position < 50: break # Sayfa sonu sınırı

        # PDF Dosya Yapısı
        pdf_structure = (
            "%PDF-1.1\n"
            "1 0 obj << /Type /Catalog /Pages 2 0 R >> endobj\n"
            "2 0 obj << /Type /Pages /Kids [3 0 R] /Count 1 >> endobj\n"
            "3 0 obj << /Type /Page /Parent 2 0 R /Resources << /Font << /F1 4 0 R >> >> /Contents 5 0 R >> endobj\n"
            "4 0 obj << /Type /Font /Subtype /Type1 /BaseFont /Helvetica >> endobj\n"
            "5 0 obj << /Length {length} >> stream\n"
            "BT\n/F1 12 Tf\n{content}ET\n"
            "endstream\n"
            "endobj\n"
            "xref\n0 6\n0000000000 65535 f\n0000000010 00000 n\n0000000059 00000 n\n0000000116 00000 n\n0000000212 00000 n\n0000000275 00000 n\ntrailer << /Size 6 /Root 1 0 R >>\n"
            "startxref\n450\n%%EOF"
        )

        final_pdf = pdf_structure.format(
            length=len(text_content) + 20,
            content=text_content
        )

        with open(output_path, "w", encoding="latin-1") as f:
            f.write(final_pdf)
            
        return output_path

    def run(self):
        try:
            if not self.input_file_id:
                raise ValueError("Dosya secilmedi.")
            
            # Şemadaki akış: storage -> executor -> web storage
            input_path = self.fetch_file_path(self.input_file_id)
            self.output_file = self.convert_to_pdf_pure_python(input_path)
            
            self.output_message = {
                "status": "Success",
                "message": "Kutuphanesiz PDF donusturme basarili."
            }
        except Exception as e:
            self.output_file = None
            self.output_message = {
                "status": "Error",
                "message": str(e)
            }

        return build_response(context=self)

if "__main__" == __name__:
    Executor(sys.argv[1]).run()