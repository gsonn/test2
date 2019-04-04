from flask import Flask, jsonify,abort
import  csv
import time
import hashlib
import re
from flask import make_response
import datetime
from flask import request
import requests
app=Flask(__name__)
count = 0;
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error':'not found'}),404)
count = count + 1
#1 calling user microservice in acts microservice
def get_users(username):
        resp=requests.get('http://52.90.84.196:80/api/v1/users')
        if resp.status_code==204:
                return False
        users=resp.json()
        print(users)
        if username in users:
                return True
        return False

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

# get total number of acts
@app.route('/api/v1/acts/count',methods=['GET'])
def total_countsof_acts():
    global count 
    count = count + 1
    list=[]
    t_acts = 0
    with open('acts.csv') as csv_file:
        csv_reader=csv.reader(csv_file)
        for row in csv_reader:
            t_acts = t_acts + 1
        list.append(t_acts)
    return make_response(jsonify(list),200)





#1 list all categories
@app.route('/api/v1/categories',methods=['GET'])
def list_cat():
    global count
    count=count+1
    list={}
    with open('categories.csv') as csv_file:
        csv_reader=csv.reader(csv_file,delimiter=',')
        for row in csv_reader:
            list[row[0]]=int(row[1])
    return jsonify(list)

#3 Add a category
from flask import request
@app.route('/api/v1/categories',methods=['POST'])
def add_cat():
	global count
	count = count + 1
	if not request.json :
		abort(400)
	data=request.json
	aa=len(data)
	with open('categories.csv') as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=',')
		flag=0
		for row in csv_reader:
			if(row[0]==data[0]):
				flag=1
			if(flag==1):
				return make_response(jsonify({}),400)
	if(aa>1):
		return make_response(jsonify({}),400)
	with open('categories.csv', 'a') as csvFile:
		writer = csv.writer(csvFile)
		r=[data[0],0]
		writer.writerow(r)
	return jsonify({}), 201



#4 delete category
@app.route('/api/v1/categories/<categoryName>',methods=['DELETE'])
def delete_cat(categoryName):
    global count
    count = count + 1
    with open('categories.csv') as csv_file:
        csv_reader=csv.reader(csv_file,delimiter=',')
        delete_flag=0
        for row in csv_reader:
            if(row[0]==categoryName):
                delete_flag=1
        if(delete_flag==0):
            return make_response(jsonify({'Error': ' Resource does not exist'}),400)
    list=[]
    with open('categories.csv','rb') as file:
        reader=csv.reader(file)
        #list1=list(reader)
        #print(list1)
        for line in reader:
            if(line[0]!=categoryName):
                list.append(line)
    print(list)
    with open("categories.csv", "wb") as f:
        writer=csv.writer(f)
        writer.writerows(list)
    return jsonify({}), 200

#7 Add and act
@app.route('/api/v1/acts',methods=['POST'])
def add_act():
	global count
	count = count + 1
	if not request.json or not 'actId' in request.json or not 'username' or not 'timestamp' in request.json or not 'caption' in request.json or not 'imgB64' in request.json or not 'categoryName' in request.json:
		abort(400)
	d=[]
	actId=request.json['actId']
	category=request.json['categoryName']
	username=request.json['username']
	timestamp=request.json['timestamp']
	caption=request.json['caption']
	base64=request.json['imgB64']
	upvote=0
	try:
		datetime.datetime.strptime(timestamp, '%d-%m-%Y:%S-%M-%H')
		#print("valid")
        	su = get_users(username)
	except ValueError:
		return make_response(jsonify(timestamp),400)
	d.append(actId)
	d.append(category)
	d.append(username)
	d.append(timestamp)
	d.append(caption)
	d.append(upvote)
	d.append(base64)
	with open('acts.csv') as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=',')
		flag=0
		for row in csv_reader:
			if(int(row[0])==int(d[0])):
				flag=1
			if(flag==1):
				return make_response(jsonify(),400)
	with open('acts.csv') as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=',')
		flag=0
		for row in csv_reader:
			if(row[2]==d[2]):
				flag=1
			if(flag==1):
				return make_response(jsonify(),400)
	data=category
	ll1=[]
	with open('categories.csv') as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=',')
		flag=0
		for line in csv_reader:
			ll1.append(line)
	for row in ll1:
		if(row[0]==data):
			flag=1
		if(flag==1):
			row[1]=int(row[1])+1
	if(flag==0):
		return make_response(jsonify(flag),400)
	with open('categories.csv', 'w') as csvFile:
		writer = csv.writer(csvFile)
		writer.writerows(ll1)

	csvFile.close()


	with open('acts.csv', 'a') as csvFile:
		writer = csv.writer(csvFile)
		r=d
		writer.writerow(r)
	return jsonify({}), 201


