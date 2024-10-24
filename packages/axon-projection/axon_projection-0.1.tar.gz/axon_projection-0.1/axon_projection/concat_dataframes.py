import pandas as pd
import sys

if len(sys.argv) < 4:
    print("Usage <df_1> <df_2> <df_3> <out_df.csv>")
    exit(1)
A = pd.read_csv(sys.argv[1], index_col=0)
B = pd.read_csv(sys.argv[2], index_col=0)
C = pd.read_csv(sys.argv[3], index_col=0)

D = pd.concat([A,B,C])
# D = D.reset_index(drop=True)
# D = D.fillna(0.)
D.drop_duplicates(inplace=True)
D.to_csv(sys.argv[4])
print("Written to ", sys.argv[4])