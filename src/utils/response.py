from sdks.novavision.src.helper.package import PackageHelper
from components.Package.src.models.PackageModel import (
    PackageModel, PackageConfigs, ConfigExecutor, 
    ExecutorOutputs, PackageResponse, PackageExecutor, 
    OutputFile
)

def build_response(context):
    # Context içindeki output_file (pdf yolu) objesini al
    outputFile = OutputFile(value=context.output_file)
    
    # Çıkışa bu PDF'i bağla
    outputs = ExecutorOutputs(outputFile=outputFile)
    
    packageResponse = PackageResponse(outputs=outputs)
    packageExecutor = PackageExecutor(value=packageResponse)
    executor = ConfigExecutor(value=packageExecutor)
    packageConfigs = PackageConfigs(executor=executor)
    
    package = PackageHelper(packageModel=PackageModel, packageConfigs=packageConfigs)
    return package.build_model(context)