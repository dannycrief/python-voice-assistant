import requests
api_file = open("api-key.txt", "r")
api_key = api_file.readline()
api_file.close()

phrase = "How long do I need to go from Warsaw to Kiev"
phrase = phrase[phrase.index('from'):].split()
home = phrase[1]

work = phrase[-1]

url = "https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&"

r = requests.get(url + "origins=" + home + "&destinations=" + work + "&key=" + api_key)

time = r.json()["rows"][0]["elements"][0]["duration"]["text"]
seconds = r.json()["rows"][0]["elements"][0]["duration"]["value"]

print(f"The total travel time from {home} to {work} is {time}")
