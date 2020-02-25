import sys
from flask import Flask
from flask_restful import Api, Resource,reqparse
app = Flask(__name__)
api =Api(application)
source_id   = ""

class Command(Resource):
	def get(self,name):
		global source_id
		if name == "source":
			return source_if, 201
		return "Command not found", 404
	def put(self,name):
		global source_id
		if name == "source":
			parse = reqparse.RequestParser()
			parser.add_argument("id")
			args = parser.parse_args()
			source_id = args["id"]
			return "App id is setted: "+source_id,201
		return "Command not found", 404


@app.route("/")
def hello():
	return "<h1 style='color:blue'>Hello!</h1>"

if __name__ == "__main__":
	api.add_resource(Command, "/command/<string:name>"
	app.run(host='80.249.144.13')
