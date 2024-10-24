import pandas as pd
import numpy as np
import os
from axon_projection.query_atlas import without_hemisphere
from axon_projection.choose_hierarchy_level import build_parent_mapping
from axon_projection.choose_hierarchy_level import find_parent_acronym
import json

df_morphs = pd.read_csv("axon_lengths_12.csv", index_col=0)
atlas_hierarchy = ("/gpfs/bbp.cscs.ch/data/project/proj135/home/petkantc/atlas/"
"atlas_aleksandra/atlas-release-mouse-barrels-density-mod/hierarchy.json")
with open(atlas_hierarchy, encoding="utf-8") as f:
    hierarchy_data = json.load(f)
hierarchy = hierarchy_data["msg"][0]
parent_mapping = build_parent_mapping(hierarchy)
df_morphs = df_morphs[['morph_path', 'source']]
df_morphs['source_wo_hemi'] = df_morphs['source'].apply(without_hemisphere)
parent_regions = [
        "MOp",
        "MOs",
        "SSp",
        "SSs",
        "VISC",
        "VIS",
        "AUD",
        "PERI",
        "ECT",
        "GU",
        "ORB",
        "ACA",
        "RSP",
        "FRP",
        "PL",
        "ILA",
        "TEa",
        "PTLp",
        "AI",
    ]
df_morphs['parent_region'] = df_morphs["source"].apply(
    lambda x: find_parent_acronym(without_hemisphere(x), parent_mapping, parent_regions)
)
df_morphs = df_morphs.dropna(subset=["parent_region"])
print(df_morphs)

dict_count = {}

for source in df_morphs['source_wo_hemi'].unique():
    len_tot = len(df_morphs[df_morphs['source_wo_hemi']==source])
    len_L = len(df_morphs[df_morphs['source']==source+"_L"])
    len_R = len(df_morphs[df_morphs['source']==source+"_R"])
    print(source+": $n="+str(len_tot)+"$")
    dict_count[source] = [len_L, len_R]

print("parents")
for parent in parent_regions:
    len_tot = len(df_morphs[df_morphs['parent_region']==parent])
    print(parent+": $n="+str(len_tot)+"$")
df_count = pd.DataFrame.from_dict(dict_count, orient='index', columns=['Left', 'Right'])
print("Total = ", len(df_morphs))
# sort by source
df_count = df_count.reindex(sorted(df_count.index), axis=0)
df_count.to_latex("count_morphs_iso.tex")