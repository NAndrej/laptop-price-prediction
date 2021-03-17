import pandas as pd

def tostr(value):
    return str(value)


intel_data = pd.read_csv('cpus_data/intel_data.csv')
mediatek_data = pd.read_csv('cpus_data/mediatek_data.csv')
amd_data = pd.read_csv('cpus_data/amd_data.csv')
data = pd.read_csv('data.csv')

frames = [intel_data, mediatek_data, amd_data]
features = pd.concat(frames)
features["Name"] = features["Name"].apply(tostr)

unique_names = data.CPU.unique()

found = []
found_cpus = pd.DataFrame()

for name in unique_names:
    if name == " ":
        continue
    for cpu in features['Name']:
        if name.lower() in cpu.lower():
            found.append(features[features['Name'] == cpu])

new_df = pd.concat(found)
new_df = new_df[["Name","Cores","Threads","Base","Turbo"]]

new_df.to_csv("processor_data.csv")