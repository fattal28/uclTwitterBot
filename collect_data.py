import requests
import json
import tweepy

with open("secret.json", 'r') as f:
    secret = json.load(f)

with open("weird_socs.json", 'r') as f:
    weird_socs = json.load(f)

bookings = []

for search_term in weird_socs + ["Society"]:

    params = {
        "token": secret['uclapikey'],
        "results_per_page": "1000",
        "contact": search_term
    }

    req = requests.get(
        "https://uclapi.com/roombookings/bookings",
        params=params
    )
    resp = req.json()

    print(resp)

    bookings += resp["bookings"]

    next_page = resp["next_page_exists"]
    counter = 0
    while next_page:
        page_token = resp["page_token"]
        params = {
            "token": secret['uclapikey'],
            "page_token": page_token
        }
        pagination_req = requests.get(
            "https://uclapi.com/roombookings/bookings",
            params=params
        )
        pagination_resp = pagination_req.json()
        bookings += pagination_resp["bookings"]
        if pagination_resp["next_page_exists"] and counter < 11:
            next_page = True
            counter += 1
        else:
            next_page = False

    with open('bookings.json', 'w') as f:
        f.write(
            json.dumps({
                "bookings": bookings
            }, sort_keys=True, indent=4)
        )
