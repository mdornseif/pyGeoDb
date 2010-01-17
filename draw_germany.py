#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random, math, sys
from optparse import OptionParser
import cairo
import pygeodb
from pprint import pprint

def intRGB(r, g, b):
        return (r/255.0, g/255.0, b/255.0)

HIGHLIGHT=intRGB(0xff, 0x72, 0x72)

class NiceCtx(cairo.Context):
    defaultBorderColour = intRGB(0x7d, 0x7d, 0x7d)
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
    def __init__(self, width, height):
        self.width, self.height = width, height
        self.surface = cairo.PDFSurface('test.pdf', width, height)
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

c = Canvas(480, 640)
ctx = c.ctx()
ctx.set_line_cap(cairo.LINE_CAP_ROUND)
ctx.set_line_join(cairo.LINE_JOIN_ROUND)
# ctx.set_source_rgb(*HIGHLIGHT)

geoitems = pygeodb.geodata['de'].items()

# find desired image size
x = []
y = []
for plz, (long, lat, name) in geoitems:
    x.append(long)
    y.append(lat)
ctx.init_geoscale(min(x), max(x)-min(x), min(y), max(y)-min(y))
ctx.set_antialias(cairo.ANTIALIAS_SUBPIXEL)
ctx.set_line_width(0.3*c.ctxscale)



# see http://lists.cairographics.org/archives/cairo/2009-June/017459.html for drawing points
for plz, (long, lat, name) in geoitems:
    ctx.move_to(*ctx.geoscale(long, lat))
    ctx.close_path()
ctx.stroke()

import voronoi
pts = []
for plz, (long, lat, name) in geoitems:
    pts.append(voronoi.Site(long,lat))

points, lines, edges = voronoi.computeVoronoiDiagram(pts)

pprint(points)
pprint(lines)
pprint(edges)

ctx.set_line_width(0.1*c.ctxscale)

for (l, p1, p2) in edges:
    x1 = y1 = x2 = y2 = None
    if p1 > -1:
        x1, y1 = points[p1]
    if p2 > -1:
        x2, y2 = points[p2]
    if p1 > -1 and p2 > -1:
        print "(%f, %f) -> (%f, %f)" % (x1, y1, x2, y2)
        ctx.move_to(*ctx.geoscale(x1, y1))
        ctx.line_to(*ctx.geoscale(x2, y2))
        ctx.stroke()

ctx.fill()
