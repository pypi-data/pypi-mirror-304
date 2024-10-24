import pandas as pd
import plotly.express as px

# Load the CSV data
csv_file = '/gpfs/bbp.cscs.ch/data/project/proj135/home/petkantc/axon/axonal-projection/axon_projection/validation/circuit-build/lite_MOp5_only/target_pts.csv'
data = pd.read_csv(csv_file)

# Extract the target_x, target_y, and target_z columns
target_x = data['target_x']
target_y = data['target_y']
target_z = data['target_z']

# Create a 3D scatter plot with plotly
fig = px.scatter_3d(data, x='target_x', y='target_y', z='target_z',
                    labels={'target_x': 'Target X', 'target_y': 'Target Y', 'target_z': 'Target Z'},
                    title='3D Scatter Plot of Target Coordinates')

# save the interactive plot
fig.savefig("target_pts.html")