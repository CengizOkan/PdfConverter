from typing import Optional, Union, Literal, Dict, Any
from sdks.novavision.src.base.model import Package, Inputs, Configs, Outputs, Response, Request, Output, Config

# Giriş yapısını dict (object) kabul edecek şekilde güncelledik
class InputFile(Config):
    name: Literal["inputFile"] = "inputFile"
    value: Dict[str, Any] 
    type: str = "object"

class OutputFile(Output):
    name: Literal["outputFile"] = "outputFile"
    value: str = ""
    type: str = "string"
    class Config:
        title = "Çevrilen PDF Dosyasının Yolu"

class ExecutorInputs(Inputs):
    inputFile: InputFile

class ExecutorConfigs(Configs):
    pass 

class ExecutorOutputs(Outputs):
    outputFile: OutputFile

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