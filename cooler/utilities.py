import numpy as np

def threePointCubicApprox(x,y,xSlopePoint,yPrime):
    C3 = (y[2] - y[0])/((x[2] - x[1])*(x[2] - x[0])**2) - (y[1] - y[0])/((x[2] - x[1])*(x[1] - x[0])**2) + yPrime/((x[1]-x[0])*(x[2] - x[0]))
    C2 = (((y[1] - y[0])/(x[1] - x[0])) - yPrime)/(x[1] - x[0]) - C3*(2*x[0] + x[1])
    C1 = yPrime - 2*C2*x[0] - 3*C3*x[0]**2
    C0 = y[0] - C1*x[0] - C2*x[0]**2 - C3*x[0]**3

    return [C0,C1,C2,C3]

def threePointQuadraticApprox(x, y):
    #Inputs: Vector of x values and y values. These vectors must be equal length
    #Outputs: Coefficients for polynomial equation according to the form C0 + C1*x + C2*x^2...
    C2 = (((y[2]-y[0])/(x[2]-x[0])) - ((y[1]-y[0])/(x[1]-x[0])))/(x[2]-x[1])
    C1 = (y[1] - y[0])/(x[1]-x[0]) - C2*(x[0]+x[1])
    C0 = y[0] - C1*x[0] - C2*x[0]**2

    return [C0,C1,C2]

def twoPointLinearApprox(x, y):
    #Inputs: Vector of x values and y values. These vectors must be equal length
    #Outputs: Coefficients for polynomial equation according to the form C0 + C1*x + C2*x^2...
    C1 = (y[1] - y[0])/(x[1]-x[0])
    C0 = y[0] - C1*x[0]
    return [C0,C1]

def getValueOfPoly(c,x):
    #Inputs: Coefficients for polynomial equation according to the form C0 + C1*x + C2*x^2...
    #Inputs: x - value to get value at
    constantQuantity = len(c)

    if constantQuantity == 1:
        # Flat line
        y = c[0]
    elif constantQuantity == 2:
        # Linear
        y = c[0] + c[1] * x
    elif constantQuantity == 3:
        # Quadratic
        y = c[0] + c[1]*x + c[2]*x**2
    elif constantQuantity == 4:
        # Cubic
        y = c[0] + c[1]*x + c[2]*x**2 + c[3]*x**3
    else:
        print("Polynomial could not be calculated. Check getValueOfPoly function.")
        y = 99999999

    return y

def gradient(function,inputs,delta=0.0001,normalize=False):
    '''returns a list of partial gradients of the function around the input point'''
    # Inputs: function is a python function that accepts only a list of inputs as arguments
    # Inputs is a list representing the point at which to evaluate the function.
    # Optional: delta is the numerical step size of the gradient approximation
    # Normalize returns the slope of each partial of the gradient divided by the total slope

    slopeValues = []
    for i in range(0,len(inputs)):
        negativeInputs = list(inputs)
        negativeInputs[i] = float(negativeInputs[i]) - float(delta)
        negativePoint = function(negativeInputs)

        positiveInputs = list(inputs)
        positiveInputs[i] = float(positiveInputs[i]) + float(delta)
        positivePoint = function(positiveInputs)

        slope = (positivePoint - negativePoint)/(2*delta)
        slopeValues.append(slope)

    if normalize == True:
        totalSlope = vlen(slopeValues)
        for i in range(0,len(slopeValues)):
            slopeValues[i] = slopeValues[i]/totalSlope
    return slopeValues

def minimizeCubic(c):
    # Inputs: Coefficients for polynomial equation according to the form C0 + C1*x + C2*x^2 + C3*x^3
    # Outputs: Values of x and y where y is minimized
    a = 3*c[3]
    b = 2*c[2]
    d = c[1]
    insideSqareroot = np.float64(b*b-4*a*d)
    if insideSqareroot < 0:
        print("Minimize Cubic function encountered imaginary square root. Aborting.")
        return
    x1 = (-b+np.sqrt(insideSqareroot))/(2*a)
    x2 = (-b-np.sqrt(insideSqareroot))/(2*a)

    x = 0
    y = 0

    y1 = approx.getValueOfPoly(c,x1)
    y2 = approx.getValueOfPoly(c,x2)
    if y1 < y2:
        x = x1
        y = y1
    elif y1 > y2:
        x = x2
        y = y1
    else:
        x = x1
        y = y1
        print("More than one solution in Minimize Cubic")
    return (x,y)

