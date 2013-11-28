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



Created on 26 Nov 2013

@author: AlphanumericSheepPig

A module which provides a SolutionVector and FluxVector class.

The Navier-Stokes equations in 2D for adiabatic flow with no body forces may be written as:

dU/dt + dFx/dx + dFy/dy = 0

where dA/dn denotes the partial derivative of the vector A with respect to the independent variable n.

The solution vector U may be stored as SolutionVector object,
and the flux vectors Fx and Fy may be stored as FluxVector objects.  
'''

from pycfdsolver.stateequation import pressure
from pycfdsolver.basicvector import Vector
from pycfdsolver.shearstress import ShearTensor
        
    
            
class SolutionVector(Vector):
    '''
    A special case vector of length 4 for a 2d solution, with methods for extracting primitive variables.
    '''
    def __init__(self):
        Vector.__init__(self,4)
    
    def set(self, rho, vel, totalEnergy):
        Vector.set(self, rho, rho*vel.x(), rho*vel.y(), rho*totalEnergy)
        return self
        
    def getDensity(self):
        return self.getElem(0)
    
    def getVelocity(self):
        rho = self.getDensity()
        u = self.getElem(1)/rho
        v = self.getElem(2)/rho
        velocity = Vector(2)
        velocity.set(u,v)
        return velocity
        
    def getTotalEnergy(self):
        rho = self.getDensity()
        # Note that this energy term includes the kinetic energy. 
        # For internal energy, the kinetic energy still needs to be subtracted 
        return self.getElem(3)/rho

    def getPressure(self):
        return pressure(self)
        
        
        
    
class FluxVector(Vector):
    '''
    A special case vector of length 4 for mass, momentum and energy fluxes in a specific direction, with an additional
    method for automatically calculating the fluxes in that direction.
    '''
    def __init__(self, component):
        '''
        The "component" argument is used to determine which elements to use for automatic flux calculation
        and should be set to 0 for flux in the x direction, and 1 for flux in the y direction.
        The full set of NS equations should have one of each of these.
        '''
        Vector.__init__(self,4)
        if component in [0, 1]:
            self.component = component
        else:
            raise Exception("Flux vector component of 0 (x) or 1 (y) must be specified.")
        
        
    def calculate(self, solution):
        '''
        Calculates the mass, momentum and energy fluxes in a direction based on the provided solution.
        Convective and diffusive fluxes are combined for simplicity. 
        '''
        c = self.component
        
        rho = solution.getDensity()
        vel = solution.getVelocity()
        energy = solution.getTotalEnergy()
        pressure = solution.getPressure()
        
        stresses = ShearTensor().calculate()
        
        # The pressure must be included only in the momentum flux parallel to the component being considered.
        # So use a vector with pressure = p in this direction, and 0 in all other directions.
        if c == 0:
            pressureVector = [pressure, 0]
        elif c == 1:
            pressureVector = [0, pressure]
        
        # The expressions below come from Anderson (1995) p. 84.
        # Note one difference: energy here is total energy = internal + kinetic energy, 
        # so no need to add in kinetic energy again.
        
        massFlux = rho * vel.getElem(c)
        momentumFluxX = rho * vel.x()*vel.getElem(c) - stresses.getElem(c, 0) + pressureVector[0] 
        momentumFluxY = rho * vel.y()*vel.getElem(c) - stresses.getElem(c, 1) + pressureVector[1]
        energyFlux = rho*energy*vel.getElem(c) + pressure*vel.getElem(c) - stresses.getElem(c, 0)*vel.x() - stresses.getElem(c, 1)*vel.y()
    
        self.set(massFlux, momentumFluxX, momentumFluxY, energyFlux)
        
        return self
        
    

        
def test():
    v = Vector(4)
    v.set(1,4,5,5)
    
    print (v)


if __name__ == "__main__":
    test()