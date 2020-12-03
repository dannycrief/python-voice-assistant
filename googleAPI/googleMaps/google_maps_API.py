import json
import re

import googlemaps


def get_api_key():
    api_file = open("googleAPI/googleMaps/api.txt", "r")
    api_key = api_file.readline()
    api_file.close()
    return api_key


def get_google_map_travel(user_address_from, user_address_to):
    api_key = get_api_key()
    google_maps = googlemaps.Client(key=api_key)

    directions_result = google_maps.directions(origin=user_address_from,
                                               destination=user_address_to,
                                               mode="driving")
    with open('road.json', 'w') as of:
        json.dump(directions_result[0], of)

    travel_duration = directions_result[0]["legs"][0]["duration"]["text"].replace("mins", "minutes")
    travel_path = []
    for road in directions_result[0]["legs"][0]["steps"]:
        road["html_instructions"] = re.sub("<\W.*?>.*?", ". ", road["html_instructions"])
        road["html_instructions"] = re.sub("<\w.*?>.*?", "", road["html_instructions"])
        road["html_instructions"] = road["html_instructions"].replace(". /", "/").replace(". ,", ",").replace(".  ",
                                                                                                              " ")
        travel_path.append(road["html_instructions"])

    return travel_duration, travel_path


if __name__ == '__main__':
    print(get_google_map_travel("warsaw", "katowice")[1])
