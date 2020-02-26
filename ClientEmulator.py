#!/usr/bin/python
import requests

def get_id():
	res = requests.get('http://gen-review.net/api/v1.0/id')
	if res.ok:
		return (res.json()['id'])

def post_id(dict):
	res = requests.post('http://gen-review.net/api/v1.0/gen', json=dict)
	if res.ok:
		return (res.json())	

if __name__ == "__main__":
	dict = {'id_user':'user2',
			'id_target': 'com.king.candycrushsaga',
			'lang':'en_US',
			'reviews_amount': 20,
			'length': "Short",
			'ratings':'1'}
	print(post_id(dict))