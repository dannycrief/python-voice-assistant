import json
import re

import googlemaps


def get_api_key():
    api_file = open("api.txt", "r")
    api_key = api_file.readline()
    api_file.close()
    return api_key


def get_google_map_travel():
    api_key = get_api_key()
    google_maps = googlemaps.Client(key=api_key)
    user_address_from = input("Type your address (address, city): ")
    user_address_to = input("Where you want to go (address, city): ")

    directions_result = google_maps.directions(origin=user_address_from,
                                               destination=user_address_to,
                                               mode="driving")
    google_maps.static_map(size=13, center=user_address_from, zoom=13)
    with open('road.json', 'w') as of:
        json.dump(directions_result[0], of)

    travel_duration = directions_result[0]["legs"][0]["duration"]["text"].replace("mins", "minutes")
    travel_path = []
    for road in directions_result[0]["legs"][0]["steps"]:
        travel_path.append(re.sub("<.*?>", "", road["html_instructions"]))

    return travel_duration, travel_path


if __name__ == '__main__':
    get_google_map_travel()