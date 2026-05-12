from pydantic import validator
from typing import Optional, Union, Literal
from sdks.novavision.src.base.model import Package, Inputs, Configs, Outputs, Response, Request, Output, Config

# --- 1. Girdi (Config üzerinden FilePicker ile) ---
class ConfigInputFile(Config):
    name: Literal["ConfigInputFile"] = "ConfigInputFile"
    value: int
    type: Literal["number"] = "number"
    field: Literal["filePicker"] = "filePicker"
    restart: Literal[True] = True
    
    class Config:
        json_schema_extra = {
            "shortDescription": "Dönüştürülecek Txt Dosyası",
            "class": "portalium\\storage\\widgets\\FilePicker",
            "options": {
                "multiple": 0,
                "returnAttribute": ["name"],
                "name": "app::logo_wide",
                "fileExtensions": ["txt"] # Şimdilik sadece txt
            },
        }
        title = "Dosya Yükle"

# --- 2. Çıktı (Sadece Mesaj) ---
class OutputMessage(Output):
    name: Literal["outputMessage"] = "outputMessage"
    value: dict
    type: str = "object"

    class Config:
        title = "Status Message"

# --- 3. Executor Input/Config/Output Toplayıcıları ---
class ExecutorInputs(Inputs):
    pass # Boş bıraktık çünkü girdiyi Configs'ten alıyoruz

class ExecutorConfigs(Configs):
    configInputFile: ConfigInputFile

class ExecutorOutputs(Outputs):
    outputMessage: OutputMessage # Flow'da görünecek TEK çıkış noktası

# --- 4. Request ve Response ---
class PackageRequest(Request):
    inputs: Optional[ExecutorInputs]
    configs: ExecutorConfigs

    class Config:
        json_schema_extra = {
            "target": "configs"
        }

class PackageResponse(Response):
    outputs: ExecutorOutputs

# --- 5. Executor ve Config Tanımları ---
class PackageExecutor(Config):
    name: Literal["Package"] = "Package"
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