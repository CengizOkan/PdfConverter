"""
    Converts strictly filtered input files (.txt, .jpg, .png) to PDF format.
"""
import os
import sys
from fpdf import FPDF  # PDF dönüştürme kütüphanesi

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../../'))

from sdks.novavision.src.base.component import Component
from sdks.novavision.src.helper.executor import Executor
from components.Package.src.utils.response import build_response
from components.Package.src.models.PackageModel import PackageModel

class Package(Component):
    def __init__(self, request, bootstrap):
        super().__init__(request, bootstrap)
        
        self.request.model = PackageModel(**(self.request.data))
        
        # Dosya ID'sini Config üzerinden alıyoruz
        self.input_file_id = self.request.get_param("ConfigInputFile")
        
        self.output_file = None
        self.output_message = {}

    @staticmethod
    def bootstrap(config: dict) -> dict:
        return {}

    def fetch_file_path(self, file_id):
        """
        NovaVision storage sisteminden ID ile dosyanın fiziksel yolunu çeker.
        """
        # TODO: Portalium SDK'sının storage metodunu kullanarak file_id'den dosya yolunu almalısın.
        # Çizimindeki örnekten yola çıkarak şimdilik mock (taklit) bir path dönüyoruz:
        return f"/tmp/storage/{file_id}_uhud.txt"

    def convert_to_pdf(self, input_path):
        """
        Dosyayı okur ve .pdf formatına dönüştürür.
        """
        if not os.path.exists(input_path):
            # Dosya sistemde yoksa mock path üzerinden hata almamak için 
            # asıl staj ortamında buradaki pass yerine hata fırlatmalısın.
            pass 

        # Yeni pdf dosyasının ismini ayarla (uhud.txt -> uhud.pdf)
        file_ext = input_path.split('.')[-1].lower()
        output_path = input_path.rsplit('.', 1)[0] + ".pdf"
        
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        
        # 1. Eğer dosya TXT ise:
        if file_ext == "txt":
            # Dosyayı satır satır okuyup PDF'e yaz
            try:
                with open(input_path, "r", encoding="utf-8") as f:
                    for line in f:
                        # Türkçe karakter uyumu için latin-1 dönüştürmesi (fpdf varsayılanı)
                        safe_text = line.encode('latin-1', 'replace').decode('latin-1')
                        pdf.multi_cell(0, 10, txt=safe_text)
            except FileNotFoundError:
                # Mock test için sahte içerik
                pdf.multi_cell(0, 10, txt="Bu, uhud.txt dosyasinin PDF'e donusmus halidir.")
                
        # 2. Eğer dosya Resim ise (JPG, PNG):
        elif file_ext in ["jpg", "jpeg", "png"]:
            # Resmi tam sayfa genişliğinde ekle
            pdf.image(input_path, x=10, y=10, w=190)
            
        else:
            raise ValueError(f"Bu dosya formati henüz desteklenmiyor: {file_ext}")
            
        # PDF'i kaydet (uhud.pdf)
        pdf.output(output_path)
        
        return output_path

    def run(self):
        try:
            if not self.input_file_id:
                raise ValueError("Herhangi bir dosya yüklenmedi.")
            
            # 1. Dosyanın yerel yolunu Storage'dan al (Çizimdeki "storage -> uhud.txt" adımı)
            input_file_path = self.fetch_file_path(self.input_file_id)
            
            # 2. PDF'e dönüştür (Çizimdeki "executor" adımı)
            output_pdf_path = self.convert_to_pdf(input_file_path)
            
            # 3. Çıktıyı arayüze/storage'a gönder (Çizimdeki "web storage" adımı)
            self.output_file = output_pdf_path
            
            # 4. Başarılı mesajını oluştur (Çizimdeki "message (success)" adımı)
            self.output_message = {
                "status": "Success",
                "message": f"Dosya başarıyla dönüştürüldü: {output_pdf_path}"
            }
            
        except Exception as e:
            self.output_file = None
            self.output_message = {
                "status": "Error",
                "message": f"Dönüştürme başarısız oldu: {str(e)}"
            }

        package_model = build_response(context=self)
        return package_model

if "__main__" == __name__:
    Executor(sys.argv[1]).run()