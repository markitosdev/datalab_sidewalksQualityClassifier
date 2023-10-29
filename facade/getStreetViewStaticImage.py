from pydantic import BaseModel
import requests

from googleMapsApiKey import GoogleMapsApiKey


class StreetViewStaticImageParams(BaseModel):
    latitude: float
    longitude: float
    azimuthalAngle: float

def getStreetViewStaticImage(params: StreetViewStaticImageParams):
    return requests.post(f"https://maps.googleapis.com/maps/api/streetview?size=600x300&location={params.latitude},{params.longitude}&heading={params.azimuthalAngle}&pitch=0.0&fov=90&key={GoogleMapsApiKey.GoogleMapsApiKey}")
