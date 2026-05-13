from pydantic import validator
from typing import Optional, Union, Literal
from sdks.novavision.src.base.model import Package, Inputs, Configs, Outputs, Response, Request, Output, Config, Input

# --- 1. Girdi (Artık Flow üzerinden Input olarak geliyor) ---
class InputFile(Input):
    name: Literal["inputFile"] = "inputFile"
    value: str # Dışarıdan gelecek dosya yolu veya ID'si
    type: str = "string"

# --- 2. Çıktı (Sadece Mesaj - Aynı kalıyor) ---
class OutputMessage(Output):
    name: Literal["outputMessage"] = "outputMessage"
    value: dict
    type: str = "object"

    class Config:
        title = "Status Message"

# --- 3. Executor Input/Config/Output Toplayıcıları ---
class ExecutorInputs(Inputs):
    inputFile: InputFile # Flow'da kutunun solunda görünecek GİRİŞ noktası

class ExecutorConfigs(Configs):
    pass # Arayüzden seçilecek bir Config (FilePicker) kalmadı

class ExecutorOutputs(Outputs):
    outputMessage: OutputMessage # Flow'da kutunun sağında görünecek ÇIKIŞ noktası

# --- 4. Request ve Response ---
class PackageRequest(Request):
    inputs: ExecutorInputs
    configs: Optional[ExecutorConfigs]

    class Config:
        json_schema_extra = {
            "target": "inputs" # Artık hedeflenen ana veri inputs içinden geliyor
        }

class PackageResponse(Response):
    outputs: ExecutorOutputs

# --- 5. Executor ve Config Tanımları ---
class PackageExecutor(Config):
    name: Literal["PdfConverter"] = "PdfConverter"
    value: Union[PackageRequest, PackageResponse]
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"

    class Config:
        title = "Package"
        json_schema_extra = {
            "target": {
                "value": 0
            }
        }

class ConfigExecutor(Config):
    name: Literal["ConfigExecutor"] = "ConfigExecutor"
    value: Union[PackageExecutor]
    type: Literal["executor"] = "executor"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"

    class Config:
        title = "Task"
        json_schema_extra = {
            "target": "value"
        }

class PackageConfigs(Configs):
    executor: ConfigExecutor

# --- 6. Ana Package Model ---
class PackageModel(Package):
    configs: PackageConfigs
    type: Literal["component"] = "component"
    name: Literal["PdfConverter"] = "PdfConverter"