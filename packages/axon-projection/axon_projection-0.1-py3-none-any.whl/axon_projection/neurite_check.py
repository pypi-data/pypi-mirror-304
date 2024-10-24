from axon_projection.compute_morphometrics import has_neurite_type
from neurom import NeuriteType
import neurom as nm
import pandas as pd

a_p_data = pd.read_csv("/gpfs/bbp.cscs.ch/data/project/proj135/home/petkantc/axon/axonal-projection/axon_projection/out_a_p_final/axon_lengths_12.csv", index_col=0)[["morph_path", "source"]]
a_p_data = a_p_data[a_p_data['morph_path'].str.contains('SEU')]
print(len(a_p_data))

a_p_data['has_apical'] = a_p_data.apply(lambda row: has_neurite_type(row['morph_path'], NeuriteType.apical_dendrite), axis=1)
a_p_data.to_csv("apical_check.csv")
# with open("/gpfs/bbp.cscs.ch/data/project/proj135/home/petkantc/atlas/atlas_aleksandra/atlas-release-mouse-barrels-density-mod/hierarchy.json", encoding="utf-8") as f:
#     hierarchy_data = json.load(f)
# hierarchy = hierarchy_data["msg"][0]
# parent_mapping = build_parent_mapping(hierarchy)
# target_regions = ["ACA",
#         "FRP",
#         "MOp",
#         "MOs",
#         "ORB",
#         "PL",
#         "RSP",
#         "ILA",
#         "SSp",
#         "AUD",
#         "SSs",
#         "TEa",
#         "VISC",
#         "ECT",
#         "PERI",
#         "GU",
#         "PTLp",
#         "VIS",]
# a_p_data["parent_region"] = a_p_data["source"].apply(
#     lambda x: find_parent_acronym(x, parent_mapping, target_regions)
# )