def minimizeParabola(c):
    # Inputs: Coefficients for polynomial equation according to the form C0 + C1*x + C2*x^2...
    # Outputs: Values of x and y where y is minimized
    minX = -c[1]/(2*c[2])
    minY = getValueOfPoly(c,minX)
    return (minX,minY)

def minimize(function, startingPoint, epsilon=0.0001, nMax=1000, damping=1, echo=False, parabolaFitStepSize = 0.1, constantStepSize = 0.1, force_constant_step = False,**kwargs):
    '''minimizes output of function using steepest descent method'''
    # Inputs: python function which returns a single value and takes an input of a list of values
    # Variables is a list of text inputs for each input variable
    # StartingPoint is a vector of intial points for each input variable
    # Convergence and timeout parameters are optional
    alpha = [-parabolaFitStepSize,0,parabolaFitStepSize]
    i = 0

    # Loop
    shouldContinue = True
    position = startingPoint
    objectiveValue = function(position)
    if echo:
        headerString = "Iteration\tPosition\t"
        headerString += "Gradient\t"
        headerString += "F(x)"
        print(headerString)

    while shouldContinue == True:
        i = i+1
        # Get gradient at position
        slopeList = gradient(function,position)
        # Get three points in that direction at positions of alpha
        functionValues = []
        for alphaValue in alpha:
            testLocation = []
            for oldPosition, slope in zip(position,slopeList):
                testLocation.append(oldPosition-slope*alphaValue)
            functionValues.append(function(testLocation))
        # Fit parabola to curve
        C = threePointQuadraticApprox(alpha, functionValues)
        # Check parabola is concave up
        # Calculate alpha that gives minimum
        alphaStar = 0.0
        if C[2] < 0:
            if echo: print("Fitted parabola is concave down. Minimum alpha value is not bounded.")
            alphaStar = constantStepSize
        elif abs(C[2]) < 0.001 or force_constant_step == True:
            if echo: print("Shallow gradient, using constant step size")
            alphaStar = constantStepSize
        else:
            (alphaStar,bestY) = minimizeParabola(C)
        # Move to position of calculated alpha
        newPosition = []
        for oldPosition, slope in zip(position,slopeList):
            newPosition.append(oldPosition-slope*damping*alphaStar)
        lastPosition = position
        position = newPosition
        objectiveValueLast = objectiveValue
        objectiveValue = function(position)

        # Print current iteration results
        if echo:
            resultsString = "%i        \t" %(i)
            resultsString += "{}\t".format(position)
            resultsString += "{}\t".format(slopeList)
            resultsString += "%2.6f" % (objectiveValue)
            print(resultsString)

        # Check convergence
        deltaObjective = objectiveValueLast - objectiveValue
        if abs(deltaObjective) <= epsilon:
            shouldContinue = False
            if echo: print("Local Optimium found")

        if i > nMax:
            if echo: print("Function timed out. Returning final result")
            shouldContinue = False

    if echo:
        print("#### - Results - ####")
        print("Position is:")
        print(position)
        print("F = %2.6f" % (objectiveValue))
    return (objectiveValue, position)

def moving_average(xs, window=3):
    from icecream import ic

    n = len(xs)
    if n < window:
        return np.full((n), np.average(xs)).tolist()

    avgs = [0 for i in range(0,n)]
    if (window % 2) == 0:
        upper_offset = int(np.floor((window-1)/2))
        lower_offset = int(np.floor((window-1)/2)) + 1
    else:
        upper_offset = int(np.floor((window-1)/2))
        lower_offset = int(np.floor((window-1)/2))

    for i in range(0,n):
        if i < lower_offset:
            avgs[i] = np.average(xs[:i+upper_offset+1])
        elif (n - i) < (upper_offset +1):
            lower_bound = i - lower_offset
            avgs[i] = np.average(xs[lower_bound:])
        else:
            avgs[i] = np.average(xs[i-lower_offset:i+upper_offset+1])
    return avgs

def linear_interpolate(x, x0, x1, y0, y1):
    y = y0*(1-(x-x0)/(x1-x0)) + y1*(1-(x1-x)/(x1-x0))
    return y
