from typing import Optional, Union, Literal
from sdks.novavision.src.base.model import Package, Inputs, Configs, Outputs, Response, Request, Output, Config, Input

# --- Girdi (Data Feed'den Gelecek) ---
class InputFile(Input):
    name: Literal["inputFile"] = "inputFile"
    value: str 
    type: str = "string"

# --- Çıktı (Sadece Durum Mesajı) ---
class OutputMessage(Output):
    name: Literal["outputMessage"] = "outputMessage"
    value: dict
    type: str = "object"
    class Config:
        title = "Status Message"

class ExecutorInputs(Inputs):
    inputFile: InputFile

class ExecutorOutputs(Outputs):
    outputMessage: OutputMessage # Sağ tarafta sadece mesaj ucu olacak

class PackageRequest(Request):
    inputs: ExecutorInputs
    configs: Optional[Configs]
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

class ConfigExecutor(Config):
    name: Literal["ConfigExecutor"] = "ConfigExecutor"
    value: Union[PackageExecutor]
    type: Literal["executor"] = "executor"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"

class PackageConfigs(Configs):
    executor: ConfigExecutor

class PackageModel(Package):
    configs: PackageConfigs
    type: Literal["component"] = "component"
    name: Literal["PdfConverter"] = "PdfConverter"