#==================================================#
# Authors: Amir H. Ansari <amirans65.ai@gmail.com> #
# License: BSD (3-clause)                          #
#==================================================#

import numpy as np

def exclude_in(x:np.ndarray, axis:int = 0, indices: list = None):
    '''
    it excludes some indices in the given axis of x and returns the results.
    the input is unchanged.
    '''
    if(isinstance(indices, int)):
        indices = [indices]
    include_indices = [i for i in range(x.shape[axis]) if i not in indices]
    return np.take(x, include_indices, axis)

def put_in(x:np.ndarray, y:np.ndarray, axis:int = 0, indices: list = None):
    '''
    This function acts similar to take while it does assignment. In other words, it takes a big tensor (x) and axis to put a smaller tensor (y) there.
    
    parameters:
    ----------
    x: the big matrix. It will be changed after this function.
    y: the smaller tensor that should be placed in x. If y.ndims is (x.ndims-1), then y is expanded and repeated to be matched to the given indices.
    axis: the target axis
    indices: the indices vector in the given axis. Length of this vector must be matched with y.shape[axis].
    if indices is None, it means the whole range.
    

    return:
    ------
    None
    '''
    if(isinstance(indices, int)):
        indices = [indices]
    if(indices is None):
        indices = range(x.shape[axis])
    if(y.ndim == (x.ndim - 1)):
        y = np.expand_dims(y, axis)
        rep_ind = np.ones(x.ndim, np.int)
        rep_ind[axis] = len(indices)
        y = np.tile(y, tuple(rep_ind))

    # apply
    idx = [slice(None)]*x.ndim
    idx[axis] = indices
    x[tuple(idx)] = y

def shuffle_outline(lst, random_state=None):
    '''
    This function takes a list and returns a new shuffled list while the original list is untouched
    the input list must be a numpy list
    '''
    assert(isinstance(lst, np.ndarray))
    if(random_state is None):
        ind = np.random.permutation(len(lst))
    else:
        ind = random_state.permutation(len(lst))
    return lst[ind]


