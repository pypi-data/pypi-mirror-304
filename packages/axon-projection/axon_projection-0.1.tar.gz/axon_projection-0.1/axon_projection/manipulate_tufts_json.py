import pandas as pd
import json
import sys
import pathlib
from axon_projection.query_atlas import load_atlas
import configparser
import logging

def try_get_region_id(brain_reg_voxel, region_map):
    reg_id = 0
    try:
        reg_id = region_map.get(brain_reg_voxel, "id", with_ascendants=False)
    except:
        logging.warning("Could not find region for %s", brain_reg_voxel)
    return reg_id

config = configparser.ConfigParser()
config.read(sys.argv[1])
out_path = config["output"]["path"]
atlas_path = config["atlas"]["path"]
atlas_regions = config["atlas"]["regions"]
atlas_hierarchy = config["atlas"]["hierarchy"]

with pathlib.Path(out_path+"/tuft_properties.json").open(mode="r", encoding="utf-8") as f:
    tufts_df = pd.DataFrame(json.load(f))
# tufts_df['morph_file'] = tufts_df['morph_file'].str.replace('/gpfs/bbp.cscs.ch/project/proj82/home/petkantc/morpho/all_morphs/morphs_ML/swc', '/gpfs/bbp.cscs.ch/project/proj82/home/petkantc/morpho/all_morphs/morphs_ML')
# tufts_df['morph_file'] = tufts_df['morph_file'].str.replace('/gpfs/bbp.cscs.ch/project/proj82/home/petkantc/morpho/SEU/out/repair_release/swc', '/gpfs/bbp.cscs.ch/project/proj82/home/petkantc/morpho/all_morphs/morphs_SEU')
# tufts_df['morph_file'] = tufts_df['morph_file'].str.replace('/gpfs/bbp.cscs.ch/project/proj82/home/petkantc/morpho/peng2021/out/out_repaired/CollectAnnotated/data', '/gpfs/bbp.cscs.ch/project/proj82/home/petkantc/morpho/all_morphs/morphs_peng')
_, brain_regions, region_map = load_atlas(atlas_path, atlas_regions, atlas_hierarchy)
# apply brain_regions.lookup on all the tufts_df["center_coords"], and put that result in tufts_df["brain_regions_voxels"]
tufts_df["target_region_id"] = brain_regions.lookup(tufts_df["center_coords"].tolist(), outer_value=-1)
# tufts_df["target_region_id"] = tufts_df.apply(lambda row: try_get_region_id(row["brain_regions_voxels"], region_map), axis=1) # region_map.get(tufts_df["brain_regions_voxels"], "id", with_ascendants=False)
# 'target_population_id' is the concatenation of population id and target region id
# tufts_df["target_population_id"] = tufts_df["population_id"].astype(str) + "_" + tufts_df["target_region_id"].astype(str)
tufts_df["population_id"] = tufts_df["target_population_id"].astype(str)

with pathlib.Path(out_path + "tuft_properties_changed.json").open(mode="w", encoding="utf-8") as f:
    json.dump(tufts_df.to_dict("records"), f, indent=4)