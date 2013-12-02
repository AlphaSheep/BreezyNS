'''
This file is a part of BreezyNS - a simple, general-purpose 2D airflow calculator.

Copyright (c) 2013, Brendan Gray

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
# import math
from geomtest import plotPolygonGroup
from pycfdmesh.mesh import Mesh
from pycfdmesh.geometry import Point
from pycfdmesh.svgloader import polygonsFromSVG


def plotPolygons(polygons, style='k-'):
    for poly in polygons:
        points = poly.getDefiningPoints()
        pylab.plot(points.getXs(), points.getYs(),style)


def plotMesh(mesh, style='k-'):
    polygons = mesh.getPolygons()
    for poly in polygons:
        points = poly.getDefiningPoints()
        pylab.plot(points.getXs(), points.getYs(),style)
    

    
def testMeshRefinement():
    bottomLeft = Point(0,0)
    mesh = Mesh(bottomLeft, 10, 10, 100, 1)
    print("Mesh generated\n")
    
    refinePoint = Point(500,500)
    
    mesh.getElementAtPoint(refinePoint).split()
    mesh.getElementAtPoint(refinePoint).split()
    mesh.getElementAtPoint(refinePoint).split()
    mesh.getElementAtPoint(refinePoint).split()
    mesh.getElementAtPoint(refinePoint).split()
    mesh.getElementAtPoint(refinePoint).split()

    
    e = mesh.getElementAtPoint(refinePoint)
    #up = e.getNeighbour('up')
    #down = e.getNeighbour('down')
    #left = e.getNeighbour('left')
    #right = e.getNeighbour('right')

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



        


def testPloygonTracer():
    minCellSize = 5
    polygon = polygonsFromSVG('./inputgeometries/arbshape6.svg', minCellSize)[0]
    print("Loaded geometry as polygon with",len(polygon.lines),"sides.")
    bottomLeft = Point(0, 300)
    mesh = Mesh(bottomLeft, 10, 10, 100, minCellSize)
    print("Generated coarse background mesh.")
    mesh.refineAlongPolygon(polygon)
    print("Mesh refined around geometry.")
    mesh.markSolidCells(polygon)
    print("Solid cells identified.")
    
    
    pylab.figure()
    
    print("Plotting mesh...")
    plotMesh(mesh)
    print("Plotting geometry...")
    plotPolygonGroup([polygon],'r-')

    pylab.axis('equal')
    pylab.show()
    






if __name__ == "__main__":    
    #testMeshRefinement()
    testPloygonTracer()
