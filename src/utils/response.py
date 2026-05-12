from sdks.novavision.src.helper.package import PackageHelper
from components.Package.src.models.PackageModel import (
    PackageModel, PackageConfigs, ConfigExecutor, 
    ExecutorOutputs, PackageResponse, PackageExecutor, 
    OutputFile, OutputMessage
)

def build_response(context):
    # Çıktı objelerini oluştur
    outputFile = OutputFile(value=context.output_file)
    outputMessage = OutputMessage(value=context.output_message)
    
    # Response zincirini aşağıdan yukarıya kur
    outputs = ExecutorOutputs(outputFile=outputFile, outputMessage=outputMessage)
    packageResponse = PackageResponse(outputs=outputs)
    packageExecutor = PackageExecutor(value=packageResponse)
    
    configExecutor = ConfigExecutor(value=packageExecutor)
    packageConfigs = PackageConfigs(executor=configExecutor)
    
    # Modeli inşa et
    package = PackageHelper(
        packageModel=PackageModel, 
        packageConfigs=packageConfigs
    )
    package_model = package.build_model(context)
    
    return package_model