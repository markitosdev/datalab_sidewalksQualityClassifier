import geopandas

from imageProcessors.imageDataset.createImageDatasetFromDataFrameWithCoordinates import \
    createImageDatasetFromDataFrameWithCoordinates
from repopulateSidewalkGroups.geographicData.generateNewPointsCloseToExistentPoints import \
    generateNewPointsCloseToExistentPoints
import pandas as pd
import os


def generateRepopulatedImageDataset(geoDfSidewalkGroup, sidewalkGroupName: str, maximumImagesToCollect: int = 3000):
    dfSidewalkGroupNewGeographicPoints = generateNewGeographicPointsBySidewalkGroup(geoDfSidewalkGroup)
    os.mkdir(sidewalkGroupName)
    if len(dfSidewalkGroupNewGeographicPoints) <= 300:
        dfSidewalkGroupNewGeographicPointsSample = dfSidewalkGroupNewGeographicPoints.sample(maximumImagesToCollect).reset_index(drop=True)
    else:
        dfSidewalkGroupNewGeographicPointsSample = dfSidewalkGroupNewGeographicPoints.copy()
    createImageDatasetFromDataFrameWithCoordinates(dfSidewalkGroupNewGeographicPointsSample, f'repopulate_{sidewalkGroupName}')
    return


def generateNewGeographicPointsBySidewalkGroup(geoDfSidewalkGroup: geopandas.GeoDataFrame) -> pd.DataFrame:
    newGeographicPointsBySidewalkGroup = generateNewPointsCloseToExistentPoints(geoDfSidewalkGroup)
    dfNewGeographicPointsBySidewalkGroup = pd.DataFrame(newGeographicPointsBySidewalkGroup)
    dfNewGeographicPointsBySidewalkGroup['latitude'] = dfNewGeographicPointsBySidewalkGroup['point'].apply(lambda row: row.latitude)
    dfNewGeographicPointsBySidewalkGroup['longitude'] = dfNewGeographicPointsBySidewalkGroup['point'].apply(lambda row: row.longitude)
    return dfNewGeographicPointsBySidewalkGroup
