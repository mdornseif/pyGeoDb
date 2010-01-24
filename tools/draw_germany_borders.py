#!/usr/bin/env python
# encoding: utf-8
"""
draw_germany_borders.py Draws germany

Created by Maximillian Dornseif on 2010-01-18.
Copyright (c) 2010 HUDORA. All rights reserved.
"""

import random, math, sys
from optparse import OptionParser
import cairo
import pygeodb
from pprint import pprint

def intRGB(r, g, b):
        return (r/255.0, g/255.0, b/255.0)

class NiceCtx(cairo.Context):
    defaultBorderColour = intRGB(0x7d/255.0, 0x7d/255.0, 0x7d/255.0)
    def stroke_border(self, border):
        src = self.get_source()
        width = self.get_line_width()
        self.set_source_rgba(*self.defaultBorderColour)
        self.stroke_preserve()
        self.set_source(src)
        self.set_line_width(width - (border * 2))
        self.stroke()
        
    def init_geoscale(self, minx, xwidth, miny, yheigth):
        self.minx = minx
        self.miny = miny
        self.xwidth = xwidth
        self.yheigth = yheigth
        self.geoscalefactor = 1 / max([xwidth, yheigth])
        self.geoscalefactor = self.geoscalefactor
        
    def geoscale(self, x, y):
        # we use 1.35 for a very simple "projection"
        return (x-self.minx)*self.geoscalefactor, ((y-self.miny)*self.geoscalefactor*-1.35) + 1.35


class Canvas:
    def __init__(self, width, height, filename):
        self.width, self.height = width, height
        self.surface = cairo.PDFSurface(filename, width, height)
        self.background(1, 1, 1)

    def ctx(self):
        context = NiceCtx(self.surface)
        self.ctxscale = min([self.width, self.height])
        context.scale(self.ctxscale, self.ctxscale)
        self.ctxscale = 1/float(self.ctxscale)
        return context

    def background(self, r, g, b):
        c = self.ctx()
        c.set_source_rgb(r, g, b)
        c.rectangle(0, 0, self.width, self.height)
        c.fill()
        c.stroke()

    def save(self, fname, vertical):
        surf = self.surface
        #surf.write_to_png(fname)

c = Canvas(480, 640, 'deutschlandgrenzen.pdf')
ctx = c.ctx()
ctx.set_line_cap(cairo.LINE_CAP_ROUND)
ctx.set_line_join(cairo.LINE_JOIN_ROUND)

from pygeodb.borderdata import deutschgrenzen
geoitems = pygeodb.geodata['de'].items()

# find desired image size
x = []
y = []
for plz, (long, lat, name) in geoitems:
    x.append(long)
    y.append(lat)
for track in deutschgrenzen:
    for long, lat in track:
        x.append(long)
        y.append(lat)
ctx.init_geoscale(min(x), max(x)-min(x), min(y), max(y)-min(y))
ctx.set_antialias(cairo.ANTIALIAS_SUBPIXEL)
ctx.set_line_width(0.5*c.ctxscale)


borderskip = 10 # Borders are too detailed, only use 10% of data
# use borders as clipping region
for track in deutschgrenzen:
    ctx.move_to(*ctx.geoscale(*track[0]))
    for long, lat in track[1::borderskip]: 
        ctx.line_to(*ctx.geoscale(long, lat))
    ctx.close_path()
#mask_ctx.fill()
ctx.clip()

# draw borders
for track in deutschgrenzen:
    ctx.move_to(*ctx.geoscale(*track[0]))
    for long, lat in track[1::borderskip]: # Borders are too detailed, only use 20% of data
        ctx.line_to(*ctx.geoscale(long, lat))
    ctx.close_path()
ctx.stroke()

# draw centers of PLZ areas
for plz, (long, lat, name) in geoitems:
    if plz.startswith('422'):
        ctx.move_to(*ctx.geoscale(long, lat))
        ctx.close_path()
ctx.stroke()

# calculate voronoi diagram for plz areas
from pygeodb import voronoi
pts = []
for plz, (long, lat, name) in geoitems:
    if plz.startswith('422'):
        pts.append(voronoi.Site(long, lat))
        print(long, lat)

points, lines, edges, edges2input = voronoi.computeVoronoiDiagram(pts)

pprint(points)
pprint(lines)
pprint(edges)
pprint(edges2input)

print(pts[3].x, pts[3].y)
ctx.set_line_width(0.01*c.ctxscale)
for (l, p1, p2) in edges2input:
    if p1 == 3 or p2 == 3:
        print((l, p1, p2), points[p1], points[p2])
        ctx.move_to(*ctx.geoscale(*points[p1]))
        ctx.line_to(*ctx.geoscale(*points[p2]))
        ctx.stroke()
        
        
# draw voronoi diagram for plz areas
ctx.set_line_width(0.1*c.ctxscale)
for (l, p1, p2) in edges:
    x1 = y1 = x2 = y2 = None
    if p1 > -1:
        x1, y1 = points[p1]
    else:
        x2, y2 = points[p2]
        a, b, c = lines[l]
        print("%f*x + %f*y = %f" % (a, b, c))
        x1 = x2 - 0.25
        y1 = -1 * ((a*x1 - c) / b)
    if p2 > -1:
        x2, y2 = points[p2]
    else:
        a, b, c = lines[l]
        print("%f*x + %f*y = %f" % (a, b, c))
        x2 = x1 + 0.25
        y2 = -1 * ((a*x2 - c) / b)
    if x1 and y1 and x2 and y2:
        print(x1, y1, x2, y2)
        ctx.move_to(*ctx.geoscale(x1, y1))
        ctx.line_to(*ctx.geoscale(x2, y2))
        ctx.stroke()

# image background
ctx.show_page()
#ctx.fill()
