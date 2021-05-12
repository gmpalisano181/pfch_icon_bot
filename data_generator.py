import random
import json
import requests
import datetime
import statistics
import urllib.request

with open("private_keys.json") as key_file:
    
    keyring = json.load(key_file)
    api_key = keyring["rijksmuseum API key"]

    item_match = []
    total_attempts = []
    total_matches = []

    twitter_output = []
    archive_output = []

    with open("twitter_files\\twitter_text_archive.json") as archive_file:

        archive_data = json.load(archive_file)

        for stat in archive_data["process_metadata"]:

            attempts = stat["number of attempts"]
            total_attempts.append(attempts)

            matches = stat["number of matches"]
            total_matches.append(matches)

    attempt_avg = round(statistics.mean(total_attempts))

    match_median = round(statistics.median(total_matches))

    fetch_attempts = 0

    while len(twitter_output) == 0:

        file_directory = "data\\ic_heading_list.json"

        with open(file_directory, "r") as ic_headings:

            ic_data = json.load(ic_headings)
            
            random_notation = random.choice(ic_data)

            todays_notation = f"{random_notation}"

            with open("data\\rijks_ic_headings.json", "r") as rijks_dir:

                fetch_attempts += 1

                dir_content = json.load(rijks_dir)

                for obj in dir_content:

                    inv_num = obj["object ID"]
                    ic_id = obj["Iconclass"]

                    if todays_notation in ic_id:
                        item_match.append(inv_num)

            if len(item_match) >= 1:
                if fetch_attempts > attempt_avg:
                    print(f"Today's selected notation is {todays_notation}. It required {fetch_attempts} attempts to find a notation with one or more matches, which is above the current average of {attempt_avg} attempts.")

                else:
                    print(f"Today's selected notation is {todays_notation}. It required {fetch_attempts} attempts to find a notation with one or more matches, which is below the current average of {attempt_avg} attempts.")

                todays_item = random.choice(item_match)

                if len(item_match) > match_median:
                    print(f"Today's selected item is {todays_item}. The collection has {len(item_match) - 1} other item(s) matching {todays_notation}, which is greater than the current median of {match_median} matches.")

                else:
                    print(f"Today's selected item is {todays_item}. The collection has {len(item_match) - 1} other item(s) matching {todays_notation}, which is less than the current median of {match_median} matches.")

                selected_item = requests.get(f"https://www.rijksmuseum.nl/api/en/collection/{todays_item}?key={api_key}")

                item_details = json.loads(selected_item.text)

                title = item_details["artObject"]["title"]
                creator = item_details["artObject"]["principalOrFirstMaker"]
                date = item_details["artObject"]["dating"]["presentingDate"]
                
                img_url = item_details["artObject"]["webImage"]["url"]
                file_name = "twitter_files\\temp_img.jpg"
                urllib.request.urlretrieve(img_url, file_name)

                uri_req = requests.get(f"http://iconclass.org/{todays_notation}.json")

                uri_text = json.loads(uri_req.text)

                acq_time = datetime.datetime.now()
                
                ic_desc = uri_text["txt"]["en"]

                twitter_text = {
                    "id" : todays_item,
                    "title" : title,
                    "creator" : creator,
                    "date" : date,
                    "source" : img_url,
                    "ic_num" : todays_notation,
                    "ic_desc" : ic_desc,
                    "total matches" : len(item_match)
                } 
                twitter_output.append(twitter_text)

                archive_data = {
                    "selected item" : title,
                    "object ID" : todays_item,
                    "iconclass notation" : todays_notation,
                    "iconclass description" : ic_desc,
                    "number of attempts" : fetch_attempts,
                    "number of matches" : len(item_match),
                    "all matches" : item_match,
                    "created on" : acq_time
                }
                archive_output.append(archive_data)

            else: 
                print("\t", f"Error: The collection does not have any items matching {todays_notation}. Restarting...")

with open("twitter_files\\twitter_text_temp.json", "w") as temp_file:
    json.dump(twitter_output, temp_file, indent = 2)

def write_json(archive_output, filename = "twitter_files\\twitter_text_archive.json"):

    with open(filename, "w") as archive_file:
        json.dump(archive_output, archive_file, indent = 2, default = str)

with open("twitter_files\\twitter_text_archive.json") as new_archive:

    archive_output = json.load(new_archive)
    update = archive_output["process_metadata"]
    update.append(archive_data)

write_json(archive_output)
