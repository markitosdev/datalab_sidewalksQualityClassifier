from pydantic import BaseModel
import requests

from googleMapsApiKey import GoogleMapsApiKey


class StreetViewStaticImageParams(BaseModel):
    latitude: float
    longitude: float
    azimuthalAngle: float

def getStreetViewStaticImage(latitude: StreetViewStaticImageParams.latitude, longitude: StreetViewStaticImageParams.longitude,
                             azimuthalAngle: StreetViewStaticImageParams.azimuthalAngle):
    return requests.post(f"https://maps.googleapis.com/maps/api/streetview?size=600x300&location={latitude},{longitude}&heading={azimuthalAngle}&pitch=0.0&fov=90&key={GoogleMapsApiKey.GoogleMapsApiKey}")
