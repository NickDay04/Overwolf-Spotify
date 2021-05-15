from flask import Flask, request, render_template
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)

#region HOME {WEBSITE HOME PAGE}
@app.route("/")
def home():

    return render_template("home.html")
#endregion

#region WEBSITE {SHOW USER CODE}
# https://accounts.spotify.com/authorize?client_id=91b7ed5b61984131a7d7425d890dbdcf&response_type=code&redirect_uri=https%3A%2F%2Foverwolf-spotify-code.herokuapp.com/code%2Fmain.html&show_dialog=false
@app.route("/code")
def Get_User_Code():

    code = request.args.get("code")

    return render_template("clip.html", code=code)
#endregion

#region API
class HelloWorld(Resource):

    def get(self):

        return {"Hello world!"}

api.add_resource(HelloWorld, "/helloworld")
#endregion

if __name__ == "__main__":

    app.run(debug=True)