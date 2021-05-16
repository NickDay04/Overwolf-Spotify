from flask import Flask, request, render_template, jsonify
from flask_restful import Api, Resource
import requests
import json

app = Flask(__name__)
api = Api(app)

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

        response = requests.post(f"https://accounts.spotify.com/api/token", data={"grant_type": "authorisation_code", "code": code, "redirect_uri": "https://overwolf-spotify-code.herokuapp.com", "client_id": "91b7ed5b61984131a7d7425d890dbdcf", "client_secret": "35557b16e54348f2a386df61ece15d06"})
        
        try:

            refreshToken = json.loads(response)["refresh_token"]
            return jsonify({"refresh_token": str(refreshToken)})
        
        except:

            return jsonify({"error": str(response)})


api.add_resource(Authorisation, "/clip/authorisation")
#endregion

if __name__ == "__main__":

    app.run(debug=True)