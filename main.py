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

    def getAccessToken(self):

        refreshResponse = requests.post("https://accounts.spotify.com/api/token", data={"grant_type": "refresh_token", "refresh_token": self.refreshToken, "client_id": "91b7ed5b61984131a7d7425d890dbdcf", "client_secret": "35557b16e54348f2a386df61ece15d06"})
        return json.loads(refreshResponse.text)["access_token"]

    def getCurrentDevice(self):

        refreshResponse = json.loads(requests.get("https://api.spotify.com/v1/me/player/devices", headers={"Accept": "application/json", "Content-Type": "application/json", "Authorization": f"Bearer {self.accessToken}"}).text)

        for i in list(refreshResponse["devices"]):

            if bool(i["is_active"]):

                return i["id"]
        
        else:

            return "no active devices"

    def put(self):

        self.refreshToken = request.args["refreshToken"]
        self.accessToken = self.getAccessToken()
        self.currentDeviceID = self.getCurrentDevice()

        response = requests.get("https://api.spotify.com/v1/me/player/currently-playing", headers={"Authorization": f"Bearer {accessToken}", "Accept": "application/json", "Content-Type": "application/json"})

        if (json.loads(response.text)["is_playing"]): # Currently playing

            self.Pause()

        else: # Not currently playing

            self.Play()


api.add_resource(Authorisation, "/clip/authorisation")
api.add_resource(PausePlay, "/clip/pauseplay")
#endregion

if __name__ == "__main__":

    app.run(debug=True)
