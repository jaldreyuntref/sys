def linearRegression(y):
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
