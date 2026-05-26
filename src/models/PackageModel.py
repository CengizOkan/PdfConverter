from typing import Optional, Union, Literal, Dict, Any
from sdks.novavision.src.base.model import Package, Inputs, Configs, Outputs, Response, Request, Output, Config

# --- 1. Kablodan Gelecek Girdi ---
class InputFile(Config):
    name: Literal["inputFile"] = "inputFile"
    value: Dict[str, Any] 
    type: str = "object"

# --- 2. Sağ Panelde Görünecek Ayar (YENİ DEĞİŞİKLİK) ---
class ConfigSavePath(Config):
    name: Literal["savePath"] = "savePath"
    value: str = "/home/cengizokan/Downloads/"
    type: str = "string"
    class Config:
        title = "Kaydedilecek Klasör"

# --- 3. İşlem Sonucu Çıktısı ---
class OutputMessage(Output):
    name: Literal["outputMessage"] = "outputMessage"
    value: dict
    type: str = "object"
    class Config:
        title = "Durum Mesajı"

# --- 4. Container'lar ---
class ExecutorInputs(Inputs):
    inputFile: InputFile

class ExecutorConfigs(Configs):
    savePath: ConfigSavePath

class ExecutorOutputs(Outputs):
    outputMessage: OutputMessage

# --- 5. Request ve Response (KİLİT NOKTA) ---
class PackageRequest(Request):
    inputs: ExecutorInputs
    configs: ExecutorConfigs # Optional'ı kaldırdık, kesinlikle istiyoruz
    class Config:
        # ŞİFRE BURADA: UI motoruna hem sol kabloyu (inputs) hem de sağ paneli (configs) çizdiriyoruz!
        json_schema_extra = {"target": ["inputs", "configs"]}

class PackageResponse(Response):
    outputs: ExecutorOutputs

# --- 6. Ana Executor Bağlantıları ---
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