from databasemanager import *
import numpy as np
import matplotlib.pyplot as plt

# root = 'C:\\db\\toyDB'
# db = Database(root)
# datasets = db.dataset_names
# ds = db.load_dataset('ds1')

import numpy as np
import matplotlib.pyplot as plt


data = {'subject1': 109438.50,
        'subject 2': 103569.59,
        'Fritsch, Russel and Anderson': 112214.71,
        'Jerde-Hilpert': 112591.43,
        'Keeling LLC': 100934.30,
        'Koepp Ltd': 103660.54,
        'Kulas Inc': 137351.96,
        'Trantow-Barrows': 123381.38,
        'White-Trantow': 135841.99,
        'Will LLC': 104437.60}
group_data = list(data.values())
group_names = list(data.keys())
group_mean = np.mean(group_data)

fig, ax = plt.subplots()
ax.barh(group_names, group_data)
plt.show