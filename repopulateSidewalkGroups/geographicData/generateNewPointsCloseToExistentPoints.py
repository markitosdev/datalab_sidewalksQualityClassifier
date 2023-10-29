import random

import geopandas
import geopy.distance


def generateNewPointsCloseToExistentPoints(geoDfCurrentPoints: geopandas.GeoDataFrame, sideWalkScoreColumnName: str = 'roundSideWalkScore',
                                           geographicPointsToCollectByScore: float = 300, radiusLowerLimit: float = 50,
                                           radiusUpperLimit: float = 100):
    newGeographicPoints = []
    for roundScore in geoDfCurrentPoints[sideWalkScoreColumnName].unique():
        gDfByScore = geoDfCurrentPoints[geoDfCurrentPoints[sideWalkScoreColumnName] == roundScore].reset_index(drop=True).copy()
        records = len(gDfByScore[sideWalkScoreColumnName]) - 1
        for tryIndex in range(0, geographicPointsToCollectByScore):
            randomRecordIndex = int(round(random.uniform(0, records), 0))
            randomDistanceAmount = round(random.uniform(radiusLowerLimit, radiusUpperLimit), 2)
            randomDistance = geopy.distance.GeodesicDistance(kilometers=randomDistanceAmount / 1000)
            randomAngle = round(random.uniform(0, 360), 2)
            newGeographicPoint = randomDistance.destination(gDfByScore['sideWalkPoint'].iloc[randomRecordIndex],
                                                            bearing=randomAngle)
            newGeographicPoints.append(
                {'point': newGeographicPoint, 'score': gDfByScore['Calificación Banquetas'].iloc[randomRecordIndex],
                 'originLatitude': gDfByScore['X02_Latitud'].iloc[randomRecordIndex],
                 'originLongitude': gDfByScore['X03_Longitud'].iloc[randomRecordIndex]})
    return newGeographicPoints
