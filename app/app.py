import os
from flask import Flask, request, jsonify
import redis
from pymongo import MongoClient
from flask_caching import Cache
from bson.objectid import ObjectId


app = Flask(__name__)
REDIS_HOST = os.environ.get('REDIS_HOST', '127.0.0.1')
MONGO_HOST = os.environ.get('MONGO_HOST', '127.0.0.1')


cache = Cache(app, config={'CACHE_TYPE': 'redis', 'CACHE_REDIS_URL': 'redis://{redis_host}:6379/0'.format(redis_host=REDIS_HOST)})

#cache.cached()


#Добавление сообщения
@app.route('/addmessage', methods=['POST'])
@cache.cached()
def addmessage():
    data = request.form
    if data.get('text'):
        result = write_db({'text':data.get('text')})
        return jsonify({'ok': True, 'message': 'Message created successfully %s' % result}), 200
    return jsonify({'ok': False, 'message': 'Invalid field'}), 200
#curl -d "text=fdgdfgdfgdhfghgfhfgh" -X POST http://127.0.0.1:5000/addmessage

#Добавление тегов
@app.route('/addtag', methods=['POST'])
@cache.cached()
def addtag():
    data = request.form
    if data.get('message_id') and data.get('tag'):
        mongo_client = MongoClient(host=[MONGO_HOST])
        for tag in list(data.get('tag').split(',')):
            mongo_client.messages.message_collection.update_one({'_id':ObjectId(data.get('message_id'))}, {'$addToSet':{'tags':tag}})
        return jsonify({'ok': True, 'message': 'Tag added successfully'}), 200
    return jsonify({'ok': False, 'message': 'Invalid field'}), 200
#curl -d "message_id=5e9833df9f00be74ac864a66&tag=three,four" -X POST http://127.0.0.1:5000/addtag

#Добавление комментариев
@app.route('/addcomment', methods=['POST'])
@cache.cached()
def addcomment():
    data = request.form
    if data.get('message_id') and data.get('name') and data.get('text'):
        comment={}
        comment[data.get('name')] = data.get('text')
        mongo_client = MongoClient(host=[MONGO_HOST])
        mongo_client.messages.message_collection.update_one({'_id':ObjectId(data.get('message_id'))}, {'$addToSet':{'comments':comment}})
        return jsonify({'ok': True, 'message': 'Comment added successfully'}), 200
    return jsonify({'ok': False, 'message': 'Invalid field'}), 200
#curl -d "message_id=5e983716dba4e514aa981cb3&name=John&text=sdfsfsdf ds s sd new" -X POST http://127.0.0.1:5000/addcomment

#получение сообщения
@app.route('/message', methods=['GET'])
@cache.cached()
def sendmessage():
    data = request.form
    if data.get('message_id'):
        mongo_client = MongoClient(host=[MONGO_HOST])
        result = mongo_client.messages.message_collection.find_one({"_id":ObjectId(data.get('message_id'))})
        if result:
            return jsonify({'ok': True, 'message': 'Message found: %s' %result}), 200
    return jsonify({'ok': False, 'message': 'Not found'}), 404
#curl -d "message_id=5e983716dba4e514aa981cb3" -X GET http://127.0.0.1:5000/message


@app.route('/message-stats', methods=['GET'])
@cache.cached()
def message_stats():
    data = request.form
    if data.get('message_id'):
        mongo_client = MongoClient(host=[MONGO_HOST])
        result = mongo_client.messages.message_collection.find_one({"_id":ObjectId(data.get('message_id'))})
        res_dict = {}
        if result:
            for k in result:
                if k =='_id':
                    res_dict[k]=result[k]
                    continue
                res_dict[k]=len(result[k])
            return jsonify({'ok': True, 'message': 'Message stats: %s' %res_dict}), 200
    return jsonify({'ok': False, 'message': 'Not found'}), 404
#curl -d "message_id=5e983716dba4e514aa981cb3" -X GET http://127.0.0.1:5000/message-stats


def write_db(dict):
    mongo_client = MongoClient(host=[MONGO_HOST])
    result = mongo_client.messages.message_collection.insert_one(dict)
    return result.inserted_id

if __name__=='__main__':
    app.run(debug=True, host='0.0.0.0', port = 5000)