#8 Remove an act
@app.route('/api/v1/acts/<actId>',methods=['DELETE'])
def remove_act(actId):
	global count
	count = count + 1
	category="temp"
	with open('acts.csv') as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=',')
		flag=0
		for row in csv_reader:
			#print(row)
			if(row[0]==actId):
				flag=1
				category=row[1]
		if(flag==0):
			return make_response(jsonify(),400)
	tl=[]
	with open('acts.csv', 'rb') as f:
		reader = csv.reader(f)
		l = list(reader)
		for line in l:
			if(line[0]!=actId):
				tl.append(line)
	#print(tl)
	with open("acts.csv", "wb") as f:
		writer = csv.writer(f)
		writer.writerows(tl)
	data=category
	ll1=[]
	with open('categories.csv') as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=',')
		flag=0
		for line in csv_reader:
			ll1.append(line)
	for row in ll1:
		if(row[0]==data):
			flag=1
		if(flag==1):
			row[1]=int(row[1])-1
	if(flag==0):
		return make_response(jsonify(flag),400)
	with open('categories.csv', 'w') as csvFile:
		writer = csv.writer(csvFile)
		writer.writerows(ll1)

	csvFile.close()
	return make_response(jsonify({}), 200)

#9 upvote an act
@app.route('/api/v1/acts/upvote',methods=['POST'])
def upvote_act():
	global count
	count = count + 1
	if not request.json :
		abort(400)
	data=request.json
	data=int(data[0])
	ll1=[]
	with open('acts.csv') as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=',')
		flag=0
		for line in csv_reader:
			ll1.append(line)
	for row in ll1:
		if(int(row[0])==data):
			flag=1
		if(flag==1):
			row[5]=int(row[5])+1
	if(flag==0):
		return make_response(jsonify(flag),400)
	with open('acts.csv', 'w') as csvFile:
		writer = csv.writer(csvFile)
		writer.writerows(ll1)
	csvFile.close()
	return make_response(jsonify(flag),200)


#10 List acts for a given category
@app.route('/api/v1/categories/<categoryname>/acts', methods=['GET'])
def list_acts_cat(categoryname):
	global count
	count = count + 1
	ll=[]
	with open('acts.csv', 'rb') as f:
		reader = csv.reader(f)
		l = list(reader)
	for line in l:
		details={}
		if(line[1]==categoryname):
			details["actId"]=int(line[0])
			details["category"]=line[1]
			details["username"]=line[2]
			details["timestamp"]=line[3]
			details["caption"]=line[4]
			details["upvotes"]=int(line[5])
			details["imgB64"]=line[6]
			ll.append(details)
	if(len(ll)>500):
		return make_response(jsonify({}),400)
	if(len(ll)==0):
		return make_response(jsonify({}),204)
	return make_response(jsonify(ll),200)


#11 list number of acts in a given category
@app.route('/api/v1/categories/<categoryname>/acts/size', methods=['GET'])
def list_num_acts_cat(categoryname):
	global count
	count = count + 1
	with open('categories.csv') as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=',')
		flag=0
		for row in csv_reader:
			if(row[0]==categoryname):
				flag=1
			if(flag==1):
				return make_response(jsonify([row[1]]),200)


	return make_response(jsonify({}),204)

#12 Acts in range of a given category
@app.route('/api/v1/categories/<categoryname>/acts', methods=['GET'])
def list_acts_cat_range(categoryname,start,end):
	global count
	count = count + 1
	ll=[]
	start=int(request.args.get('start'))
	end=int(request.args.get('end'))
	with open('acts.csv', 'rb') as f:
		next(f)
		reader = csv.reader(f)

		l = list(reader)
	for line in l:
		if(line[1]==categoryname):
			ll.append(line)
	ll.sort(key=lambda x: x[3][12])
	ll.sort(key=lambda x: x[3][11])
	ll.sort(key=lambda x: x[3][15])
	ll.sort(key=lambda x: x[3][14])
	ll.sort(key=lambda x: x[3][18])
	ll.sort(key=lambda x: x[3][17])
	ll.sort(key=lambda x: x[3][0])
	ll.sort(key=lambda x: x[3][1])
	ll.sort(key=lambda x: x[3][3])
	ll.sort(key=lambda x: x[3][4])
	ll.sort(key=lambda x: x[3][3])
	ll.sort(key=lambda x: x[3][9])
	ll.sort(key=lambda x: x[3][8])
	ll.sort(key=lambda x: x[3][7])
	ll.sort(key=lambda x: x[3][6])
	ll.reverse()
	a=end-start+1
	#if(a>500):
	return make_response(jsonify({start}),200)


if __name__=='__main__':
    app.run(host='0.0.0.0',port=80)

