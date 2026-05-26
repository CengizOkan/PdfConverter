from sdks.novavision.src.helper.package import PackageHelper
from components.Package.src.models.PackageModel import (
    PackageModel, PackageConfigs, ConfigExecutor, 
    ExecutorOutputs, PackageResponse, PackageExecutor, 
    OutputMessage
)

def build_response(context):
    outputMessage = OutputMessage(value=context.output_message)
    outputs = ExecutorOutputs(outputMessage=outputMessage)
    
    packageResponse = PackageResponse(outputs=outputs)
    packageExecutor = PackageExecutor(value=packageResponse)
    executor = ConfigExecutor(value=packageExecutor)
    packageConfigs = PackageConfigs(executor=executor)
    
    package = PackageHelper(packageModel=PackageModel, packageConfigs=packageConfigs)
    return package.build_model(context)