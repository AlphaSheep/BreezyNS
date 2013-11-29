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

A module that provides a function to calculate pressure and internal energy based on flow variables in a solution vector.
'''



def pressure(solution, model = "IdealGas"):
    '''
    Calculates the pressure using the equation described by the "model" argument.
    Currently implemented models are:
        IdealGas: Uses equations for a calorifically perfect ideal gas. 
    '''
    
    # Extract primitive variables from the solution vector
    rho = solution.getDensity()
    vel = solution.getVelocity()
    e = solution.getTotalEnergy()

    if model == "IdealGas":
        gamma = 1.4
        speedsqr = vel.sumOfSquares()
        
        p = (gamma - 1)*rho*(e-speedsqr/2)
        
    else:
        raise Exception("The model ("+model+") specified for the pressure calculation was not recognised.")
    
    return p



if __name__ == "__main__":
    pass