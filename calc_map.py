from genericpath import isfile
import subprocess
from os import listdir
from os.path import isfile

data_file = "data/obj.data"
cfg_file = "cfg/yolov3_ndds_final.cfg"
weights_folder = "backup/"

if __name__ == "__main__":

    weights_files = [f for f in listdir(weights_folder) if isfile(f) and f.endswith(".weights")]

    print(weights_files)
    to_save = ""
    aps = []

    for weights_file in weights_files:
        std_out = subprocess.Popen(["./darknet", "detector", "map", data_file, cfg_file, f"{weights_folder}/{weights_file}"], stdout=subprocess.PIPE).communicate()[0]
        print(std_out)
        _split = std_out.split("\n\n\n")
        to_save += _split[0]
        ap = float(_split[1])
        aps.append((ap, weights_file))
        to_save +=f"\n{ap}\n\n"
    
    aps.sort()
    to_save += aps
    with open("output.txt", "w") as file:
        file.write(to_save)
