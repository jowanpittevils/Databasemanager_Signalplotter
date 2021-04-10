#%%
import numpy as np
from signalplotter import iplot
import matplotlib.pyplot as plt
x = np.random.randn(10,500)


def a(ich=0, ix=0, x=None):
    if(ich%2==0):
        return {'color': (1,0,0)}
    return {'color': (0,0,1)}

d = a()
print(d)
plt.plot(x.transpose(), **a())
plt.show()
iplot(x, plot_args=a)

# %%
