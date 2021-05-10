import json
import time
import requests
import tweepy
import random

user_id = "1386036098137305089"
user_name = "wimmelbuch"

with open("private_keys.json") as key_file:
    
    keyring = json.load(key_file)

    bearer_token = keyring["twitter bearer token"]
    api_key = keyring["twitter API key"]
    api_secret = keyring["twitter secret API key"]
    access_token = keyring["twitter access token"]
    access_secret = keyring["twitter access token"]

    tweet_opener = [
        "This image displays the notation",
        "Our next random Iconclass notation is",
        "Here we have the notation",
        "Next we're taking a look at",
        "This artwork is an instance of"
    ]
    comment_opener = [
        "Did you know?",
        "Fun fact:",
        "And what about other examples?",
        "Are you interested in finding a different example?"
    ]

    with open("twitter_files\\twitter_text_temp.json") as script:

        script_array = json.load(script)

        for obj in script_array:

            obj_num = obj["id"]
            obj_title = obj["title"]
            obj_creator = obj["creator"]
            obj_date = obj["date"]
            img_url = obj["source"]

            rijks_url = f"https://www.rijksmuseum.nl/en/collection/{obj_num}"

            item_matches = obj["total matches"]
            other_matches = item_matches - 1

            ic_num = obj["ic_num"]
            ic_desc = obj["ic_desc"]

            random_opener = random.choice(tweet_opener)
            random_comment = random.choice(comment_opener)

            tweet_string = f'{random_opener} {ic_num}, which is used to catalogue depictions of "{ic_desc}".'
            comment_string_1 = f'@{user_name} The pictured example is "{obj_title}", made by {obj_creator} in {obj_date}.'

            if other_matches > 1:
                comment_string_2 = f'@{user_name} {random_comment} Currently, the Rijksmuseum collection contains {other_matches} other items described using this notation.'
            if other_matches == 1:
                comment_string_2 = f'@{user_name} {random_comment} Currently, the Rijksmuseum collection contains only one other item described using this notation.'
            if other_matches < 1:
                comment_string_2 = f'@{user_name} {random_comment} Currently, this is the only item in the Rijksmuseum collection described using this notation.'
            
            auth = tweepy.OAuthHandler(api_key, api_secret)
            auth.set_access_token(access_token, access_secret)

            api = tweepy.API(auth)

            media = api.media_upload("twitter_files\\temp_img.jpg")

            api.update_status(status = tweet_string, media_ids = [media.media_id])

            time.sleep(10) #this break ensures that there is enough time for the tweet to post before the following code searches for it
            
            headers = {"Authorization": f"Bearer {bearer_token}"}
            tweet_lookup = requests.get(f"https://api.twitter.com/2/users/{user_id}/tweets", headers = headers)

            tweet_data = json.loads(tweet_lookup.text)

            status_id = tweet_data["meta"]["newest_id"]

            api.update_status(comment_string_1, status_id)

            time.sleep(10)

            status_id = tweet_data["meta"]["newest_id"]

            api.update_status(comment_string_2, status_id)




        
