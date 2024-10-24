import neurom as nm
import numpy as np
import pandas as pd
from axon_synthesis.utils import get_morphology_paths

def get_morph_files_from_dirs(dirs_list):
    if not (isinstance(dirs_list, list) or isinstance(dirs_list, np.ndarray) or isinstance(dirs_list, pd.Series)):
        return nm.io.utils.get_morph_files(dirs_list)
    
    list_morphs = []
    for directory in dirs_list:
        list_morphs += nm.io.utils.get_morph_files(directory)
    return list_morphs

print(nm.io.utils.get_morph_files("/gpfs/bbp.cscs.ch/project/proj82/home/petkantc/morpho/test_ln"))
print(get_morphology_paths("/gpfs/bbp.cscs.ch/project/proj82/home/petkantc/morpho/test_ln")["morph_path"].values.tolist())