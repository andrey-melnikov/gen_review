import json
from flask import Flask, jsonify, abort, request, render_template, session
from celery import Celery
import datetime
import Main
import os

application = Flask(__name__)
application.secret_key="hello"
application.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
application.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'
application.conf.update(BROKER_URL=os.environ['REDIS_URL'],CELERY_RESULT_BACKEND=os.environ['REDIS_URL'])

celery = Celery(application.name, broker=application.config['CELERY_BROKER_URL'])
celery.conf.update(application.config)




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
def gen():
	id_user = request.json['id_user']
	with open('users.txt','r') as json_file:
		if (id_user in json.load(json_file)) == False:
			return  abort(404)
	session['file_id'] = str(id_user+" "+str(datetime.datetime.now()))
	id_target = request.json['id_target']
	lang = request.json['lang']
	reviews_amount = (int)(request.json['reviews_amount'])
	mode=request.json['length']
	ratings=(int)(request.json['ratings'])
	try:
		similar_ids = request.json['similar_ids']
	except:
		similar_ids=[]

	generating.delay(id_target,lang,reviews_amount,ratings,mode,session['file_id'],similar_ids)
	return jsonify({'file_id':session['file_id']})
	#return jsonify({'return':'Generating reviews for '+id_target}),201

@celery.task
def generating(id_target,lang,reviews_amount,ratings,mode,name, similar_ids):
	Main.main(id_target,lang,reviews_amount,ratings,mode,name,similar_ids)





@application.route("/api/v1.0/get_reviews", methods=['GET'])
def get_reviews():
	if 'file_id' in session:
		ratings = (int)(request.json['ratings'])
		output_path = "output/reviews/"+session['file_id']+".txt"
		output_file = open(output_path, 'r',encoding='utf-8')
		r = {}
		i=0
		for line in output_file:
			rating = int(line[0])
			if(ratings==1 and rating>=4 or ratings==0 and rating==3 or ratings==-1 and rating<=2):
				r.update({str(i):line[2:]})
				i+=1
		return r
	else:
		return 'no session'





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
