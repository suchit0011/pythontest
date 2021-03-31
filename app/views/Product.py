from flask import Blueprint, render_template, request, jsonify 
import config
import json
import bson
from bson import json_util
from bson.objectid import ObjectId
product = Blueprint('product', __name__, template_folder='templates',   static_folder='static')
collection = config.connect()

# print('44', config.connect("users"))
# @app.route('/flextest', methods=["GET"])
# def get_flextest():
#  all_flextest = list(collection.find({}))
#  return json.dumps(all_flextest, default=json_util.default)

# @product.route('/product')
@product.route('/', methods=["GET"])
def productshome():
        all_flextest = list(collection.find({}))
        return json.dumps(all_flextest, default=json_util.default)
        # Do some stuff
        # return render_template('product/product.html')

@product.route('/productbuy', methods=["POST"])
def productsbuy():
         name = request.json['name']
         email = request.json['email']
         results  = collection.insert_one({'name': name,'email':email}).inserted_id
         new_result = list(collection.find({'_id': results}))
         ourresult = {'ids':str(new_result[0]['_id']),'name':new_result[0]['name'],'email':new_result[0]['email']}
         return jsonify(customers=ourresult)  


@product.route('/productdetail', methods=["POST"])
def productsdetail():
        # Do some stuff
         name = request.json['name']
         email = request.json['email']
       
        #  new_result = list(collection.find({"_id": ObjectId("4ecbe7f9e8c1c9092c000027")})) 
         new_result = list(collection.find({"name":"avani"}))
         id = "6059d55b6a685246d39c6057"
         new_result=collection.find_one({'_id':bson.ObjectId(oid=id)})
         print('++',new_result)
         return jsonify({"test":"hello"})  
        #  return jsonify(customers=ourresult)  
       
    

