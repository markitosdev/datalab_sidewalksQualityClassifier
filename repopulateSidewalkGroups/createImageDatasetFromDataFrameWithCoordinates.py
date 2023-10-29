import os

from facade.getStreetViewImageMetadata import getStreetViewImageMetadata, StreetViewMetadataParams
from facade.getStreetViewStaticImage import getStreetViewStaticImage, StreetViewStaticImageParams
from imageProcessors.utils.joinImagesInFolder import joinImagesInFolder


def createImageDatasetFromDataFrameWithCoordinates(df, latitudeRowName: str, longitudeRowName: str, folderToStoreImages: str):
    failedCoordinates = []
    metadataPanoIds = set()
    repeatedPanos = []
    for index, row in df.iterrows():
        failed = False
        folderName = f'''{folderToStoreImages}/_{index}_{0}'''
        os.mkdir(f"{folderName}")
        for angle in [0, 90, 180, 270]:
            metadataResponse = getStreetViewImageMetadata(StreetViewMetadataParams(latitude=row[latitudeRowName], longitude=row[longitudeRowName], azimuthalAngle=angle))
            if metadataResponse.get('status') == 'ZERO_RESULTS':
                failed = True
                failedCoordinates.append({'latitude': row[latitudeRowName], 'longitude': row[longitudeRowName]})
                os.rmdir(folderName)
                break
            if (metadataResponse.get('pano_id') in metadataPanoIds) and angle == 0:
                failed = True
                repeatedPanos.append({'latitude': row[latitudeRowName], 'longitude': row[longitudeRowName]})
                os.rmdir(folderName)
                break
            metadataPanoIds.add(metadataResponse.get('pano_id'))
            response = getStreetViewStaticImage(StreetViewStaticImageParams(latitude=row[latitudeRowName], longitude=row[longitudeRowName], azimuthalAngle=angle))
            saveSingleImageInFolderByIndexAngleAndScore(response, folderName, index, angle)
        if not failed:
            joinImagesInFolder(folderToStoreProcessedImage=folderToStoreImages, index=index, score=0, imagesFolderName=folderName)
    print(f"you removed {len(repeatedPanos)} repeated images and {len(failedCoordinates)} failed images")


def saveSingleImageInFolderByIndexAngleAndScore(response, folderName: str, index: float, angle: float, score=0):
    file = open(f"{folderName}/{index}_{angle}_{0}.png", "wb")
    file.write(response.content)
    file.close()