import os
import json

# Define the root directory where the subfolders are located
root_dir = '.'

# Define the old and new paths to be replaced
old_path_substring = "/gpfs/bbp.cscs.ch/project/proj135/home/petkantc/axon/axonal-projection/axon_projection/validation/circuit-build/lite_iso_final/sonata//struct_circuit_config.json"
new_path_substring = "/gpfs/bbp.cscs.ch/project/proj135/home/petkantc/axon/axonal-projection/axon_projection/validation/circuit-build/lite_iso_final/auxiliary/struct_circuit_config_fake.json"

# Function to update the "path" fields in the JSON data
def update_paths_in_json(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)

    # Check if "models" key exists and iterate over its contents
    models = data.get('models', [])
    for model in models:
        loader = model.get('loader', {})
        if 'path' in loader and old_path_substring in loader['path']:
            # Replace the old substring with the new one
            loader['path'] = loader['path'].replace(old_path_substring, new_path_substring)
            print(f'Updated path in {file_path}: {loader["path"]}')

    # Write the updated data back to the file
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)

# Walk through the directory structure and find all config.json files
for subdir, dirs, files in os.walk(root_dir):
    for file in files:
        if file == 'config.json':
            file_path = os.path.join(subdir, file)
            update_paths_in_json(file_path)

print('Path update completed.')
