from flask import Flask, jsonify,abort
import  csv
import time
import hashlib
import re
from flask import make_response
import datetime
from flask import request

app=Flask(__name__)
count = 0;
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error':'not found'}),404)
count = count + 1
# return total number of request
@app.route('/api/v1/_count',methods=['GET'])
def total_request():
    list=[]
    list.append(count)
    return make_response(jsonify(list),200)

# reset the request count to zero
@app.route('/api/v1/_count',methods=['DELETE'])
def set_request_zero():
    list=[]
    global count
    count = 0
    list.append(count)
    #return make_response(jsonify(list),200)
    return make_response(jsonify({}),200)





#2 list all users
@app.route('/api/v1/users',methods=['GET'])
def list_all_users():
    users=[]
    global count
    count = count + 1
    with open('users.csv') as csv_file:
        csv_reader=csv.reader(csv_file)
        for row in csv_reader:
            users.append(row[0])
    return jsonify(users)

#5 add users
@app.route('/api/v1/users',methods=['POST'])
def adde_user():
    global count
    count = count + 1
    if not request.json or not 'username' in request.json:
        abort(400)
    data=request.json
    cred={'username':data['username'],'password':data['password']}
    print(data)
    with open('users.csv') as users:
        user_reader=csv.reader(users,delimiter=',')
        user_flag=0
        for row in user_reader:
            if(row[0]==cred['username']):
                user_flag=1
            if(user_flag==1):
                return make_response(jsonify(),400)
    pass_hash=cred['password']
    pattern=re.compile(r'\b[0-9a-f]{40}\b')
    match=re.match(pattern,pass_hash)
    flag=0
    try:
        if(match.group(0)==pass_hash):
            flag=1
    except:
        pass
    if(flag==1):
        with open('users.csv','a') as csv_file:
            writer=csv.writer(csv_file)
            appe=[cred["username"],cred["password"]]
            writer.writerow(appe)
        return jsonify({}),201
    else:
        return jsonify(),400
#6 Delete a user
@app.route('/api/v1/users/<username>', methods=['DELETE'])
def delete_user(username):
	global count
	count = count + 1
	with open('users.csv') as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=',')
		flag=0
		for row in csv_reader:
			#print(row)
			if(row[0]==username):
				flag=1
		if(flag==0):
			return make_response(jsonify(),400)
	tl=[]
	with open('users.csv', 'rb') as f:
		reader = csv.reader(f)
		l = list(reader)
		for line in l:
			if(line[0]!=username):
				tl.append(line)
	print(tl)
	with open("users.csv", "wb") as f:
		writer = csv.writer(f)
		writer.writerows(tl)
	return jsonify({}), 200

if __name__=='__main__':
    app.run(host='0.0.0.0',port=80)

