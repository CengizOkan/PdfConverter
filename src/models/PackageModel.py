from pydantic import Field, validator
from typing import List, Optional, Union, Literal
from sdks.novavision.src.base.model import Package, File, Inputs, Configs, Outputs, Response, Request, Output, Config

# --- Yeni Dosya Seçici Konfigürasyonu ---
class ConfigInputFile(Config):
    name: Literal["ConfigInputFile"] = "ConfigInputFile"
    value: int  # filePicker sistemden dosya ID'si döndürür
    type: Literal["number"] = "number"
    field: Literal["filePicker"] = "filePicker"
    restart: Literal[True] = True
    
    class Config:
        json_schema_extra = {
            "shortDescription": "Dönüştürülecek Dosya",
            "class": "portalium\\storage\\widgets\\FilePicker",
            "options": {
                "multiple": 0,
                "returnAttribute": ["name"],
                "name": "app::logo_wide",
                # SADECE BU UZANTILARA İZİN VERİLİR
                "fileExtensions": ["txt", "doc", "docx", "jpg", "jpeg", "png"] 
            },
        }
        title = "Dosya Yükle"

# --- Output Sınıfları (Aynı Kalıyor) ---
class OutputFile(Output):
    name: Literal["outputFile"] = "outputFile"
    value: Optional[File] = None
    type: Literal["File"] = "File"

    class Config:
        title = "Converted PDF File"

class OutputMessage(Output):
    name: Literal["outputMessage"] = "outputMessage"
    value: dict
    type: str = "object"

    class Config:
        title = "Status Message"

# --- Executor Input/Config/Output ---
class ExecutorInputs(Inputs):
    pass # Artık dosya Configs'den gelecek, burası boş kalabilir

class ExecutorConfigs(Configs):
    configInputFile: ConfigInputFile # filePicker'ı config içine ekledik

class ExecutorOutputs(Outputs):
    outputFile: OutputFile
    outputMessage: OutputMessage

# --- Request, Response, Executor, Package Modelleri (Öncekiyle Aynı) ---
class PackageRequest(Request):
    inputs: Optional[ExecutorInputs]
    configs: ExecutorConfigs

    class Config:
        json_schema_extra = {
            "target": "configs"
        }

class PackageResponse(Response):
    outputs: ExecutorOutputs

class PackageExecutor(Config):
    name: Literal["Package"] = "Package"
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
    name: Literal["Package"] = "Package"