'''
Created on 26 Nov 2013

@author: AlphanumericSheepPig
'''



class ShearTensor ():
    def __init__(self):
        self.tensor = [[0,0],[0,0]]
        
    def calculate(self):
        # Apply a Newtonion model, using finite differences for the spacial derivatives
        return self
    
    def getElem(self, i, j):
        return self.tensor[i][j]
    
    def xx(self):
        return self.tensor[0][0]
    
    def xy(self):
        return self.tensor[0][1]
        
    def yx(self):
        return self.tensor[1][0]
    
    def yy(self):
        return self.tensor[1][1]
        
        