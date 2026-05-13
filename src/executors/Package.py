import os
import sys
from datetime import datetime

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../../'))

from sdks.novavision.src.base.component import Component
from sdks.novavision.src.helper.executor import Executor
from components.Package.src.utils.response import build_response
from components.Package.src.models.PackageModel import PackageModel

# İstenen kütüphaneyi içeri aktarıyoruz
try:
    from fpdf import FPDF
except ImportError:
    pass # Hatayı aşağıda yakalayıp loga basacağız

class Package(Component):
    def __init__(self, request, bootstrap):
        super().__init__(request, bootstrap)
        self.request.model = PackageModel(**(self.request.data))
        
        try:
            # Data Feed'den gelen kabloyu okuyoruz
            self.input_file_path = self.request.model.configs.executor.value.inputs.inputFile.value
        except AttributeError:
            self.input_file_path = None
            
        self.output_message = {}

    @staticmethod
    def bootstrap(config: dict) -> dict:
        return {}

    def run(self):
        try:
            # 1. Girdi Kontrolü
            if not self.input_file_path or not os.path.exists(self.input_file_path):
                raise ValueError(f"Data Feed'den gelen dosya bulunamadi: {self.input_file_path}")

            if 'fpdf' not in sys.modules:
                raise ImportError("Sistemde 'fpdf' kütüphanesi kurulu değil!")

            # 2. Çıktı Yolu Hazırlığı
            dosya_adi = os.path.basename(self.input_file_path)
            hedef_klasor = "/home/cengizokan/Downloads/"
            zaman_damgasi = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = os.path.join(hedef_klasor, f"cevrilmis_{dosya_adi}_{zaman_damgasi}.pdf")

            # 3. KÜTÜPHANE KULLANARAK PDF OLUŞTURMA
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Helvetica", size=12) # Standart font

            # Dosyayı okuyup PDF'e satır satır yazıyoruz
            with open(self.input_file_path, "r", encoding="utf-8") as f:
                for satir in f:
                    # Türkçe karakterleri ve özel işaretleri bozmaması için latin-1'e güvenli kodlama
                    temiz_satir = satir.encode('latin-1', 'replace').decode('latin-1')
                    pdf.cell(200, 10, txt=temiz_satir, ln=1, align='L')

            # PDF'i kaydet
            pdf.output(output_path)

            # 4. Başarı Mesajı
            self.output_message = {
                "status": "Success",
                "message": f"Kütüphane (fpdf) kullanılarak PDF oluşturuldu: {output_path}"
            }
        except Exception as e:
            self.output_message = {"status": "Error", "message": str(e)}

        # Loglarda sonucu görmek için
        print("\n🦅 PDF CONVERTER SONUCU:", self.output_message, "\n", flush=True)

        return build_response(context=self)

if "__main__" == __name__:
    Executor(sys.argv[1]).run()