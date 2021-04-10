#%%

from classes.path import Path
root = 'C:\\MyFiles\\MyDatabases\\Sleep'

print('--static test')
print(Path.DATAFOLDER)
print(Path.get_datafolder_fullpath(root))
print(Path.get_datasetsfolder_fullpath(root))
print(Path.get_extrafolder_fullpath(root))

print('--object test')
dbp = Path(root)
print(dbp.datafolder_fullpath)
print(dbp.datasetsfolder_fullpath)
print(dbp.extrafolder_fullpath)
print(dbp.datasets_list_fullpath)
names = dbp.datasets_list_names 
print(names[0])
print(dbp.get_dataset_fullpath(names[0]))

#%%
from classes.tsvreader import TSVReader
r,c = TSVReader.read_rows(dbp.get_dataset_fullpath(names[0]))
print(c)
print(r)

# %%
