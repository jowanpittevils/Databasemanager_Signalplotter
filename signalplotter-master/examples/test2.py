#%%
from signalplotter import iplot, gplot
import numpy as np

x = np.random.randn(100,8,30*250)/5
iplot(x[1,])
gplot(x)


# %%
