import requests
from pydantic import BaseModel

from googleMapsApiKey import GoogleMapsApiKey


class StreetViewMetadataParams(BaseModel):
    latitude: float
    longitude: float
    azimuthalAngle: float


def getStreetViewImageMetadata(params: StreetViewMetadataParams):
    return requests.post(f"https://maps.googleapis.com/maps/api/streetview/metadata?location={params.latitude},{params.longitude}&heading={params.azimuthalAngle}&pitch=0.0&fov=90&key={GoogleMapsApiKey.GoogleMapsApiKey}").json()
