#!/usr/bin/python
import requests

def get_reviews(dict):
	res = requests.get('http://gen-review.net/api/v1.0/get_reviews',json=dict)
	if res.ok:
		return (res.json())

def progress(task_id):
	res = requests.get('http://80.249.144.13:5000/api/v1.0/progress/'+task_id)
	if res.ok:
		return (res.json())

def post_id(dict):
	res = requests.post('http://gen-review.net/api/v1.0/gen', json=dict)
	if res.ok:
		return (res.json())	

def request_file_id(dict):
	res = requests.get('http://80.249.144.13:5000/api/v1.0/request_file_id', json=dict)
	if res.ok:
		return (res.json())	


def similar(dict):
	res = requests.get('http://80.249.144.13:5000/api/v1.0/similar_apps_count',json=dict)
	if res.ok:
		return (res.json())	

if __name__ == "__main__":
	dict = {'user_id':'user2',
			'target_id': 'com.ansangha.drjb',
			'lang':'en_US',
			'reviews_amount': 200,
			'length': "Short",
			'file_id':'user2 2020-02-27 22:53:44.456785',
			'ratings':1}
	#print(request_file_id({'user_id': 'user2'}))
	#print(post_id(dict))
	print(get_reviews({'file_id':'user2 2020-02-27 22:53:44.456785', 'ratings':"1"}))
	#print(progress("f635e99d-7737-4498-b9ec-501316093de3"))
	#print(similar({'target_id':'com.AndreyMelnikov.DroneRacingSimulator'}))