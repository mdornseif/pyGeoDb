default: pygeodb/plzdata.py

cleanup:
	2to3-2.6 -w -f zip -f xreadlines -f xrange -f ws_comma -f throw -f standarderror -f set_literal \
	-f repr -f renames -f reduce -f raise -f paren -f nonzero -f ne -f itertools_imports -f itertools \
	-f isinstance  -f idioms -f has_key -f getcwdu -f filter -f except .

pygeodb/plzdata.py: data/plz.txt
	PYTHONPATH=. python contrib/createDB.py < data/plz.txt > pygeodb/plzdata.py
