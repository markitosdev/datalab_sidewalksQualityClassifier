import requests
from pydantic import BaseModel

from googleMapsApiKey import GoogleMapsApiKey


class StreetViewMetadataParams(BaseModel):
    latitude: float
    longitude: float
    azimuthalAngle: float


def getStreetViewImageMetadata(latitude: StreetViewMetadataParams.latitude, longitude: StreetViewMetadataParams.longitude,
                               azimuthalAngle: StreetViewMetadataParams.azimuthalAngle):
    return requests.post(f"https://maps.googleapis.com/maps/api/streetview/metadata?location={latitude},{longitude}&heading={azimuthalAngle}&pitch=0.0&fov=90&key={GoogleMapsApiKey.GoogleMapsApiKey}").json()
