import os

folder_path = "C:/fixie/fixie-hack23/agents/trainingdata" # replace with the path to your folder containing text files
files = os.listdir(folder_path)

data = {}

for file in files:
    if file.endswith(".txt"):
        with open(os.path.join(folder_path, file), "r") as f:
            content = f.read()
            key = os.path.splitext(file)[0] # get the filename without the extension
            data[key] = content

print(data)