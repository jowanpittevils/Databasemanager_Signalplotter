#==================================================#
# Authors: Amir H. Ansari <amirans65.ai@gmail.com> #
# License: BSD (3-clause)                          #
#==================================================#

import numpy  as np
from databasemanager.classes.dataset import Dataset
def split_subjects(dataset: Dataset, ratio:float = None, N:int = None, random_seed=None, deep_copying=True):
    '''
    This function breaks a dataset into two datasets to be used as training and validation/test.
    The 'ratio' or 'N' (exclusive or) defines their ratio.
    deep_copying: if it is True, it copies the datasets and all interanal elements (except the offline loaded data) thoroughly.
                  If it is False, for big datasets, the splitting is much faster and more memory-efficient. 
                  In thsi case, the connection between the ds and splitted ones couse changing one (like purify, foreach, etc.) changes the other one as well.
    '''
    ds0 = dataset.copy(deep_copy_elements = deep_copying)
    assert (ratio is None or N is None)
    assert (ratio is not None or N is not None)
    assert (ratio is None or (ratio >=0 and ratio <=1))
    N0 = len(ds0)
    assert (N is None or (N >=0 and N <= N0))
    if(N is None):
        N = round(N0 * ratio)
    random = np.random.RandomState(random_seed)
    sub_ind = random.permutation(N0)
    sub_ind = sub_ind[0:N]
    subjects = list(np.array(ds0.subjects)[sub_ind])
    subject_names = [s.name for s in subjects]

    ds1 = ds0.copy(deep_copy_elements = deep_copying)
    ds1.intersect_subjects(subject_names)
    ds2 = ds0 - ds1
    return (ds1,ds2)

def K_fold(dataset: Dataset, K:int, random_seed=None):
    '''K-fold splitter. It returns a list of tuples each of which is the pair of a training dataset and a validation/test dataset.'''
    raise ValueError('not yet implemented') # error in shuffeling the subjects

    N = len(dataset)
    dataset_list = []
    random = np.random.RandomState(random_seed)
    subs = random.permutation(dataset.subjects)
    ss = np.array_split(subs, K)
    for k in range(K):
        dsts = dataset.copy()
        dsts.intersect_subjects([s.name for s in list(ss[k])])
        dstr = dataset - dsts
        dataset_list.append((dstr, dsts))
    return dataset_list

def LOSO(dataset: Dataset, index = None):
    '''Leave-One-Subject_Out (LOSO) splitter. 
    if index is None: it returns a list of tuples each of which is the pair of a training dataset and a validation/test dataset.
    if the index is set, it returns 1 tuple (dstraining, dstesting) corresponding the given index. Thus, the dstesting has only dataset.subjects[index].
    '''
    if(index is None):
        lst = range(len(dataset))
    else:
        lst = [index]
    dataset_list = []
    for i in lst:
        dsts = dataset.copy()
        dsts.intersect_subjects([dataset.subjects[i].name])
        dstr = dataset - dsts
        dataset_list.append((dstr, dsts))
    if(index is not None):
        return dataset_list[0]
    return dataset_list

def split_recordings(dataset, ratio:float = None, length:int = None, in_annotation_range:bool = True):
    '''
    This function breaks a dataset into two datasets to be used as training and validation/test with changing the annotations.
    The datasets are the same except for their annotations. The annotations are complimentary so that from the start to N second exist in the
    first dataset and from N to the end exist in the 2nd dataset.
    ratio: defining the ration of first and second dataset. It will be counted based on the start and end of annotations (not recording)
    length: define the length of the first dataset in seconds, it is counted from the start of the first annotation. 
            If it is negative, it applies from end to separate validation/test with this fixed length.
            If it is longer than the possible duration, the possible duration is taken.
    '''
    assert (ratio is None or length is None)
    assert (ratio is not None or length is not None)
    assert (ratio is None or (ratio >=0 and ratio <=1))
    dstr = dataset.copy()
    dsts = dataset.copy()
    for isub in range(len(dataset.subjects)):
        for irec in range(len(dataset.subjects[isub].recordings)):
            rec = dataset.subjects[isub].recordings[irec]
            for iann in range(len(rec.annotations)):
                ann_tr = dstr.subjects[isub].recordings[irec].annotations[iann]
                ann_ts = dsts.subjects[isub].recordings[irec].annotations[iann]
                ann_tr.sort_events()
                ann_ts.sort_events()                
                if(len(ann_tr.events)==0):
                    raise ValueError('This function is annotation based, while one of the annotations are empty: ', rec.name)
                max_possibl_dur = ann_tr.events[-1].end - ann_tr.events[0].start
                if(length is None):
                    applying_length = round(ratio * max_possibl_dur)
                elif(length > 0):
                    applying_length =  min(length, max_possibl_dur)
                elif(length < 0):
                    applying_length = max(0, max_possibl_dur + length) # (-*- length0 is negative)
                stoppoint = applying_length + ann_tr.events[0].start
                ann_tr.add_stop_point(stoppoint)
                ann_tr.events = [event for event in ann_tr.events if event.end <= stoppoint]

                ann_ts.add_stop_point(stoppoint)
                ann_ts.events = [event for event in ann_ts.events if event.start >= stoppoint]
    return (dstr, dsts)

