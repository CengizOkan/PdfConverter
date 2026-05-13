import os
import sys
from fpdf import FPDF 
from datetime import datetime # Zaman damgası için

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
            
        self.output_message = {}

    def convert_to_pdf_with_library(self, input_path):
        if not os.path.exists(input_path):
            raise FileNotFoundError(f"Gelen dosya yolu bulunamadı: {input_path}")
            
        # --- DOĞRUDAN KAYIT MANTIĞI ---
        # Görseldeki ayarlara göre hedef klasör ve dosya adını belirliyoruz
        hedef_klasor = "/home/cengizokan/Downloads/"
        temel_isim = "messi"
        
        # Zaman damgası ekle (Görseldeki Filename Suffix: Time Stamp ayarı gibi)
        zaman_damgasi = datetime.now().strftime("%Y%m%d_%H%M%S")
        dosya_adi = f"{temel_isim}_{zaman_damgasi}.pdf"
        
        output_path = os.path.join(hedef_klasor, dosya_adi)
        # -----------------------------
        
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        
        with open(input_path, "r", encoding="utf-8") as f:
            for line in f:
                safe_text = line.encode('latin-1', 'replace').decode('latin-1')
                pdf.multi_cell(0, 10, txt=safe_text)
                
        # Dosyayı doğrudan Downloads klasörüne kaydet
        pdf.output(output_path)
        return output_path

    def run(self):
        try:
            if not self.input_file_path:
                raise ValueError("Girdi dosyası bulunamadı.")
            
            pdf_path = self.convert_to_pdf_with_library(self.input_file_path)
            
            self.output_message = {
                "status": "Success",
                "message": f"PDF başarıyla oluşturuldu ve şuraya kaydedildi: {pdf_path}"
            }
        except Exception as e:
            self.output_message = {"status": "Error", "message": str(e)}

        return build_response(context=self)

if "__main__" == __name__:
    Executor(sys.argv[1]).run()