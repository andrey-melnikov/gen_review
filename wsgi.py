import json
from flask import Flask, jsonify, abort, request, render_template, session
from Main import main
import datetime

application = Flask(__name__)
application.secret_key="hello"

@application.route("/")
@application.route("/index")
def index():
	return render_template('index.html', title='Gen-Review')

@application.route("/api")
def api_info():
	return render_template('api.html')

@application.route("/example")
def example():
	return render_template('example.html')

@application.route("/api/v1.0/gen", methods=['POST'])
def generate():
	id_user = request.json['id_user']
	with open('users.txt','r') as json_file:
		if (id_user in json.load(json_file)) == False:
			return  abort(404)
	session['time'] = str(datetime.datetime.now())
	id_target = request.json['id_target']
	lang = request.json['lang']
	reviews_amount = (int)(request.json['reviews_amount'])
	mode=request.json['length']
	ratings=(int)(request.json['ratings'])
	try:
		similar_ids = request.json['similar_ids']
	except:
		similar_ids=[]
	main(id_target,lang,reviews_amount,ratings,mode,session['time'],similar_ids)
	#return jsonify({'return':'Generating reviews for '+id_target}),201

@application.route("/api/v1.0/get_reviews", methods=['GET'])
def get_reviews():
	if 'time' in session:
		ratings = request.json['ratings']
		output_path = "output/reviews/"+session['time']+".txt"
		output_file = open(output_path, 'r',encoding='utf-8')
		r = []
		for line in output_file:
			rating = int(line[0])
			if(ratings==1 & rating>=4 | ratings==0 & rating==3 | ratings==-1 & rating<=2):
				r.append(line[2:])
		return r

@application.route("/api/v1.0/progress",methods=['GET'])
def progress():
	#to-do return the progress
	#if there is no generation then return the message
	return abort(404)

#@application.route("/api/v1.0/id/<int:id_id>",methods=['GET'])
#def get_id(id_id):
	#task =[task for task in tasks if task['id] == task_id]
	#if len(task) == 0: abort(404)
#	return jsonify({'task':task[0]})

if __name__ == "__main__":
	application.run(host="80.249.144.13")
