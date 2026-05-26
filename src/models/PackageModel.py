from typing import Optional, Union, Literal, Any
from sdks.novavision.src.base.model import Package, Inputs, Configs, Outputs, Response, Request, Output, Config

# --- 1. Sol Kablo (Giriş) ---
class InputFile(Config):
    name: Literal["inputFile"] = "inputFile"
    value: Any = {}
    type: Literal["object"] = "object"

# --- 2. Sağ Kablo (Çıkış) ---
class OutputMessage(Output):
    name: Literal["outputMessage"] = "outputMessage"
    value: dict = {}
    type: Literal["object"] = "object"
    class Config:
        title = "Durum Mesajı"

class ExecutorInputs(Inputs):
    inputFile: InputFile

class ExecutorOutputs(Outputs):
    outputMessage: OutputMessage

class PackageRequest(Request):
    inputs: ExecutorInputs
    configs: Optional[Configs] = None # Derin bodrumu boşalttık
    class Config:
        json_schema_extra = {"target": "inputs"} # Kabloların kaybolmaması için

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

# --- 3. SAĞ PANEL AYARI (YENİ VE DOĞRU YERİ) ---
class ConfigSavePath(Config):
    name: Literal["savePath"] = "savePath"
    value: str = "/home/cengizokan/Downloads/"
    type: Literal["string"] = "string"
    field: Literal["input"] = "input"
    class Config:
        title = "Kaydedilecek Klasör"

# Ayarı doğrudan ana Configs sınıfına (kök dizine) ekledik!
class PackageConfigs(Configs):
    executor: ConfigExecutor
    savePath: ConfigSavePath = ConfigSavePath() 

class PackageModel(Package):
    configs: PackageConfigs
    type: Literal["component"] = "component"
    name: Literal["PdfConverter"] = "PdfConverter"