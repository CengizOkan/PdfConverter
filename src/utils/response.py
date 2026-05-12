from sdks.novavision.src.helper.package import PackageHelper
from components.Package.src.models.PackageModel import (
    PackageModel, PackageConfigs, ConfigExecutor, 
    ExecutorOutputs, PackageResponse, PackageExecutor, 
    OutputMessage
)

def build_response(context):
    # Context içindeki output_message objesini al
    outputMessage = OutputMessage(value=context.output_message)
    
    # Flow'a sadece mesajı bağla
    outputs = ExecutorOutputs(outputMessage=outputMessage)
    
    packageResponse = PackageResponse(outputs=outputs)
    packageExecutor = PackageExecutor(value=packageResponse)
    executor = ConfigExecutor(value=packageExecutor)
    packageConfigs = PackageConfigs(executor=executor)
    
    package = PackageHelper(packageModel=PackageModel, packageConfigs=packageConfigs)
    package_model = package.build_model(context)
    
    return package_model