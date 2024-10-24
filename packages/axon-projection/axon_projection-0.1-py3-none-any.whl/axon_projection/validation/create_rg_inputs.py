"""Example on how to use the TMD synthesis in space."""
import os
import configparser
from itertools import islice, chain
import sys
import pandas as pd

from voxcell.nexus.voxelbrain import Atlas
from axon_synthesis.atlas import AtlasConfig, AtlasHelper
from axon_projection.utils import get_morph_files_from_dirs

# from region_grower.context import CellHelper
# from region_grower.context import SpaceContext
# from region_grower.synthesize_morphologies import SynthesizeMorphologies

from axon_synthesis.utils import create_random_morphologies
import neurom as nm

def create_population(
    context, cell_path, mtype, number_of_cells, output_path, output_name, formats=None
):
    """Generates N cells according to input distributions.

    The distributions are saved them in the selected files formats (default: h5, swc, asc).
    thickness_ref: initial thickness corresponding to input cell
                   taken from species, layer combination
    layer: defines the layer of the somata
    num_cells: number of cells to grow
    """
    somata = CellHelper(cell_path).positions(mtype)

    if formats is None:
        formats = ["swc", "h5", "asc"]

    # Creates directories to save selected formats
    for f in formats:
        if not os.path.isdir(output_path + f):
            os.mkdir(output_path + f)

    for i, position in enumerate(islice(somata, number_of_cells)):
        neuron = context.synthesize(position, mtype)
        for f in formats:
            neuron.write(output_path + "/" + f + "/" + output_name + "_" + str(i + 1) + "." + f)

def generate_mtype_file(config):
    morphs_dir = config["morphologies"]["path"]
    mtype = "L3_TPC:A"
    list_morphs = get_morph_files_from_dirs(morphs_dir)
    # get the name of the morphologies list paths without the extension
    list_morphs = [os.path.splitext(os.path.basename(x))[0] for x in list_morphs]

    dict_mtypes = {"0": list_morphs, "1": [0] * len(list_morphs), "2": [mtype] * len(list_morphs)}

    mtype_df = pd.DataFrame(dict_mtypes)
    mtype_df.to_csv(config["output"]["path"] + "mtypes_POST.dat", index=None, header=True, sep=" ")

def generate_inputs(config, brain_acronyms_to_grow, n_cells):
    print("Loading atlas...")
    atlas = AtlasHelper(AtlasConfig(config["atlas"]["path"], config["atlas"]["regions"], load_region_map=True))

    brain_ids_to_grow = atlas.get_region_ids(brain_acronyms_to_grow, with_descendants=False)
    # concatenate all the lists in brain_ids_to_grow
    brain_ids_to_grow = list(set(chain.from_iterable(brain_ids_to_grow)))
    print("Region ids to grow: ", brain_ids_to_grow)
    print("Generating morphologies somata positions...")
    create_random_morphologies(
        atlas,
        n_cells,
        brain_ids_to_grow, 
        #config["output"]["path"] + "/cells_collection", 
        output_cell_collection = config["output"]["path"] + "cells_collection.mvd3",
        rng = int(config["random"]["seed"])
    )

    print("Generating mtypes.dat file...")
    generate_mtype_file(config)

    print("Done (", config["output"]["path"], ").")

if __name__ == "__main__":
    # CONTEXT = SynthesizeMorphologies(
    #     atlas=Atlas.open(
    #         "/gpfs/bbp.cscs.ch/project/proj68/entities/dev/atlas/ccf_2017-25um/20190118"
    #     ),
    #     tmd_distributions=(
    #         "/gpfs/bbp.cscs.ch/project/proj68/home/kanari/SynthInput/mouse_distributions.json"
    #     ),
    #     tmd_parameters=(
    #         "/gpfs/bbp.cscs.ch/project/proj68/home/kanari/SynthInput/tmd_parameters.json"
    #     ),
    # )

    # create_population(
    #     CONTEXT,
    #     "/gpfs/bbp.cscs.ch/project/proj68/circuits/COLUMN/20190211.dev/circuit.mvd3.metypes",
    #     mtype="default",
    #     number_of_cells=100,
    #     output_path=".",
    #     output_name="synth_region",
    # )
    
    brain_acronyms_to_grow = ["MOp", "MOs", "SSp", "SSs"]
    n_cells = 100
    config_ = configparser.ConfigParser()
    try:
        config_.read(sys.argv[1])
    except:
        print("Usage: python create_rg_inputs.py <config_file>")
        sys.exit(1)

    generate_inputs(config_, brain_acronyms_to_grow, n_cells)


