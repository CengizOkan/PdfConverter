from typing import Optional, Union, Literal, Any
from sdks.novavision.src.base.model import Package, Inputs, Configs, Outputs, Response, Request, Output, Config

# Gelen veri liste, dict veya str olabilir. Katı kuralı kaldırdık (Any).
class InputFile(Config):
    name: Literal["inputFile"] = "inputFile"
    value: Any 
    type: str = "object"

class ConfigSavePath(Config):
    name: Literal["savePath"] = "savePath"
    value: str = "/home/cengizokan/Downloads/"
    type: str = "string"
    class Config:
        title = "Kaydedilecek Klasör"

class OutputMessage(Output):
    name: Literal["outputMessage"] = "outputMessage"
    value: dict
    type: str = "object"
    class Config:
        title = "Durum Mesajı"

class ExecutorInputs(Inputs):
    inputFile: InputFile

class ExecutorConfigs(Configs):
    savePath: ConfigSavePath

class ExecutorOutputs(Outputs):
    outputMessage: OutputMessage

class PackageRequest(Request):
    inputs: ExecutorInputs
    configs: Optional[ExecutorConfigs] = None # Arayüz henüz kaydedilmemişse çökmeyi önler
    class Config:
        # UI'a hem sol kabloyu hem sağ ayar panelini çizdiriyoruz
        json_schema_extra = {"target": ["inputs", "configs"]}

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