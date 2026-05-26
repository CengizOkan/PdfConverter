from typing import Optional, Union, Literal, Any
from sdks.novavision.src.base.model import Package, Inputs, Configs, Outputs, Response, Request, Output, Config

# --- 1. Sol Kablo Ucu (Giriş Portu) ---
class InputFile(Config):
    name: Literal["inputFile"] = "inputFile"
    value: Any = {}
    type: str = "object"

# --- 2. Sağ Panel Ayarı (İŞTE EKSİK OLAN SİHİRLİ SATIR BURADA) ---
class ConfigSavePath(Config):
    name: Literal["savePath"] = "savePath"
    value: str = "/home/cengizokan/Downloads/"
    type: str = "string"
    # Arayüz motoruna "Buraya bir metin girme kutusu (input) çiz!" diyoruz
    field: Literal["input"] = "input" 
    class Config:
        title = "Kaydedilecek Klasör"

# --- 3. Sağ Kablo Ucu (Çıkış Portu) ---
class OutputMessage(Output):
    name: Literal["outputMessage"] = "outputMessage"
    value: dict = {}
    type: str = "object"
    class Config:
        title = "Durum Mesajı"

class ExecutorInputs(Inputs):
    inputFile: InputFile

class ExecutorConfigs(Configs):
    # Boş veri gelirse Pydantic çökmesin diye sınıfı varsayılan olarak başlatıyoruz
    savePath: ConfigSavePath = ConfigSavePath() 

class ExecutorOutputs(Outputs):
    outputMessage: OutputMessage

class PackageRequest(Request):
    inputs: ExecutorInputs
    # Optional etiketini kaldırdık ki UI motoru bunu kesinlikle okusun
    configs: ExecutorConfigs = ExecutorConfigs() 
    class Config:
        # Kabloların (portların) silinmemesi için target her zaman "inputs" kalmalı!
        json_schema_extra = {"target": "inputs"}

class PackageResponse(Response):
    outputs: ExecutorOutputs

class PackageExecutor(Config):
    name: Literal["PdfConverter"] = "PdfConverter"
    value: Union[PackageRequest, PackageResponse]
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"
    class Config:
        title = "Package"
        json_schema_extra = {"target": {"value": 0}}

class ConfigExecutor(Config):
    name: Literal["ConfigExecutor"] = "ConfigExecutor"
    value: Union[PackageExecutor]
    type: Literal["executor"] = "executor"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"
    class Config:
        title = "Task"
        json_schema_extra = {"target": "value"}

class PackageConfigs(Configs):
    executor: ConfigExecutor

class PackageModel(Package):
    configs: PackageConfigs
    type: Literal["component"] = "component"
    name: Literal["PdfConverter"] = "PdfConverter"