from fastapi import FastAPI
from fastapi.exceptions import HTTPException
from pydantic import BaseModel
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


fx = DX_ParkingDuration(name=worker_name)
app = FastAPI()

# Modify this class to represent your expected input structure.
class ExtractorInput(BaseModel):
    imaginary_id: str
    GoogleOcrDataFormatted: dict



@app.get("/liveness")
async def liveness():
    return "I am alive."

# use this method to feed inference tasks to your extractor and return an appropriate response
@app.post("/extract")
async def extract(payload: ExtractorInput):
    response = fx.extract(payload.dict())
    if response is None:
        raise HTTPException(status_code=500, detail="Internal failure. Was unable to process request.")
    return response