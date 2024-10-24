import pandas as pd
from voxcell.cell_collection import CellCollection
from axon_projection.choose_hierarchy_level import build_parent_mapping, find_parent_acronym
import json

morphs_coll_path = "/gpfs/bbp.cscs.ch/data/project/proj135/home/petkantc/axon/axonal-projection/axon_projection/validation/circuit-build/lite_iso_final/auxiliary/circuit.synthesized_morphologies.h5"

morphs_df = CellCollection.load(morphs_coll_path).as_dataframe()

with open("/gpfs/bbp.cscs.ch/data/project/proj135/home/petkantc/atlas/atlas_aleksandra/atlas-release-mouse-barrels-density-mod/hierarchy.json", encoding="utf-8") as f:
    hierarchy_data = json.load(f)
    hierarchy = hierarchy_data["msg"][0]
    parent_mapping = build_parent_mapping(hierarchy)
target_parents = ["MOp", "MOs", "SSp", "SSs", "VISC", "AUD", "PERI", "ECT", "GU", "ORB", "ACA", "RSP", "FRP", "PL", "ILA", "TEa", "VIS", "PTLp", "AI"]
morphs_df['parent_region'] = morphs_df['region'].apply(lambda x: find_parent_acronym(x, parent_mapping, target_parents))
morphs_df = morphs_df[morphs_df['parent_region'].notna()]

# original config file for movie
config_path = "/gpfs/bbp.cscs.ch/data/project/proj135/home/petkantc/axon/axonal-projection/axon_projection/validation/circuit-build/lite_iso_final/movie/config.json"
movie_path = "/gpfs/bbp.cscs.ch/data/project/proj135/home/petkantc/axon/axonal-projection/axon_projection/validation/circuit-build/lite_iso_final/movie/"

morphs_df = morphs_df.sort_values('parent_region')
list_all_subregions = []
with open(config_path, 'r') as file:
    config_data = json.load(file)

# for each parent, show the index of all the children
for parent in morphs_df['parent_region'].unique():
    print(parent)
    print(morphs_df[morphs_df['parent_region'] == parent].index.values)
    list_subregions = morphs_df[morphs_df['parent_region'] == parent]['subregion'].unique().tolist()
    list_all_subregions += list_subregions
    print(json.dumps(list_subregions))
    config_data['models'][1]['loader']['properties']['node_population_settings'][0]['node_sets'] = list_all_subregions
    # save back the config file
    config_file_path = movie_path + "config_" + parent + ".json"
    with open(config_file_path, 'w') as file:
        json.dump(config_data, file, indent=4)
