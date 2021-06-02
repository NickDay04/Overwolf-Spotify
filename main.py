from flask import Flask, request, render_template, jsonify, Response
from flask_restful import Api, Resource
from flask_cors import CORS
import requests
import json

app = Flask(__name__)
api = Api(app)
core = CORS(app, resources={r"/clip/*": {"origins": "*"}})

#region HOME {WEBSITE HOME PAGE}
@app.route("/")
def home():

    return render_template("home.html")
#endregion

#region WEBSITE {SHOW USER CODE} /* COMPLETE */
# https://accounts.spotify.com/authorize?client_id=91b7ed5b61984131a7d7425d890dbdcf&response_type=code&redirect_uri=https%3A%2F%2Foverwolf-spotify-code.herokuapp.com%2Fcode&show_dialog=false
@app.route("/code")
def Get_User_Code():

    code = request.args.get("code")

    return render_template("clip.html", code=code)
#endregion

#region API

def getAccessToken(refreshToken):

    refreshResponse = requests.post("https://accounts.spotify.com/api/token", data={"grant_type": "refresh_token", "refresh_token": refreshToken, "client_id": "91b7ed5b61984131a7d7425d890dbdcf", "client_secret": "35557b16e54348f2a386df61ece15d06"})
    return json.loads(refreshResponse.text)["access_token"]

def getCurrentDevice(accessToken):

    refreshResponse = json.loads(requests.get("https://api.spotify.com/v1/me/player/devices", headers={"Accept": "application/json", "Content-Type": "application/json", "Authorization": f"Bearer {accessToken}"}).text)

    for i in list(refreshResponse["devices"]):

        if bool(i["is_active"]):

            return i["id"]
    
    else:

        return "no active devices"

class Authorisation(Resource):

    def post(self):

        code = request.args["code"]

        response = requests.post(f"https://accounts.spotify.com/api/token", data={"grant_type": "authorization_code", "code": code, "redirect_uri": "https://overwolf-spotify-code.herokuapp.com/code", "client_id": "91b7ed5b61984131a7d7425d890dbdcf", "client_secret": "35557b16e54348f2a386df61ece15d06"})
        
        apiResponse = Response()
        apiResponse.body = {"response"}

        return jsonify({"response": str(response.text)})

class PausePlay(Resource):

    def Pause(self):

        data = {"Authorization": f"Bearer {self.accessToken}", 
            "Accept": "application/json", 
            "Content-Type": "application/json", 
            "device_id": self.currentDeviceID}

        response = requests.put("https://api.spotify.com/v1/me/player/pause", headers=data)

    def Play(self):

        data = {"Authorization": f"Bearer {self.accessToken}", 
            "Accept": "application/json", 
            "Content-Type": "application/json", 
            "device_id": self.currentDeviceID}

        response = requests.put("https://api.spotify.com/v1/me/player/play", headers=data)

    def put(self):

        self.refreshToken = request.args["refreshToken"]
        self.accessToken = getAccessToken(self.refreshToken)
        self.currentDeviceID = getCurrentDevice(self.accessToken)

        response = requests.get("https://api.spotify.com/v1/me/player/currently-playing", headers={"Authorization": f"Bearer {self.accessToken}", "Accept": "application/json", "Content-Type": "application/json"})

        if (json.loads(response.text)["is_playing"]): # Currently playing

            self.Pause()

        else: # Not currently playing

            self.Play()


class Previous(Resource):

    def post(self):

        self.refreshToken = request.args["refreshToken"]
        self.accessToken = getAccessToken(self.refreshToken)
        self.currentDeviceID = getCurrentDevice(self.accessToken)

        response = requests.post(f"https://api.spotify.com/v1/me/player/previous?device_id={self.currentDeviceID}", headers={"Accept": "application/json", "Content-Type": "application/json", "Authorization": f"Bearer {self.accessToken}"})


class Next(Resource):

    def post(self):

        self.refreshToken = request.args["refreshToken"]
        self.accessToken = getAccessToken(self.refreshToken)
        self.currentDeviceID = getCurrentDevice(self.accessToken)

        response = requests.post(f"https://api.spotify.com/v1/me/player/next?device_id={self.currentDeviceID}", headers={"Accept": "application/json", "Content-Type": "application/json", "Authorization": f"Bearer {self.accessToken}"})


class ChangeVol(Resource):

    def getCurrentVolume(self):

        refreshResponse = json.loads(requests.get("https://api.spotify.com/v1/me/player/devices", headers={"Accept": "application/json", "Content-Type": "application/json", "Authorization": f"Bearer {self.accessToken}"}).text)
        for i in list(refreshResponse["devices"]):

            if bool(i["is_active"]):

                return i["volume_percent"]
            
            else:

                return "no active devices"

    def put(self):

        self.refreshToken = request.args["refreshToken"]
        self.mode = request.args["mode"] # volup or voldown
        self.accessToken = getAccessToken(self.refreshToken)
        self.currentDeviceID = getCurrentDevice(self.accessToken)
        self.currentVolume = self.getCurrentVolume()

        if self.currentVolume != "no active devices":

            if self.mode == "up":

                self.newVol = self.currentVolume + 10
                if self.newVol > 100:

                    self.newVol = 100

            else:

                self.newVol = self.currentVolume - 10
                if self.newVol < 0:

                    self.newVol = 0
        
            response = requests.put(f"https://api.spotify.com/v1/me/player/volume?volume_percent={self.newVol}&device_id={self.currentDeviceID}", headers={"Accept": "application/json", "Content-Type": "application/json", "Authorization": f"Bearer {self.accessToken}"})


# TODO: program this to return the song title and artist name for the headers, and the volume for the slider
# class GetInfo(Resource):

#     def get(self):

#         self.refreshToken = request.args["refreshToken"]

#         return songTitle, artistName, volume

api.add_resource(Authorisation, "/clip/authorisation")
api.add_resource(PausePlay, "/clip/pauseplay")
api.add_resource(Previous, "/clip/previous")
api.add_resource(Next, "/clip/next")
api.add_resource(ChangeVol, "/clip/changevol")
#endregion

if __name__ == "__main__":

    app.run(debug=True)
