'''
Created on 26 Nov 2013

@author: AlphanumericSheepPig
'''


import math
from pycfdmesh.geometry import Point, BoundingBox, PointList, Polygon



class Element():
    '''
    The Element object is a Quadtree. Each element may potentially be split into four smaller elements.
    If the element is polled for anything, then it will return it's value only if it is a leaf. Otherwise,
    it will poll its children instead and pass on the result. 
    '''
    
    def __init__(self, center, cellSize, maxCellSize, minCellSize, parent = None):
        self.isLeaf = True
        
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
        if self.neighbour[direction]:
            self.neighbour[direction] = self.neighbour[direction].getElementAtPoint(neighbourLocation)
            return self.neighbour[direction]
        else:
            self.neighbour[direction] = self.parent.getElementAtPoint(neighbourLocation)
            return self.neighbour[direction]
        

    
    def getElementAtPoint(self, point):
        '''
        Gets the leaf element that contains a point.
        '''
        # Start of by checking if this element contains the point. If not, there's no need to go further, but
        # presumably, some element somewhere needs an answer. So, we ask the parent to find it for us.
        if not self.boundingBox.containsPoint(point):
            return self.parent.getElementAtPoint(point)
            
        if self.isLeaf:
            return self
        else:
            for child in self.children:
                # We MUST ensure that we only poll the child that definitely contains the point, otherwise
                # it will poll it's parent (this instance), which will poll the child again, and so on.
                if child.boundingBox.containsPoint(point):
                    return child.getElementAtPoint(point)
        
    
    def getPointList(self):
        '''
        If its a leaf, this returns points for drawing a closed loop around the cell. Otherwise, it 
        returns a list of points for all of its children.
        '''
        if self.isLeaf:
            return self.boundingBox.getPointList()
        else:
            pointList = PointList()
            for child in self.children:
                pointList += child.getPointList()
            return pointList
            
            
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
            else:
                print("Cell is already too small")
        else:
            print("Something went wrong with splitting a cell")
    
    
    
        
    def __repr__(self):
        return "Element at "+str(self.center)+" with size "+str(self.cellSize)
    
    
    
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
                center = Point(maxCellSize/2 + i*maxCellSize, maxCellSize/2 + j*maxCellSize)
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
    
    
    def removeShape(self, polygon):
        pass
        