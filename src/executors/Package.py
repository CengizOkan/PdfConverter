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
        
        self.input_file_path = None
        try:
            incoming_data = self.request.model.configs.executor.value.inputs.inputFile.value
            
            # 1. KALKAN: Veri Liste İse (DataFeed birden fazla dosya desteklediği için liste atıyor olabilir)
            if isinstance(incoming_data, list) and len(incoming_data) > 0:
                incoming_data = incoming_data[0] # İlk elemanı al
                
            # 2. KALKAN: Veri Sözlük (dict) İse (İçindeki yolu ayıkla)
            if isinstance(incoming_data, dict):
                self.input_file_path = (
                    incoming_data.get("filePath") or 
                    incoming_data.get("path") or 
                    incoming_data.get("absolutePath") or 
                    incoming_data.get("value")
                )
                # Anahtar uyuşmazsa "değeri" string olan ilk değişkeni kap
                if not self.input_file_path:
                    for val in incoming_data.values():
                        if isinstance(val, str) and (val.startswith("/") or val.startswith("C:\\")):
                            self.input_file_path = val
                            break
                            
            # 3. KALKAN: Veri doğrudan string İse
            elif isinstance(incoming_data, str):
                self.input_file_path = incoming_data
                
        except Exception:
            self.input_file_path = None
            
        # Sağ panelden kayıt yerini (savePath) al
        try:
            if self.request.model.configs.executor.value.configs:
                self.save_path = self.request.model.configs.executor.value.configs.savePath.value
            else:
                self.save_path = "/home/cengizokan/Downloads/"
        except Exception:
            self.save_path = "/home/cengizokan/Downloads/"
            
        self.output_message = {}

    @staticmethod
    def bootstrap(config: dict) -> dict:
        return {}

    def convert_to_pdf(self, input_path, output_path):
        if FPDF is None:
            raise ImportError("Sistemde 'fpdf2' kurulu degil! (Lutfen 'pip install fpdf2' calistirin)")

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
            if not self.input_file_path or not os.path.exists(str(self.input_file_path)):
                raise FileNotFoundError(f"Kablodan gelen veriden dosya yolu cikarilamadi veya dosya yok: {self.input_file_path}")

            if not os.path.exists(self.save_path):
                os.makedirs(self.save_path, exist_ok=True)

            base_name = os.path.basename(self.input_file_path)
            zaman = datetime.now().strftime("%H%M%S")
            output_path = os.path.join(self.save_path, f"converted_{zaman}_{base_name}.pdf")

            self.convert_to_pdf(self.input_file_path, output_path)
            
            self.output_message = {
                "status": "Success",
                "message": f"PDF locale kaydedildi: {output_path}"
            }
            print(f"\n🦅 PDF CONVERTER BAŞARILI: {output_path}\n", flush=True)

        except Exception as e:
            self.output_message = {"status": "Error", "message": str(e)}
            print(f"\n❌ PDF CONVERTER HATA: {str(e)}\n", flush=True)

        return build_response(context=self)

if "__main__" == __name__:
    Executor(sys.argv[1]).run()