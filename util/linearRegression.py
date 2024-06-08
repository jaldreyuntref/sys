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

"""
# Regresión lineal
m, b = linearRegression(schroederIntegralSignal)
xFit = list(range(1, len(schroederIntegralSignal) + 1))
yFit = [m * xi + b for xi in xFit]

# Crear figura y plotear datos y regresión lineal
fig, ax = createFigure(range(1, len(schroederIntegralSignal) + 1), schroederIntegralSignal)
ax.plot(xFit, yFit, label="Linear Regression", color='red')
ax.legend()
plt.show()
"""