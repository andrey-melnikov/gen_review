import json
from flask import Flask, jsonify, abort, request, render_template
import datetime
import Main

application = Flask(__name__)

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

@application.route("/api/v1.0/similar_apps_exist", methods=['GET'])
def similar_apps_exist(target_id):
	return Main.similar_apps_exist(request.json['target_id']),200


@application.route("/api/v1.0/request_file_id", methods=['GET'])
def get_file_id():
	user_id = request.json['user_id']
	file_id = str(user_id+" "+str(datetime.datetime.now()))
	return jsonify({'file_id': file_id}),200

@application.route("/api/v1.0/gen", methods=['POST'])
def gen():
	user_id = request.json['user_id']
	with open('users.txt','r') as json_file:
		if (user_id in json.load(json_file)) == False:
			return  abort(404)
	file_id = request.json['file_id']
	target_id = request.json['target_id']
	lang = request.json['lang']
	reviews_amount = (int)(request.json['reviews_amount'])
	mode=request.json['length']
	ratings=(int)(request.json['ratings'])
	try:
		similar_ids = request.json['similar_ids']
	except:
		similar_ids=[]

	Main.main(target_id,lang,reviews_amount,ratings,mode,file_id,similar_ids)
	return ("Copleted generting reviews for "+target_id), 202






@application.route("/api/v1.0/get_reviews", methods=['GET'])
def get_reviews():
	file_id = request.json['file_id']
	ratings = (int)(request.json['ratings'])
	try:
		output_path = "output/reviews/"+file_id+".txt"
		output_file = open(output_path, 'r',encoding='utf-8')
	except:
		return abort(404)
	r = {}
	i=0
	for line in output_file:
		rating = int(line[0])
		if(ratings==1 and rating>=4 or ratings==0 and rating==3 or ratings==-1 and rating<=2):
			r.update({str(i):line[2:]})
			i+=1
	return r


#@application.route("/api/v1.0/id/<int:id_id>",methods=['GET'])
#def get_id(id_id):
	#task =[task for task in tasks if task['id] == task_id]
	#if len(task) == 0: abort(404)
#	return jsonify({'task':task[0]})

if __name__ == "__main__":
	application.run(host='80.249.144.13')
