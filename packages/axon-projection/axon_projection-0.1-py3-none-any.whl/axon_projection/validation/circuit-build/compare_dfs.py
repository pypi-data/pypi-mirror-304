import pandas as pd

df_axons = pd.read_csv("/gpfs/bbp.cscs.ch/project/proj82/home/petkantc/axon/axonal-projection/axon_projection/validation/circuit-build/lite_isocortex/connection_counts_for_pathways.csv")
df_no_axons = pd.read_csv("/gpfs/bbp.cscs.ch/project/proj82/home/petkantc/axon/axonal-projection/axon_projection/validation/circuit-build/lite_isocortex_no_axons/connection_counts_for_pathways.csv")

print("DFs are equal: ", df_axons.equals(df_no_axons))
# print(df_axons.head())
# print(df_no_axons.head())

cmp_df = df_axons.compare(df_no_axons, keep_shape=True, keep_equal=False)

# print(df_axons.compare(df_no_axons, keep_shape=True, keep_equal=True))