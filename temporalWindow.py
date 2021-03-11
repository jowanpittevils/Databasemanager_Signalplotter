from databasemanager import *
import numpy as np
import matplotlib.pyplot as plt

root = 'C:\\db\\toyDB'
db = Database(root)
datasets = db.dataset_names
ds = db.load_dataset('ds1')


