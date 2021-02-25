#%%
%reload_ext autoreload
%autoreload 2

#%% databse
import numpy as np
from databasemanager import *

#root = 'C:\\MyFiles\\MyDatabases\\TempleSeizure'
root = r'C:\db\toyDB'
db = Database(root)
db.summary()

dsNames =  db.dataset_names

#%%
# set config on config.ini
# or the settings
#UserSettings.global_settings().loading_data_channels = ['c4','c3','fp1']
#ds = db.load_dataset('ds_train_tcp_ar')

#% dataset
UserSettings.global_settings().loading_data_missing_channel_type = 'error'
UserSettings.global_settings().loading_data_channels = ['fp1','fp2','t3','t4','o1','o2','c3','c4']
ds = db.load_dataset('ds1')
ds.add_background_label('NQS')

#%%
ds.summary()

print(ds)
print(ds.subjects[0])
print(ds.subjects[0].recordings[0])
print(ds.subjects[0].recordings[0].annotations[0])
print(ds.subjects[0].recordings[0].annotations[0].extrainfo)
print(ds.subjects[0].recordings[0].annotations[0].events[0])
print(ds.subjects[0].recordings[0].annotations[0].events[0].extrainfo)
print(ds.subjects[0].recordings[0].annotations[0].events[0].annotation.name)
print(ds.subjects[0].recordings[0].channels)
print(ds.subjects[0].recordings[0].duration_samp)
print(ds.subjects[0].recordings[0].fs)
print(ds.subjects[0].recordings[0].duration_sec)
print(ds.subjects[0].recordings[0].duration_str)
print(ds.unique_labels)
print(ds.number_of_channels)


#%%
#%%
# purify, where, take, foreach, count

def name(x):
    return 'PT' in x.name

def rr(rec):
    print(rec.name)
    print(rec.duration)
    res = (rec.duration==0)
    print(type(res))
    return res

# copy
dstemp = ds.copy()
dstemp.purify(Criteria(Subject, lambda s: '18' in s.name))
dstemp.summary()


recs = ds.take(Criteria(RecordingBase, rr))
#recs = ds.take(Criteria(RecordingBase, lambda x: True))
print(len(recs))
#recs.summary()

#dstemp.summary()
#dstemp.purify(Criteria(RecordingBase, lambda x: x.name[0]=='r'))
#dstemp.purify(Criteria(RecordingBase, lambda x: x.name[1]=='r'))
#or
#dstemp = ds.where(Criteria(Subject, lambda x: 'PT 43' in x.name, 'include'))
#dstemp = ds.where(Criteria(Subject, lambda x: 'PT 43' in x.name, 'include'))
#dstemp = ds.where(Criteria(RecordingBase, lambda x: 'PT 43' in x.name))

#2
dstemp = ds.where(Criteria(AnnotationExtraInfo, lambda x: float(x.GA)>35, 'include'))
dstemp.summary()
dstemp.purify(Criteria(RecordingBase, lambda x: x.number_of_annotations==0, 'exclude'))
dstemp.purify(Criteria(Subject, lambda x: x.number_of_recordings==0, 'exclude'))
dstemp.summary()

#extra info
#dstemp = ds.copy()
#dstemp = ds.where(Criteria(EventExtraInfo, lambda x: int(x.artifact)==1, 'exclude', 'include'))

#other levels
#dstemp = ds.copy()
#dstemp.subjects[0].purify(Criteria(RecordingBase, lambda x: 'PT ' in x.name, 'exclude'))
#dstemp.purify(Criteria(Subject, lambda x: x.number_of_recordings==0, 'exclude'))

# normal functions
#dstemp = ds.copy()
#def f(x):
#    return 'PT ' in x.name

# event time
#dstemp = ds.copy()
#dstemp.purify(Criteria(Event, lambda x: (x.start is None) or (x.start<1000), 'exclude'))
#dstemp.purify(Criteria(Event, lambda x: x.duration<60 , 'exclude'))
#dstemp.purify(Criteria(Event, lambda x: x.label == 'Undetermined' , 'exclude'))

dstemp.summary()

#%%
recs = ds.take(Criteria(RecordingBase))
anns = recs[0].annotations
print(anns)
#%% taking
events = ds.take(Criteria(Event, lambda x: x.label == 'ASI'))
print('N: ' + str(len(events)))
print('mean duration: {}'.format(np.array([item.duration for item in events]).mean()))
print('std duration: {}'.format(np.array([item.duration for item in events]).std()))

#%% foreach
# calc mean
dstemp = ds.copy()
print(dstemp.unique_labels)
dur_list = dstemp.foreach(Criteria(Event, lambda x: x.label == 'QS'), lambda x: setattr(x,'label', 'QUIETSLEEP'))
print(dstemp.unique_labels)

dur_list = dstemp.foreach(Criteria(Event, lambda x: x.label == 'NQS'), lambda x: x.duration)
print(dur_list)

# do an action
dstemp.foreach(Criteria(Event, lambda x: x.label == 'Undetermined'), lambda x: setattr(x,'label','blabla'))

print("#original: {}".format(ds.count(Criteria(Event, lambda x: x.label == 'Undetermined'))))
print("#changed: {}".format(dstemp.count(Criteria(Event, lambda x: x.label == 'Undetermined'))))
print("#changed to: {}".format(dstemp.count(Criteria(Event, lambda x: x.label == 'blabla'))))


# %% fetch mne
print('dataset level, #mne raw: {}'.format(len(ds.fetch_mne_list())))
print('subject level, #mne raw: {}'.format(len(ds.subjects[0].fetch_mne_list())))
print('recording level, #mne raw: {}'.format(len(ds.subjects[0].recordings[0].fetch_mne_list())))

# %% mne
ds_t = ds.copy()
ds_t.purify(Criteria(Event, lambda x: x.label == 'Undetermined', 'exclude'))
ds_t.purify(Criteria(Event, lambda x: x.label == 'Artifact', 'exclude'))

custom_mapping = {'LVI':0, 'ASI':1, 'HVS':2, 'TA':3}
raw = ds_t.fetch_mne_list()
(rem_events, rem_event_dict) = mne.events_from_annotations(
                                                raw[0], 
                                                chunk_duration=30,
                                                event_id=custom_mapping,)
rem_events.shape
raw[0].plot()
# %%
ds.foreach(
    Criteria(Annotation,lambda x:True),
    lambda ann:ann.add_background_label(
                    'NQS',
                    int(ann.extrainfo.start_annotation), int(ann.extrainfo.start_annotation)
                    ),
    )
print(ds.subjects[0].recordings[0].name)
print(ds.subjects[0].recordings[0].annotations[0].get_label(2935, 2946,'longest'))
#print(ds.subjects[0].recordings[0].annotations[0].get_label(2950, 2960))
# %%

events = ds.take(Criteria(Event))
print(events)
# %%
