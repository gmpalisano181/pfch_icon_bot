#this script takes the local directory of the Rijksmuseum's full inventory and converts it into a single .json array that is stripped down to only include the data necessary to the selection process

import json
import glob

rijks_ic = []

index = 0

for file_name in glob.glob("data\\id_directory_\\*.json"):
        
    index += 1

    print(f"{index}/664611 transferred")

    with open(file_name, "r") as file_data:

        file_entry = json.load(file_data)
        inv_num = file_entry["artObject"]["objectNumber"]
        img_availability = file_entry["artObject"]["hasImage"]

        try:
            ic_id = file_entry["artObject"]["classification"]["iconClassIdentifier"]
        except:
            ic_id = []

        list_entry = {
            "object ID" : inv_num,
            "Iconclass" : ic_id
        }

        if img_availability == True:
            rijks_ic.append(list_entry)

with open("data\\rijks_ic_headings.json", "w") as save_file:
    json.dump(rijks_ic, save_file, indent = 2)