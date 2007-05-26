#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os.path
from sqlobject import *
import huGeoDB

if __name__ == "__main__":

    if len(sys.argv) < 3:
        sys.stderr.write("Usage: %s textfile database\n" % (sys.argv[0]))
        sys.exit()


    # open textfile
    textfile = open(sys.argv[1])

    # open database
    
    db_filename = os.path.abspath(sys.argv[2])
    if os.path.exists(db_filename):
        os.unlink(db_filename)
    
    connection_string = 'sqlite:' + db_filename
    connection = connectionForURI(connection_string)
    sqlhub.processConnection = connection

    huGeoDB.GeoLocation.createTable()

    for line in textfile: #.readlines():
            if line[0] == "#": continue

            if line[-1] == "\n": line = line[:-1]
            values = line.split(";")
            
            # Feld 1: eindeutiger Schlüssel (Primary Key)
            # Felder 2 bis 8: hierarchische Verwaltungsgliederung, hier:
            #      Feld  2: Staat (DE == Deutschland)
            #      Feld  3: Bundesland, s.o.
            #      Feld  4: Regierungsbezirk
            #      Feld  5: Landkreis
            #      Feld  6: Verwaltungszusammenschluss
            #      Feld  7: Ort
            # Felder 8 und 9: Koordinaten:
            #      Feld 8: Längengrad
            #      Feld 9: Breitengrad
            # Feld 10: Postleitzahl
            #
            #
            
            newLocation = huGeoDB.GeoLocation(
                Zipcode=values[9],
                #City=values[7],
                Country=values[1],
                Longitude=float(values[7]),
                Latitude=float(values[8])
            )

    textfile.close()
            
