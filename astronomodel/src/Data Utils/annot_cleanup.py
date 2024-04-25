import pickle
import os
with open('annotations.pkl', 'rb') as handle:
    annotations = pickle.load(handle)
    

folder_path = 'Images'  # Path to your folder

# List all files in the folder
files = os.listdir(folder_path)
files = [x.split(".")[0] for x in files]

for f in files:
    if f not in annotations.keys():
        print(f)
print(f"Annotations: {len(annotations)}")
print(f"Images: {len(files)}")
