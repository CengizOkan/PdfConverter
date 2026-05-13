import os
import sys
from datetime import datetime

# SDK yollarını sisteme ekliyoruz
sys.path.append(os.path.join(os.path.dirname(__file__), '../../../../'))

from sdks.novavision.src.base.component import Component
from sdks.novavision.src.helper.executor import Executor
from components.Package.src.utils.response import build_response
from components.Package.src.models.PackageModel import PackageModel

# Python 3.13 uyumlu fpdf2 kütüphanesini içeri aktarıyoruz
try:
    from fpdf import FPDF
except ImportError:
    FPDF = None

class Package(Component):
    def __init__(self, request, bootstrap):
        super().__init__(request, bootstrap)
        self.request.model = PackageModel(**(self.request.data))
        
        try:
            # Data Feed'den gelen yolu alıyoruz
            self.input_file_path = self.request.model.configs.executor.value.inputs.inputFile.value
        except AttributeError:
            self.input_file_path = None
            
        self.output_message = {}

    @staticmethod
    def bootstrap(config: dict) -> dict:
        return {}

    def convert_to_pdf(self, input_path, output_path):
        """fpdf2 kullanarak dosyayı PDF'e dönüştürür"""
        if FPDF is None:
            raise ImportError("Sistemde 'fpdf2' kütüphanesi kurulu değil!")

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Helvetica", size=12)

        # Dosya içeriğini oku ve PDF'e yaz
        with open(input_path, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                # Satır sonu karakterlerini temizle ve güvenli kodlama yap
                clean_line = line.strip().encode('latin-1', 'replace').decode('latin-1')
                pdf.cell(200, 10, txt=clean_line, ln=True, align='L')

        pdf.output(output_path)

    def run(self):
        try:
            # 1. Giriş Kontrolü
            if not self.input_file_path or not os.path.exists(self.input_file_path):
                raise FileNotFoundError(f"Data Feed'den geçerli bir dosya gelmedi: {self.input_file_path}")

            # 2. Dosya Adı ve Uzantısı
            base_name = os.path.basename(self.input_file_path)
            hedef_klasor = "/home/cengizokan/Downloads/"
            zaman = datetime.now().strftime("%H%M%S")
            output_path = os.path.join(hedef_klasor, f"converted_{zaman}_{base_name}.pdf")

            # 3. Dönüştürme İşlemi
            self.convert_to_pdf(self.input_file_path, output_path)
            
            self.output_message = {
                "status": "Success",
                "message": f"PDF Başarıyla Oluşturuldu: {output_path}"
            }
        except Exception as e:
            self.output_message = {"status": "Error", "message": str(e)}

        # Docker logları için terminale çıktı veriyoruz
        print("\n🦅 PDF CONVERTER SONUCU:", self.output_message, "\n", flush=True)

        return build_response(context=self)

if "__main__" == __name__:
    Executor(sys.argv[1]).run()