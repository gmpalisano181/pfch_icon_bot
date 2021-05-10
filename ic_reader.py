#this script takes the raw data of every possible Iconclass permutation and converts it to a local .json array consisting of a single list containing every possible notation

import json

notation_list = []

with open("data\\iconclass_full.ndjson") as ic_file:       #<----acquired from http://www.iconclass.org/help/lod

    index = 0

    for line in ic_file:
        ic_content = json.loads(line)
        
        notation = (ic_content["skos:notation"])  

        notation_list.append(notation)

        index += 1
        
        print(f"{index} total notations listed")

with open("data\\ic_heading_list.json", "w") as save_data:
    json.dump(notation_list, save_data, indent = 2)
