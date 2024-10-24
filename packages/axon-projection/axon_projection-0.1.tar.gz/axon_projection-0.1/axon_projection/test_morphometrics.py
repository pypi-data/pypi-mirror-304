from axon_projection.figures_scripts.compute_scores import compute_stats_populations, plot_population_stats
import neurom as nm
from axon_synthesis.utils import get_morphology_paths

morphometrics = ["number_of_segments", "segment_lengths", "segment_path_lengths", "segment_radii", "segment_volumes", "number_of_sections", "section_tortuosity"]

old_axons = nm.load_morphologies("/gpfs/bbp.cscs.ch/data/project/proj135/home/petkantc/axon/axonal-projection/axon_projection/validation/circuit-build/lite_MOp5_final/a_s_out_old/Morphologies/non_centered")
new_axons = nm.load_morphologies("/gpfs/bbp.cscs.ch/data/project/proj135/home/petkantc/axon/axonal-projection/axon_projection/validation/circuit-build/lite_MOp5_final/a_s_out/Morphologies/non_centered")
list_trunks_old = get_morphology_paths("/gpfs/bbp.cscs.ch/data/project/proj135/home/petkantc/axon/axonal-projection/axon_projection/validation/circuit-build/lite_MOp5_final/a_s_out_old/PostProcessTrunkMorphologies/hashed")["morph_path"].values.tolist()
list_trunks_new = get_morphology_paths("/gpfs/bbp.cscs.ch/data/project/proj135/home/petkantc/axon/axonal-projection/axon_projection/validation/circuit-build/lite_MOp5_final/a_s_out/PostProcessTrunkMorphologies/hashed")["morph_path"].values.tolist()
print("Computing stats...")
df_res = compute_stats_populations(list_trunks_old, list_trunks_new, morphometrics, morph_type="morphs", in_parallel=True)
print("Plotting...")
plot_population_stats(df_res['pop_1'], df_res['pop_2'], morphometrics, type_1="Old", type_2="New", morph_type="morphs")