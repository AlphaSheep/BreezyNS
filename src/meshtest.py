'''
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