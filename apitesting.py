import requests

code = input()

print(requests.post(f"https://overwolf-spotify-code.herokuapp.com/code/authorisation/{code}/91b7ed5b61984131a7d7425d890dbdcf/35557b16e54348f2a386df61ece15d06").text)