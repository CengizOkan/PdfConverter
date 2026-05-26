from typing import Optional, Union, Literal, Any
from sdks.novavision.src.base.model import Package, Inputs, Configs, Outputs, Response, Request, Output, Config

# Sol Kablo (Veri Girişi)
class InputFile(Config):
    name: Literal["inputFile"] = "inputFile"
    value: Any = None 
    type: Literal["object"] = "object"

# Sağ Kablo (Sonuç Mesajı)
class OutputMessage(Output):
    name: Literal["outputMessage"] = "outputMessage"
    value: dict = {}
    type: Literal["object"] = "object"
    class Config:
        title = "Durum Mesajı"

class ExecutorInputs(Inputs):
    inputFile: InputFile

class ExecutorConfigs(Configs):
    pass # Sağ paneli sildik, dert bitti!

class ExecutorOutputs(Outputs):
    outputMessage: OutputMessage

class PackageRequest(Request):
    inputs: ExecutorInputs
    configs: Optional[ExecutorConfigs] = None
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