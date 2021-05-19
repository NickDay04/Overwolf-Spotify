import requests
import json

code = input()

response = requests.post(f"https://overwolf-spotify-code.herokuapp.com/clip/authorisation?code={code}")

refreshToken = json.loads(json.loads(response.text)["response"].replace("\\", ""))["refresh_token"]
print(refreshToken)