default: test

test: data
	PYTHONPATH=. python -c 'import doctest; doctest.testfile("README.rst")'

cleanup: # this does NOT convert to python 3.x
	2to3-2.6 -w -f zip -f xreadlines -f xrange -f ws_comma -f throw -f standarderror -f set_literal \
	-f repr -f renames -f reduce -f raise -f paren -f nonzero -f ne -f itertools_imports -f itertools \
	-f isinstance  -f idioms -f has_key -f getcwdu -f filter -f except -f print .

pygeodb/borderdata.py: data/de_landmasse_osm_relation_62781.gpx tools/grenzen2python.py
	PYTHONPATH=. python tools/grenzen2python.py > pygeodb/borderdata.py

pygeodb/plzdata.py: data/opengeodb_plz.txt tools/plz2python.py
	PYTHONPATH=. python tools/plz2python.py data/opengeodb_plz.txt pygeodb/plzdata.py

data: pygeodb/borderdata.py pygeodb/plzdata.py

maps: data
	python ./plz_draw --frontier --borders maps/deutschland_gebiete.pdf
	python ./plz_draw --frontier --borders --width=1440 --heigth=1920 maps/deutschland_gebiete.png
	#python ./plz_draw --frontier --borders maps/deutschland_gebiete.svg
	#python ./plz_draw --frontier --borders maps/deutschland_gebiete.eps
	#python ./plz_draw --frontier --borders maps/deutschland.ps

	python ./plz_draw --frontier --center=250 maps/deutschland.pdf
	python ./plz_draw --frontier --center=250 --width=1440 --heigth=1920 maps/deutschland.png

clean:
	rm pygeodb/borderdata.py pygeodb/plzdata.py maps/*

.PHONY: maps data
