#this script takes a .csv containing every object id in the Rijksmuseum's inventory and converts it into a local directory of files which each correspond to the full metadata for a single object 

import requests
import csv
import json
import os
from itertools import islice

with open("rma_csv_collection.csv", errors = "ignore") as full_inventory:          #<----acquired from https://data.rijksmuseum.nl/object-metadata/download/

    index = 0

    last_used = 667895

    for row in islice(csv.reader(full_inventory), last_used, None): 
        
        index +=1 

        object_id = row[0]

        api_key = "" #insert Rijksmuseum API key here

        item_request = requests.get(f"https://www.rijksmuseum.nl/api/en/collection/{object_id}?key={api_key}")

        if item_request.status_code != 200:
            print(f"{object_id} experienced an error.")
        
        else:
            print(f"{object_id} was extracted successfully. Total extractions: {index}")
            
            inventory_entry = json.loads(item_request.text)
        
            if not os.path.exists(f"id_directory\\{object_id}.json"):
                with open(f"id_directory\\{object_id}.json", "w") as save_data:
                    json.dump(inventory_entry, save_data, indent = 2)
                        

        

                
