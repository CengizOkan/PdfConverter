import os
import sys
from datetime import datetime

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../../'))

from sdks.novavision.src.base.component import Component
from sdks.novavision.src.helper.executor import Executor
from components.Package.src.utils.response import build_response
from components.Package.src.models.PackageModel import PackageModel

class Package(Component):
    def __init__(self, request, bootstrap):
        super().__init__(request, bootstrap)
        self.request.model = PackageModel(**(self.request.data))
        
        # Yeniden Flow'dan dosya gelmesini bekleyen yapıya dönüyoruz
        try:
            self.input_file_path = self.request.model.configs.executor.value.inputs.inputFile.value
        except AttributeError:
            self.input_file_path = None
            
        self.output_message = {}

    @staticmethod
    def bootstrap(config: dict) -> dict:
        return {}

    def text_to_pdf(self, input_path, output_path):
        """ .txt veya .csv gibi düz metinleri çevirir """
        # Not: Sisteme fpdf kurulduğunda buralar fpdf kodlarıyla güncellenebilir
        with open(input_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
            
        text_content = ""
        y_position = 750
        for line in lines:
            clean_line = line.strip().replace("(", "\\(").replace(")", "\\)")
            text_content += f"1 0 0 1 50 {y_position} Tm ({clean_line}) Tj\n"
            y_position -= 15
            if y_position < 50: break

        pdf_structure = (
            "%PDF-1.1\n1 0 obj << /Type /Catalog /Pages 2 0 R >> endobj\n"
            "2 0 obj << /Type /Pages /Kids [3 0 R] /Count 1 >> endobj\n"
            "3 0 obj << /Type /Page /Parent 2 0 R /Resources << /Font << /F1 4 0 R >> >> /Contents 5 0 R >> endobj\n"
            "4 0 obj << /Type /Font /Subtype /Type1 /BaseFont /Helvetica >> endobj\n"
            f"5 0 obj << /Length {len(text_content) + 20} >> stream\nBT\n/F1 12 Tf\n{text_content}ET\nendstream\nendobj\n"
            "xref\n0 6\n0000000000 65535 f\n0000000010 00000 n\n0000000059 00000 n\n0000000116 00000 n\n0000000212 00000 n\n0000000275 00000 n\n"
            "trailer << /Size 6 /Root 1 0 R >>\nstartxref\n450\n%%EOF"
        )
        with open(output_path, "w", encoding="latin-1") as f:
            f.write(pdf_structure)

    def image_to_pdf(self, input_path, output_path):
        """ .jpg, .png gibi görselleri çevirir """
        try:
            # Pillow (PIL) kütüphanesi gerektirir
            from PIL import Image
            image = Image.open(input_path)
            pdf_bytes = image.convert('RGB')
            pdf_bytes.save(output_path)
        except ImportError:
            raise ImportError("Gorselleri cevirmek icin Docker icine 'Pillow' kütüphanesi kurulmali! (pip install Pillow)")

    def office_to_pdf(self, input_path, output_path):
        """ .docx, .xlsx gibi Office belgelerini çevirir """
        # Linux sistemlerinde Office dosyalarını çevirmenin endüstri standardı LibreOffice kullanmaktır.
        import subprocess
        try:
            hedef_klasor = os.path.dirname(output_path)
            subprocess.run(['libreoffice', '--headless', '--convert-to', 'pdf', input_path, '--outdir', hedef_klasor], check=True)
        except Exception:
            raise RuntimeError("Word/Excel dosyalari icin Docker imajina 'libreoffice' paketi kurulmali!")

    def run(self):
        try:
            if not self.input_file_path or not os.path.exists(self.input_file_path):
                raise ValueError(f"Gelen dosya yolu bulunamadi veya baglanmadi: {self.input_file_path}")

            # Dosyanın ismini ve uzantısını ayırıyoruz (Örn: "rapor.docx" -> uzantı: "docx")
            dosya_adi = os.path.basename(self.input_file_path)
            uzanti = dosya_adi.split('.')[-1].lower()
            
            # Kaydedilecek yeri belirliyoruz
            hedef_klasor = "/home/cengizokan/Downloads/"
            zaman_damgasi = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = os.path.join(hedef_klasor, f"{dosya_adi}_{zaman_damgasi}.pdf")

            # --- TRAFİK POLİSİ MANTIĞI ---
            if uzanti in ['txt', 'csv']:
                self.text_to_pdf(self.input_file_path, output_path)
                
            elif uzanti in ['jpg', 'jpeg', 'png']:
                self.image_to_pdf(self.input_file_path, output_path)
                
            elif uzanti in ['doc', 'docx', 'xls', 'xlsx']:
                self.office_to_pdf(self.input_file_path, output_path)
                
            else:
                raise ValueError(f"Sistem henuz bu dosya uzantisini desteklemiyor: .{uzanti}")
            # -----------------------------

            self.output_message = {
                "status": "Success",
                "message": f"Dosya ({uzanti}) basariyla PDF yapildi: {output_path}"
            }
        except Exception as e:
            self.output_message = {"status": "Error", "message": str(e)}

        return build_response(context=self)

if "__main__" == __name__:
    Executor(sys.argv[1]).run()