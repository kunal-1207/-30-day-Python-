import os

for file in os.listdir("."):
    if file.endswith(".log"):
        os.rename(file, file + ".bak")
