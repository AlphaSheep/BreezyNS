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



Created on 26 Nov 2013

@author: AlphanumericSheepPig
'''


import math
from pycfdmesh.geometry import Point, BoundingBox, PointList#, Polygon
from pycfdalg.usefulstuff import removeDuplicates



class Element():
    '''
    The Element object is a Quadtree. Each element may potentially be split into four smaller elements.
    If the element is polled for anything, then it will return it's value only if it is a leaf. Otherwise,
    it will poll its children instead and pass on the result. 
    '''
    
    def __init__(self, center, cellSize, maxCellSize, minCellSize, parent = None):
        self.isLeaf = True
        self.isSolid = None
        self.isBoundary = False
        self.Boundary = None
        
        self.parent = parent
        self.children = []
        
        self.cellSize = cellSize
        self.maxCellSize = maxCellSize
        self.minCellSize = minCellSize
        
        self.center = center
        self.boundingBox = BoundingBox(center, cellSize/2)
        
        # We need a simple, direction-agnostic way of storing our neighbours.
        self.neighbours = {'up':None, 'down':None, 'left':None, 'right':None}
        
        #print("    Created new element at",center,"with size",cellSize)
    
    
    def getBoundingBox(self):
        return self.boundingBox 
    
    def getNeighbour(self, direction):
        '''
        Returns the element located immediately above, by finding the element (cellSize+minCellSize)/2 away.
        "direction" is a string that's either 'up', 'down', 'left' or 'right'.
        '''
        distance = (self.cellSize+self.minCellSize)/2

        if direction == 'up':
            queryPoint = Point(0,1)
        elif direction == 'down':
            queryPoint = Point(0,-1)
        elif direction == 'left':
            queryPoint = Point(-1,0)
        elif direction == 'right':
            queryPoint = Point(1,0)
        else:
            # This also serves as a check to see that the direction is a valid key for the neighbour dict.
            raise Exception("Error: Cannot interpret direction given while trying to find a neighbour.")
        
        neighbourLocation = self.center + queryPoint.scaledBy(distance)
        
        # If we've found a neighbour before, then we can save time by querying them directly to see if it's changed.
        # If we don't have a neighbour yet, we'll ask our parent if they can find our neighbour for us.
        if self.neighbours[direction]:
            self.neighbours[direction] = self.neighbours[direction].getElementAtPoint(neighbourLocation)
            return self.neighbours[direction]
        else:
            self.neighbours[direction] = self.parent.getElementAtPoint(neighbourLocation)
            return self.neighbours[direction]
        
        
    def getAllElements(self):
        '''
        Returns a list of all leaf elements within the current element.
        '''
        if self.isLeaf:
            if self.isSolid:
                return []
            return [self]
        else:
            elementList = []
            for c in self.children:
                elementList += c.getAllElements()
            return elementList
            
    
    def getElementAtPoint(self, point):
        '''
        Gets the leaf element that contains a point.
        '''
        # Start of by checking if this element contains the point. If not, there's no need to go further, but
        # presumably, some element somewhere needs an answer. So, we ask the parent to find it for us.
        if not self.boundingBox.containsPoint(point):
            return self.parent.getElementAtPoint(point)
            
        if self.isLeaf:
            if self.isSolid:
                return None
            return self
        else:
            for child in self.children:
                # We MUST ensure that we only poll the child that definitely contains the point, otherwise
                # it will poll it's parent (this instance), which will poll the child again, and so on.
                if child.boundingBox.containsPoint(point):
                    return child.getElementAtPoint(point)
        
    
    def getPointList(self):
        '''
        If its a leaf, this returns the points defining the corners of the cell. Otherwise, it 
        returns a list of points for all of its children.
        '''
        if self.isLeaf:
            if self.isSolid:
                return PointList()
            return self.boundingBox.getPointList()
        else:
            pointList = PointList()
            for child in self.children:
                pointList += child.getPointList()
            return pointList
    
    
    def getPolygons(self):
        '''
        Returns a list of Polygon objects defining each leaf element.
        '''
        if self.isLeaf:
            if self.isSolid:
                return []
            return [self.boundingBox.getPolygon()]
        else:
            polyList = []
            for child in self.children:
                polyList += child.getPolygons()
            return polyList
        
            
    def split(self):
        if self.isLeaf:
            newCellSize = self.cellSize/2
            if newCellSize > self.minCellSize:
                self.isLeaf = False
                topLeft     = Point(self.center.x - newCellSize/2, self.center.y + newCellSize/2)
                topRight    = Point(self.center.x + newCellSize/2, self.center.y + newCellSize/2) 
                bottomRight = Point(self.center.x + newCellSize/2, self.center.y - newCellSize/2)
                bottomLeft  = Point(self.center.x - newCellSize/2, self.center.y - newCellSize/2)
                self.children.append(Element(topLeft, newCellSize, self.maxCellSize, self.minCellSize, self))
                self.children.append(Element(topRight, newCellSize, self.maxCellSize, self.minCellSize, self))
                self.children.append(Element(bottomRight, newCellSize, self.maxCellSize, self.minCellSize, self))
                self.children.append(Element(bottomLeft, newCellSize, self.maxCellSize, self.minCellSize, self))
                for c in self.children:
                    c.fixNeighbourCellSizes()
    
    
    def getNeighbours(self):
        directions = ['up','down','left','right']
        neighbours = []
        for d in directions:
            neighbours.append(self.getNeighbour(d))
        return neighbours
        
    
    def fixNeighbourCellSizes(self):
        '''
        Checks the cell size of all neighbouring elements. If any of them are larger than twice the current cell size, 
        then they are refined until they meet this criteria.
        '''
        
        directions = ['up','down','left','right']
        
        for d in directions:
            n = self.getNeighbour(d)
            if n: # There won't be any neighbour on the edge.
                #print ("Checking",n, "since it's a neighbour of",self)
                while self.isLeaf and n.cellSize > 2*self.cellSize: 
                    #print ("    ",n,"is too large.")
                    n.split()
                    n = self.getNeighbour(d)
                    
                    
    def __repr__(self):
        if self.isSolid: 
            solid = "Solid. " 
        else:
            solid = ""
        if self.isBoundary:
            boundary = " Boundary. "
        else:
            boundary = ""
        
         
        return "Element at "+str(self.center)+" with size "+str(self.cellSize)+". "+solid+boundary
    
    
    
class Mesh():
    '''
    The mesh object contains a uniform cartesian grid of the largest possible cell size.
    "Mesh.elements" contains a list of the root Elements.
    The (i,j)th root element, is given by "Mesh.elements[j*horizontalCellCount+i]".
    '''

    def __init__(self, bottomLeft, horizontalCellCount, verticalCellCount, maxCellSize, minCellSize):
        '''
        "bottomLeft" is a Point, and an n x m mesh of square cells with dimension maxCellSize is generated above
        and to the right of this point, where n is given by "horizontalCellCount" and m is "verticalCellCount".
        '''
        self.horizontalCellCount = horizontalCellCount
        self.verticalCellCount = verticalCellCount
        self.maxCellSize = maxCellSize
        self.minCellSize = minCellSize
        
        elements = []
        for i in range(horizontalCellCount):
            for j in range(verticalCellCount):
                center = bottomLeft + Point(maxCellSize/2 + i*maxCellSize, maxCellSize/2 + j*maxCellSize)
                elements.append(Element(center, maxCellSize, maxCellSize, minCellSize, self))
        self.elements = elements
        self.bottomLeft = bottomLeft
        
        width = horizontalCellCount*maxCellSize/2
        height = verticalCellCount*maxCellSize/2
        center = bottomLeft + Point(width, height)
        
        self.boundingBox = BoundingBox(center, width, height)
    
    
    def getElementAtPoint(self, point):
        '''
        Returns a leaf Element which contains the point.
        '''
        # First, we check that the point does fall inside the mesh.
        if not self.boundingBox.containsPoint(point):
            return None
        
        # Since the root elements in the mesh have a fixed size and spatial arrangement, it's simple to 
        # figure out which root element a point is in without having to poll any other elements.
        
        # Start by converting the point in (x,y) in global units into a relative coord (i,j) measured in cell counts.
        relativeLocation = (point - self.bottomLeft).scaledBy(1/self.maxCellSize)
        i = math.floor(relativeLocation.x)
        j = math.floor(relativeLocation.y)
        
        # Figure out which element that is.
        e = self.elements[i*self.verticalCellCount+j]
             
        # As a safety net, we check that the element does contain the point. If it doesn't, we risk infinite 
        # recursion. There's probably something wrong if that happens, so let's raise an exception.
        if e.boundingBox.containsPoint(point):
            return e.getElementAtPoint(point)
        else:
            print("Need to query an element",e,"for a point ",point,", but it's the wrong element.")
            raise Exception("Fatal Error: Parent mesh attempted to query an element for a point it did not contain.")
    
    
    def getPolygons(self):
        '''
        Returns a list of Polygon objects defining each leaf element.
        '''
        polyList = []
        for e in self.elements:
            polyList += e.getPolygons()
        return polyList
        

    def getElementsAroundPoint(self, point, distance=None):
        '''
        Returns a list of elements containing the element at point, and the four elements distance in each direction.
        If distance is not specified, it defaults to minCellSize/2
        '''

        if not distance:
            distance = self.minCellSize/2
        
        up     = self.getElementAtPoint(point + Point( 0, 1).scaledBy(distance))
        down   = self.getElementAtPoint(point + Point( 0,-1).scaledBy(distance))
        left   = self.getElementAtPoint(point + Point(-1, 0).scaledBy(distance))
        right  = self.getElementAtPoint(point + Point( 1, 0).scaledBy(distance))
        center = self.getElementAtPoint(point)
        
        return removeDuplicates([up, down, left, right, center])
    
    
    def refineAlongLine(self, line):
        # We calculate the number of steps needed to ensure that we don't miss any cells.
        nSteps = math.ceil(line.length()/self.minCellSize)
        if nSteps < 1:
            print('Got a line of length',line.length())
        # nSteps is the number of line segments. Number of points to check is nSteps + 1
        for i in range(nSteps+1):
            thisPoint = line.startPoint + (line.endPoint-line.startPoint).scaledBy(i/nSteps)
            
            e = self.getElementAtPoint(thisPoint)
            while e and e.cellSize/2 > e.minCellSize:
                for element in self.getElementsAroundPoint(thisPoint):
                    element.split()                    
                e = self.getElementAtPoint(thisPoint)
    
    
    def refineAlongPolygon(self, polygon):
        counter = 0
        for line in polygon.lines:
            counter += 1
            # print("    Resolving along line",counter,":", line)
            self.refineAlongLine(line)
            # print("      Detecting solid cells")
            self.markSolidCells(polygon)
    
    
    def getAllElements(self):
        elementList = []
        for e in self.elements:
            elementList += e.getAllElements()
        return elementList
    

            
    def markSolidCells(self, polygon):
        '''
        Marks all elements in polygon as solid.
        '''
        for e in self.getAllElements():
            if e.isSolid==None and polygon.containsBoundingBox(e.getBoundingBox()):
                e.isSolid = True
            else:
                e.isSolid = False
            

    
   
