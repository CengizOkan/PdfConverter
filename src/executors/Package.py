import os
import sys
from fpdf import FPDF 

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../../'))

from sdks.novavision.src.base.component import Component
from sdks.novavision.src.helper.executor import Executor
from components.Package.src.utils.response import build_response
from components.Package.src.models.PackageModel import PackageModel

class Package(Component):
    def __init__(self, request, bootstrap):
        super().__init__(request, bootstrap)
        self.request.model = PackageModel(**(self.request.data))
        
        try:
            self.input_file_path = self.request.model.configs.executor.value.inputs.inputFile.value
        except AttributeError:
            self.input_file_path = None
            
        self.output_file = "" # Artık mesaj yerine dosyayı tutuyoruz

    @staticmethod
    def bootstrap(config: dict) -> dict:
        return {}

    def convert_to_pdf_with_library(self, input_path):
        if not os.path.exists(input_path):
            raise FileNotFoundError(f"Gelen dosya yolu bulunamadı: {input_path}")
            
        output_path = input_path.rsplit('.', 1)[0] + ".pdf"
        
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        
        with open(input_path, "r", encoding="utf-8") as f:
            for line in f:
                safe_text = line.encode('latin-1', 'replace').decode('latin-1')
                pdf.multi_cell(0, 10, txt=safe_text)
                
        pdf.output(output_path)
        return output_path

    def run(self):
        print("\n=== PDF CONVERTER CALISIYOR ===")
        try:
            if not self.input_file_path:
                raise ValueError("Flow üzerinden girdi gelmedi.")
            
            # PDF'i oluştur ve yolunu değişkene ata
            pdf_path = self.convert_to_pdf_with_library(self.input_file_path)
            self.output_file = pdf_path 
            print(f"PDF uretildi: {pdf_path}")
            
        except Exception as e:
            print(f"HATA: {str(e)}")
            self.output_file = ""

        return build_response(context=self)

if "__main__" == __name__:
    Executor(sys.argv[1]).run()