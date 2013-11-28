'''
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