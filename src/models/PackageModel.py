from typing import Optional, Union, Literal, Any
from sdks.novavision.src.base.model import Package, Inputs, Configs, Outputs, Response, Request, Output, Config

# Sol taraftan gelecek giriş kablosu
class InputFile(Config):
    name: Literal["inputFile"] = "inputFile"
    value: Any = None  # UI boş gönderirse çökmemesi için eklendi
    type: str = "object"

# Sağ panelde görünecek kayıt yeri
class ConfigSavePath(Config):
    name: Literal["savePath"] = "savePath"
    value: str = "/home/cengizokan/Downloads/"
    type: str = "string"
    class Config:
        title = "Kaydedilecek Klasör"

# İşlem sonucu mesajı
class OutputMessage(Output):
    name: Literal["outputMessage"] = "outputMessage"
    value: dict = {}
    type: str = "object"
    class Config:
        title = "Durum Mesajı"

class ExecutorInputs(Inputs):
    inputFile: Optional[InputFile] = None

class ExecutorConfigs(Configs):
    savePath: Optional[ConfigSavePath] = None

class ExecutorOutputs(Outputs):
    outputMessage: Optional[OutputMessage] = None

class PackageRequest(Request):
    inputs: Optional[ExecutorInputs] = None
    configs: Optional[ExecutorConfigs] = None
    class Config:
        # HATA BURADAYDI: Sadece string olmalı. UI motoru config'i otomatik tanır.
        json_schema_extra = {"target": "inputs"}

class PackageResponse(Response):
    outputs: Optional[ExecutorOutputs] = None

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