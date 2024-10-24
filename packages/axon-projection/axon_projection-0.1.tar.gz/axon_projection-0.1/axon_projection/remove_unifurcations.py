import os
import sys
from multiprocessing import Pool
from morphio.mut import Morphology
from morph_tool.converter import convert

def reomve_one_morph_unifurcation(morph_path, morph_num):
    if morph_num % 1000 == 0:
        print('.')
    try:
        morph = Morphology(morph_path)
    except:
        print(f"WARNING: morphology {morph_path} not found!")
        return
    
    morph.remove_unifurcations()
    convert(morph, morph_path, nrn_order=True, sanitize=True)

def remove_all_unifurcations(morphs_path):
    list_morphs = os.popen("find "+morphs_path+" -name \"*.asc\" -o -name \"*.h5\" -o -name \"*.swc\"").read()
    list_morphs = list_morphs.split("\n")
    nb_morphs = len(list_morphs)
    print("Number of morphs to process:", nb_morphs)
    args = []
    for m, morph_path in enumerate(list_morphs):
        if morph_path == "":
            continue
        args.append((morph_path,m,))

    with Pool() as p:
        p.starmap(reomve_one_morph_unifurcation, args)

if __name__ == "__main__":
    morphs_path = sys.argv[1]
    remove_all_unifurcations(morphs_path)