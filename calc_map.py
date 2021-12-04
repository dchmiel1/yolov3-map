from genericpath import isfile
import subprocess
from os import listdir
from os.path import isfile

data_file = "data/obj.data"
cfg_file = "cfg/yolov3_map.cfg"
weights_folder = "backup"

if __name__ == "__main__":

    weights_files = [f for f in listdir(weights_folder) if isfile(f"{weights_folder}/{f}") and f.endswith(".weights")]

    print(weights_files)
    to_save = ""
    aps = []

    for weights_file in weights_files:
        std_out = subprocess.Popen(["./darknet", "detector", "map", data_file, cfg_file, f"{weights_folder}/{weights_file}"], stdout=subprocess.PIPE).communicate()[0]
        print(std_out)
        std_out = std_out.decode("utf-8")
        _split = std_out.split("class_id = 0")
        _split = _split[1].split("\n\n\n")
        to_save += "class_id = 0" + _split[0]
        ap = float(_split[1])
        aps.append((ap, weights_file))
        to_save +=f"\n{ap}\n\n"
    
    aps.sort()
    to_save += str(aps)
    with open("output.txt", "w") as file:
        file.write(to_save)
