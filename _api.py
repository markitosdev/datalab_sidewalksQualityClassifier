from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel
from starlette.middleware.cors import CORSMiddleware

from imageProcessors.imageDataset.createImageDatasetFromDataFrameWithCoordinates import \
    createImageDatasetFromDataFrameWithCoordinates
from predict.predictSingleCoordinates import predictSingleCoordinates

app = FastAPI()

class RequestParams(BaseModel):
    latitude: float
    longitude: float

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/predictFromCoordinatesApi")
def predictFromCoordinatesApi(params: RequestParams):
    return predictSingleCoordinates(params.latitude, params.longitude, singlePointName="predictionImages", modelPath='repopulated_dataset_based', datasetPath='dataset')
