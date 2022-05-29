import sys
sys.path.insert(0, '..')
from beehive_infra.common.SqsExtractorWorker import *
from extractor.DX_ParkingDuration import DX_ParkingDuration
from beehive_infra.common.common_constants import *

# modify via deployment configuration or set your defaults
worker_step = getenv_str(WorkerEnvironmentVariable.worker_step, 'DataExtraction1')
default_worker_input_features = [ExtractedFeature('YourExtractorInput', FileExtension.json)] # dont forget to change this
default_worker_output_features = [ExtractedFeature('YourExtractorOutput', FileExtension.json)] # dont forget to change this
worker_name = getenv_str(WorkerEnvironmentVariable.worker_name, 'ParkingDuration')


class ParkingDurationExtractor(SqsExtractorWorker):
    def __init__(self, extractor: FxBase):
        super().__init__(name=worker_name, step=worker_step, extractor=extractor,
                         input_features=default_worker_input_features, output_features=default_worker_output_features)
        self.version = extractor.version


if __name__ == '__main__':
    fx = DX_ParkingDuration(name=worker_name)
    ext = ParkingDurationExtractor(extractor=fx)
    ext.main_loop()
