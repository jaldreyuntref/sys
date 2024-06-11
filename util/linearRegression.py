def linearRegression(y):

    """
    Performs a linear regression on a given set of y-values.

    Parameters:
        y (list or numpy array): The dependent variable values.

    Returns:
        tuple: A tuple containing the slope (m) and intercept (b) of the 
               best-fit line y = mx + b.

    This function calculates the linear regression of the input data `y` 
    using the least squares method. It computes the slope and intercept 
    of the line that best fits the data points.
    """

    n = len(y)
    x = list(range(1, n + 1))
    sumX = sum(x)
    sumY = sum(y)
    sumXy = sum(x_i * y_i for x_i, y_i in zip(x, y))
    sumXSquared = sum(x_i ** 2 for x_i in x)
    
    m = (n * sumXy - sumX * sumY) / (n * sumXSquared - sumX ** 2)
    b = (sumY - m * sumX) / n
    
    return m, b

if __name__ == "__main__":
    from synthesizeImpulseResponse import synthesizeImpulseResponse
    from schroederIntegral import schroederIntegral
    from logarithmicScaleConversion import logarithmicScaleConversion
    from functions import createFigure
    import matplotlib.pyplot as plt

    impulseResponse,time = synthesizeImpulseResponse(test=True)
    impulseResponse = schroederIntegral(impulseResponse)
    impulseResponse = logarithmicScaleConversion(impulseResponse)
    m, b = linearRegression(impulseResponse)
    xFit = list(range(1, len(impulseResponse) + 1))
    yFit = [m * xi + b for xi in xFit]
    
    fig, ax = createFigure(range(1, len(impulseResponse) + 1), impulseResponse)
    ax.plot(xFit, yFit, label="Linear Regression", color='red')
    ax.legend()
    plt.show()
