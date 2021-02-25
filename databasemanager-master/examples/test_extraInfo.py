#%% make 
from databasemanager.classes.extrainfo import ExtraInfo
info = ExtraInfo('#test, #GA:10 \n age:23, #nice!')
info.__dict__

#%% get a defined property
print("info['GA']: " + info['GA'])
print('info.GA: ' + info.GA)

#%% assign a new properties
info.foo = '10' #or
info["foo"] = '20'
print("info.foo: " + info.foo)
print("info['foo']: " + str(info['foo']))
print("support space: info['GA haha']: " + info['GA'])

#%% get what is not defined
# > below line does not raise an exception. It returns None.
print("info['blabla']: " + str(info['blabla']))
# > but below line raises an exception as info has no blabla.
print("info.blabla: " + info.blabla)

# %% test
def a(p: int):
    print(p)
a('str')


# %%
