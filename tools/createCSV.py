#!/usr/bin/env python

# quick and dirty to convert from db to txt that can
# be parsed by createDB.py

import sys
import string

ifile = open(sys.argv[1])

ofile = open(sys.argv[2], "w")
linec = 0
for line in ifile:
    if line[-1] == "\n":
        line = line[:-1]
    linec += 1
    pll = line.split("|")

    # map(str, pll)
    plz, lon, lat = map(string.strip, pll)

    # Feld 1: eindeutiger Schl�ssel (Primary Key)
    # Felder 2 bis 8: hierarchische Verwaltungsgliederung, hier:
    #      Feld  2: Staat (DE == Deutschland)
    #      Feld  3: Bundesland, s.o.
    #      Feld  4: Regierungsbezirk
    #      Feld  5: Landkreis
    #      Feld  6: Verwaltungszusammenschluss
    #      Feld  7: Ort
    # Felder 8 und 9: Koordinaten:
    #      Feld 8: L�ngengrad
    #      Feld 9: Breitengrad
    # Feld 10: Postleitzahl

    values = ("1", "AT", "", "", "", "", "", lon, lat, plz)

    ofile.write("%s\n" % (";".join(values)))
ofile.close()
