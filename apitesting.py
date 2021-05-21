import requests
import json

# code = input()

# response = requests.post(f"https://overwolf-spotify-code.herokuapp.com/clip/authorisation?code={code}")

# refreshToken = json.loads(json.loads(response.text)["response"].replace("\\", ""))["refresh_token"]
# print(refreshToken)

# with open("C:\\Windows\\System32\\refreshToken.txt", "r") as refreshTokenTxt:

#     refreshToken = refreshTokenTxt.read()

refreshToken = "AQBijdRb9PWK4hcovKqtUlsMRNbpfiu4TXVOfoAK_Y4Dn2QRV5pQn7mIlYufNgYBID57eUXu_WtI5iWw3Z3Ysn4Wn0-EW9OwYgXP0cLagYkuLcWFMQqQx_qrHh7na8C43uI"

refreshResponse = requests.post("https://accounts.spotify.com/api/token", data={"grant_type": "refresh_token", "refresh_token": refreshToken, "client_id": "91b7ed5b61984131a7d7425d890dbdcf", "client_secret": "35557b16e54348f2a386df61ece15d06"})
accessToken = json.loads(refreshResponse.text)["access_token"]

# data = {"Authorization": f"Bearer {accessToken}", 
#     "Accept": "application/json", 
#     "Content-Type": "application/json", 
#     "device_id": "dd9d11375d60526824305b61f5599e6257783f74"}

# response = requests.put("https://api.spotify.com/v1/me/player/play", headers=data)

# response = requests.get("https://api.spotify.com/v1/me/player/currently-playing", headers={"Authorization": f"Bearer {accessToken}", "Accept": "application/json", "Content-Type": "application/json"})
# print(response.text)

refreshResponse = json.loads(requests.get("https://api.spotify.com/v1/me/player/devices", headers={"Accept": "application/json", "Content-Type": "application/json", "Authorization": f"Bearer {accessToken}"}).text)
print(list(refreshResponse["devices"]))

# for i in list(refreshResponse["devices"]):

#     if bool(i["is_active"]):

#         print(i["id"])

# response = requests.put("https://overwolf-spotify-code.herokuapp.com/clip/pauseplay?refreshToken=AQBijdRb9PWK4hcovKqtUlsMRNbpfiu4TXVOfoAK_Y4Dn2QRV5pQn7mIlYufNgYBID57eUXu_WtI5iWw3Z3Ysn4Wn0-EW9OwYgXP0cLagYkuLcWFMQqQx_qrHh7na8C43uI")
# print(response.text)
