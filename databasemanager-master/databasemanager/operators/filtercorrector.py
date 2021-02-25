#==================================================#
# Authors: Amir H. Ansari <amirans65.ai@gmail.com> #
# License: BSD (3-clause)                          #
#==================================================#

import numpy as np
from databasemanager.operators.shrinker import Shrinker

class FilterCorrector(Shrinker):
    def __init__(self, filter):
        super().__init__(*filter.correction_samples)