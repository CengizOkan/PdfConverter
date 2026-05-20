from typing import Optional, Union, Literal
from sdks.novavision.src.base.model import Package, Inputs, Configs, Outputs, Response, Request, Output, Config

# Sol taraftan (Data Feed'den) gelecek kablo
class InputFile(Config):
    name: Literal["inputFile"] = "inputFile"
    value: str 
    type: str = "string"

# Sağ tarafa (File Save'e) gidecek kablo
class OutputFile(Output):
    name: Literal["outputFile"] = "outputFile"
    value: str = ""
    type: str = "string"
    class Config:
        title = "Converted PDF File"

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