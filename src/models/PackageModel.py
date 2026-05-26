from typing import Optional, Union, Literal, Any
from sdks.novavision.src.base.model import Package, Inputs, Configs, Outputs, Response, Request, Output, Config

# --- 1. Sol Kablo Ucu (Giriş) ---
class InputFile(Config):
    name: Literal["inputFile"] = "inputFile"
    value: Any = {}  # Liste veya sözlük gelse bile çökmeyi engeller
    type: str = "object"

# --- 2. Sağ Panel Ayarı (Klasör Yolu) ---
class ConfigSavePath(Config):
    name: Literal["savePath"] = "savePath"
    value: str = "/home/cengizokan/Downloads/"
    type: str = "string"
    class Config:
        title = "Kaydedilecek Klasör"

# --- 3. Sağ Kablo Ucu (Çıkış Durumu) ---
class OutputMessage(Output):
    name: Literal["outputMessage"] = "outputMessage"
    value: dict = {}
    type: str = "object"
    class Config:
        title = "Durum Mesajı"

# --- 4. Portların Zorunlu Kılınması (Kabloları Geri Getiren Kısım) ---
class ExecutorInputs(Inputs):
    inputFile: InputFile  # Optional ibaresi kaldırıldı, sol port geri gelecek

class ExecutorConfigs(Configs):
    savePath: ConfigSavePath

class ExecutorOutputs(Outputs):
    outputMessage: OutputMessage  # Optional ibaresi kaldırıldı, sağ port geri gelecek

class PackageRequest(Request):
    inputs: ExecutorInputs
    configs: Optional[ExecutorConfigs]
    class Config:
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