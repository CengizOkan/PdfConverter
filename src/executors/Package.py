"""
    Converts strictly filtered input files to PDF format.
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
        
        # Dosya ID'sini Config üzerinden alıyoruz
        self.input_file_id = self.request.get_param("ConfigInputFile")
        
        self.output_file = None
        self.output_message = {}

    @staticmethod
    def bootstrap(config: dict) -> dict:
        return {}

    def fetch_file_by_id(self, file_id):
        """NovaVision storage sisteminden ID ile dosyayı çeker."""
        # TODO: Sistemin storage modülünü kullanarak file_id ile dosyayı RAM'e veya geçici dizine çek.
        return file_data

    def convert_to_pdf(self, file_data):
        """Dosyayı PDF formatına dönüştürür."""
        # TODO: PDF dönüştürme algoritmaları
        return file_data

    def run(self):
        try:
            if not self.input_file_id:
                raise ValueError("Herhangi bir dosya yüklenmedi.")
            
            # 1. Dosyayı Storage'dan çek
            raw_file = self.fetch_file_by_id(self.input_file_id)
            
            # 2. PDF'e dönüştür
            self.output_file = self.convert_to_pdf(raw_file)
            
            # 3. Başarılı mesajını oluştur
            self.output_message = {
                "status": "Başarılı",
                "message": "Seçilen dosya başarıyla PDF formatına dönüştürüldü."
            }
            
        except Exception as e:
            self.output_file = None
            self.output_message = {
                "status": "Başarısız",
                "message": f"Dönüştürme başarısız oldu: {str(e)}"
            }

        package_model = build_response(context=self)
        return package_model

if "__main__" == __name__:
    Executor(sys.argv[1]).run()