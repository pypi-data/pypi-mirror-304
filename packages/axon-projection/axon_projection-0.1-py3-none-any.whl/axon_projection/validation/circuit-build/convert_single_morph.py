from neurom import load_morphology
import morph_tool.graft as mtg
from morph_tool.transform import translate
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from neurom.view import matplotlib_impl, matplotlib_utils, plotly_impl, plot_morph
import sys
import os

def convert_morph(morph, path='./morph', to='swc'):
    morph.write(path+"."+to)

def plot_morphs(list_morphs, two_d = False):
    for morph_path in list_morphs:
        morph = load_morphology(morph_path)
        if two_d:
            plotly_impl.plot_morph(morph, inline=False)
            os.system(f"mv morphology-2D.html {os.path.basename(morph_path).split('.')[0]}.html")
        else:
            plotly_impl.plot_morph3d(morph, inline=False)
            os.system(f"mv morphology-3D.html {os.path.basename(morph_path).split('.')[0]}.html")
        plt.close()

if __name__=="__main__":
    morph_path = sys.argv[1]
    convert_morph(load_morphology(morph_path), to='asc')