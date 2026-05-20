import os
import sys
from datetime import datetime

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../../'))

from sdks.novavision.src.base.component import Component
from sdks.novavision.src.helper.executor import Executor
from components.Package.src.utils.response import build_response
from components.Package.src.models.PackageModel import PackageModel

try:
    from fpdf import FPDF
except ImportError:
    FPDF = None

class Package(Component):
    def __init__(self, request, bootstrap):
        super().__init__(request, bootstrap)
        self.request.model = PackageModel(**(self.request.data))
        
        try:
            # Data Feed'den gelen kabloyu al
            self.input_file_path = self.request.model.configs.executor.value.inputs.inputFile.value
        except AttributeError:
            self.input_file_path = None
            
        # File Save'e gidecek yol
        self.output_file_path = ""

    @staticmethod
    def bootstrap(config: dict) -> dict:
        return {}

    def convert_to_pdf(self, input_path, output_path):
        if FPDF is None:
            raise ImportError("Sistemde 'fpdf2' kurulu değil!")

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Helvetica", size=12)

        with open(input_path, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                clean_line = line.strip().encode('latin-1', 'replace').decode('latin-1')
                pdf.cell(200, 10, txt=clean_line, ln=True, align='L')

        pdf.output(output_path)

    def run(self):
        try:
            if not self.input_file_path or not os.path.exists(self.input_file_path):
                raise FileNotFoundError(f"Data Feed'den dosya gelmedi: {self.input_file_path}")

            base_name = os.path.basename(self.input_file_path)
            hedef_klasor = "/tmp/" # Konteyner içi güvenli geçici klasör
            zaman = datetime.now().strftime("%H%M%S")
            output_path = os.path.join(hedef_klasor, f"converted_{zaman}_{base_name}.pdf")

            # Çevir
            self.convert_to_pdf(self.input_file_path, output_path)
            
            # Oluşan yolu çıktı değişkenine ata
            self.output_file_path = output_path
            
            print(f"\n🦅 PDF CONVERTER BAŞARILI: {self.output_file_path}\n", flush=True)

        except Exception as e:
            self.output_file_path = f"HATA: {str(e)}"
            print(f"\n❌ PDF CONVERTER HATA: {str(e)}\n", flush=True)

        return build_response(context=self)

if "__main__" == __name__:
    Executor(sys.argv[1]).run()