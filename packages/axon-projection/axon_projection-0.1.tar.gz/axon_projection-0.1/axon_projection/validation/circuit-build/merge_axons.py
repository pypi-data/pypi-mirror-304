import pandas as pd
from morphio import PointLevel, SectionType
from morphio.mut import Morphology

from axon_synthesis.utils import get_morphology_paths

morph_dir = "/gpfs/bbp.cscs.ch/project/proj82/home/petkantc/axon/axonal-projection/axon_projection/validation/circuit-build/lite_isocortex/a_s_out/Morphologies/hashed"
list_morphs = get_morphology_paths(morph_dir)["morph_path"].values.tolist()
for i, morpho_path in enumerate(list_morphs):
    if i % 10 == 0:
        print(f"{i}/{len(list_morphs)}")
    morpho = Morphology(morpho_path)

    num_axons = 0
    axons_roots = []
    for sec in morpho.root_sections:
        if sec.type == SectionType.axon:
            axons_roots.append(sec)
            num_axons += 1
    if num_axons <= 1:
        print(f"Nothing to do, {num_axons} found.")
    else:
        # append a root section at the soma
        root_section = morpho.append_root_section(
            PointLevel(
                [[2, 2, 2], [3, 3, 3]],  # x, y, z coordinates of each point
                [4, 4]),  # diameter of each point
            SectionType.axon)  # (optional) perimeter of each point
        # and graft the axons to that section
        for sec in axons_roots:
            child_section0 = root_section.append_section(sec, recursive=True) # section type is omitted -> parent section type will be used
            morpho.delete_section(sec, recursive=True)

    morpho.write(morpho_path)
print("Done merging axons")