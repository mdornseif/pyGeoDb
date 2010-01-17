default: pygeodb/borderdata.py pygeodb/plzdata.py

cleanup:
	2to3-2.6 -w -f zip -f xreadlines -f xrange -f ws_comma -f throw -f standarderror -f set_literal \
	-f repr -f renames -f reduce -f raise -f paren -f nonzero -f ne -f itertools_imports -f itertools \
	-f isinstance  -f idioms -f has_key -f getcwdu -f filter -f except .

pygeodb/borderdata.py: data/de_landmasse_osm_relation_62781.gpx tools/grenzen2python.py
	PYTHONPATH=. python tools/grenzen2python.py > pygeodb/borderdata.py

pygeodb/plzdata.py: data/opengeodb_plz.txt tools/plz2python.py
	PYTHONPATH=. python tools/plz2python.py < data/opengeodb_plz.txt > pygeodb/plzdata.py
