from voxcell.cell_collection import CellCollection
import pandas as pd
import os
morph_coll = CellCollection.load('lite_isocortex/auxiliary/cells_collection_MOp5.h5')
morphs_df = morph_coll.as_dataframe()

for index, row in morphs_df.iterrows():
    if not os.path.exists('lite_isocortex/morphologies/neurons/' + row['morphology'] + '.asc'):
        os.system('cp -v lite_isocortex_no_axons/morphologies/neurons/' + row['morphology'] + '.asc lite_isocortex/morphologies/neurons/'+ '/'.join(row['morphology'].split('/')[:-1])+'/.')
    if index % 100 == 0:
        print("Progress ", 100*float(index)/len(morphs_df))