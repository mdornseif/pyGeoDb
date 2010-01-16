#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created by Christioan Klein in 2007
# BSD licensed

"""
1) alle GeoLocations in einem PLZ-Gebiet:

GeoLocation.select(GeoLocation.q.Zipcode == zipcode)
oder
GeoLocation.select(GeoLocation.q.Zipcode.startswith(zipcode))

2) Distanz zwischen zwei GeoLocations

geoloc_1 = GeoLocation.select()[0]
geoloc_2 = GeoLocation.select()[0]

distance = geoloc_1 - geoloc_2
(Reihenfolge spielt keine Rolle)

3) GeoLocations sortiert nach Distanz zu einem Referenzpunkt:

referenz = GeoLocation.select()[0]
locations = GeoLocation.select()

distanz_liste = sort(locations, referenz)
"""

from sqlobject import *
import math
import operator

class GeoLocation(SQLObject):
    """The python object for a geolocation"""
    Zipcode = StringCol(length=10, varchar=True)
    #City = StringCol(length=200, varchar=True)
    Country = StringCol(length=200, varchar=True)
    Latitude = FloatCol()
    Longitude = FloatCol()

    def __sub__(self, other):
        """Calculates the distance between two geolocations"""
        fLat, fLon = math.radians(self.Latitude), math.radians(self.Longitude)
        tLat, tLon = math.radians(other.Latitude), math.radians(other.Longitude)

        distance = math.acos( math.sin(tLat) * math.sin(fLat) + math.cos(tLat) * math.cos(fLat) * math.cos(tLon
- fLon)) * 6380

        return distance

def sort(locations, reference):
    """Return a sorted list of GeoDBLocation objects. The list is in ascending order
of the distance relative to the reference location. The reference location must be a GeoDBLocation object"""
    distances = {}
    for location in locations:
        #distances[location.id] = reference - location
        distances[location.Zipcode] = reference - location

    items = distances.items()
    items.sort(key = operator.itemgetter(1))

    return items
