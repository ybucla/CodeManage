## density plot
import scipy.stats
import numpy as np
import matplotlib.pyplot as plt

x = np.random.normal(3,1,100)
density = scipy.stats.gaussian_kde(x)
xs = np.linspace(min(x),max(x),len(x))

plt.plot(xs, density(xs))
plt.show()
