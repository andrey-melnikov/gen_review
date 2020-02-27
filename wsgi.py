import json
from flask import Flask, jsonify, abort, request, render_template
from celery import Celery
import datetime
import Main

application = Flask(__name__)
application.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
application.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

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
	file_id = str(id_user+" "+str(datetime.datetime.now()))
	id_target = request.json['id_target']
	lang = request.json['lang']
	reviews_amount = (int)(request.json['reviews_amount'])
	mode=request.json['length']
	ratings=(int)(request.json['ratings'])
	try:
		similar_ids = request.json['similar_ids']
	except:
		similar_ids=[]

	task = generating.apply_async(args=[id_target,lang,reviews_amount,ratings,mode,file_id,similar_ids])
	return jsonify({'task_id':task.id, 'file_id':file_id}), 202

@celery.task(bind=True)
def generating(self,id_target,lang,reviews_amount,ratings,mode,name, similar_ids):
	Main.main(id_target,lang,reviews_amount,ratings,mode,name,similar_ids)





@application.route("/api/v1.0/get_reviews", methods=['GET'])
def get_reviews():
	file_id = request.json['file_id']
	ratings = (int)(request.json['ratings'])
	try:
		output_path = "output/reviews/"+session['file_id']+".txt"
		output_file = open(output_path, 'r',encoding='utf-8')
	except:
		return "File does not exist"
	r = {}
	i=0
	for line in output_file:
		rating = int(line[0])
		if(ratings==1 and rating>=4 or ratings==0 and rating==3 or ratings==-1 and rating<=2):
			r.update({str(i):line[2:]})
			i+=1
	return r


@application.route("/api/v1.0/progress/<task_id>")
def taskstatus(task_id):
    task = generating.AsyncResult(task_id)
    if task.state == 'PENDING':
        # job did not start yet
        response = {
            'state': task.state,
            'current': 0,
            'total': 1,
            'status': 'Pending...'
        }
    elif task.state != 'FAILURE':
        response = {
            'state': task.state,
            'current': task.info.get('current', 0),
            'total': task.info.get('total', 1),
            'status': task.info.get('status', '')
        }
        if 'result' in task.info:
            response['result'] = task.info['result']
    else:
        # something went wrong in the background job
        response = {
            'state': task.state,
            'current': 1,
            'total': 1,
            'status': str(task.info),  # this is the exception raised
        }
    return jsonify(response)


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
