from scipy.stats import norm
import time, numpy as np
import matplotlib.pyplot as plt


x = np.arange(0,100, 0.001)
y = norm.pdf(x,30,10)/norm.pdf(30,30,10)
print(norm.pdf(100,30,10)/norm.pdf(30,30,10))
plt.plot(x,y)
plt.show()

