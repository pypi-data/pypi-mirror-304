import json
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

# Load the JSON data
with open('/gpfs/bbp.cscs.ch/data/project/proj135/home/petkantc/axon/axonal-projection/axon_projection/pop_comparison_MOp5_morphs.json', 'r') as f:
    data = json.load(f)

morphometrics = ["number_of_segments", "segment_lengths", "segment_path_lengths", "segment_radii", "segment_volumes", "number_of_sections", "section_tortuosity"]
for morph in morphometrics:
    # Extract data for the two populations
    pop_1_data = data["pop_1"][morph]
    pop_2_data = data["pop_2"][morph]

    # Create a DataFrame with both populations
    df = pd.DataFrame({
        "Segments": pop_1_data + pop_2_data,
        "Population": ["Pop 1"] * len(pop_1_data) + ["Pop 2"] * len(pop_2_data)
    })

    # Plot the split violin plot
    plt.figure(figsize=(10, 6))
    sns.violinplot(
        x="Population", y="Segments", data=df, split=True, inner="quartile", palette="Set2"
    )

    # Add plot title and labels
    plt.title("Split Violin Plot: Pop 1 vs Pop 2")
    plt.ylabel(morph)
    plt.savefig("plot_"+morph+".png")