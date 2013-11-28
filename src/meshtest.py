'''
This file is a part of BreezyNS - a simple, general-purpose 2D airflow calculator.

BreezyNS is copyright (c) 2013, Brendan Gray

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.


Created on 27 Nov 2013

@author: AlphanumericSheepPig
'''

import pylab
from pycfdmesh.mesh import Mesh
from pycfdmesh.geometry import Point
# from pycfdmesh.svgloader import polygonsFromSVG


def plotPolygons(polygons, style='k-'):
    for poly in polygons:
        points = poly.getDefiningPoints()
        pylab.plot(points.getXs(), points.getYs(),style)


def plotMesh(mesh, style='k-'):
    polygons = mesh.getPolygons()
    for poly in polygons:
        points = poly.getDefiningPoints()
        pylab.plot(points.getXs(), points.getYs(),style)
    
    
    
def test():
    bottomLeft = Point(0,0)
    mesh = Mesh(bottomLeft, 10, 10, 100, 1)
    print("Mesh generated\n")
    mesh.getElementAtPoint(Point(320,220)).split()
    mesh.getElementAtPoint(Point(320,220)).split()
    mesh.getElementAtPoint(Point(320,220)).split()
    mesh.getElementAtPoint(Point(320,220)).split()
    mesh.getElementAtPoint(Point(320,220)).split()
    mesh.getElementAtPoint(Point(320,220)).split()

    
    e = mesh.getElementAtPoint(Point(320,220))
    up = e.getNeighbour('up')
    down = e.getNeighbour('down')
    left = e.getNeighbour('left')
    right = e.getNeighbour('right')

    print("Plotting...\n")
    
    pylab.figure()
    plotMesh(mesh)
    #plotMesh(up,'go-')
    #plotMesh(down,'bo-')
    #plotMesh(left,'co-')
    #plotMesh(right,'mo-')
    plotMesh(e,'ro-')
    pylab.axis('equal')
    pylab.show()
    
    
from pycfdmesh.svgloader import beziergonsFromSVG



test()