import requests

code = input()

print(requests.post(f"https://overwolf-spotify-code.herokuapp.com/clip/authorisation?code={code}").text)