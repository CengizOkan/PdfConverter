from typing import Optional, Union, Literal, Any
from sdks.novavision.src.base.model import Package, Inputs, Configs, Outputs, Response, Request, Output, Config

# --- 1. Sol Kablo Ucu ---
class InputFile(Config):
    name: Literal["inputFile"] = "inputFile"
    value: Any = None  # Gelen her türlü veriyi (liste, dict) çökmeksizin kabul eder
    type: Literal["object"] = "object"

# --- 2. Sağ Panel Ayarı ---
class ConfigSavePath(Config):
    name: Literal["savePath"] = "savePath"
    value: str = "/home/cengizokan/Downloads/"
    type: Literal["string"] = "string"
    field: Literal["input"] = "input"  # ÇÖZÜM: Arayüze "Buraya metin kutusu çiz" dedik!
    class Config:
        title = "Kaydedilecek Klasör"

# --- 3. Sağ Kablo Ucu ---
class OutputMessage(Output):
    name: Literal["outputMessage"] = "outputMessage"
    value: dict = {}
    type: Literal["object"] = "object"

# --- 4. Doğru Katmanlandırma (Backend'i Çökertmeyen Yapı) ---
class ExecutorInputs(Inputs):
    inputFile: InputFile

class ExecutorConfigs(Configs):
    savePath: ConfigSavePath  # ÇÖZÜM: Ayar güvenli katmanda duruyor

class ExecutorOutputs(Outputs):
    outputMessage: OutputMessage

class PackageRequest(Request):
    inputs: ExecutorInputs
    configs: ExecutorConfigs
    class Config:
        json_schema_extra = {"target": "inputs"} # Kabloların görünmesini sağlar

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