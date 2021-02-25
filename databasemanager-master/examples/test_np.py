#%%
import numpy as np
import databasemanager.numpyextensions as npx

#%% shuffle
lst = ['a',2,'c',4]
lst = np.array(lst)
#print(npx.shuffle_outline(lst))
L = len(lst)
ind = np.random.permutation(L)
res = lst[ind]
print(lst)
print(res)

#%%
x = np.reshape(np.arange(10*20*30*40*50),(10,20,30,40,50))
axis=1
indices = [1,2,4,5] 
y = np.take(x, indices, axis)

print(x.shape)
print(y.shape)


xh = np.copy(x)
npx.put_in(xh, y, axis, indices)
print(xh.shape)
mse = ((x - xh)**2).mean()
print(mse)

# %%
#x = np.reshape(np.arange(1*2*3*4*5),(1,2,3,4,5))
x=np.array([[1,2,3],[4,5,6]])
axis=1
y = x[:,1,]
indices = None
#indices = [1]
print(x)
print(y)
print(x.shape)
print(y.shape)


xh = np.copy(x)
npx.put_in(xh, y, axis, indices)
print(xh)
print(xh.shape)
mse = ((x - xh)**2).mean()
print(mse)


# %%
x=np.array([[1,2,3],[4,5,6]])
y = npx.exclude_in(x, 1, [0,2])

print(x.shape)
print(y.shape)
print(x)
print(y)

# %%
