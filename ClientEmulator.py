#!/usr/bin/python
import requests

def get_id():
	res = requests.get('http://80.249.144.13:5000/api/v1.0/id')
	if res.ok:
		return (res.json()['id'])

def post_id(dict):
	res = requests.post('http://80.249.144.13:5000/api/v1.0/gen', json=dict)
	if res.ok:
		return (res.json())	

if __name__ == "__main__":
	dict = {'id_user':'user2',
			'id_target': 'com.ansangha.drjb',
			'lang':'en_US',
			'reviews_amount': 200,
			'length': "Short",
			'ratings':1}
	print(post_id(dict))