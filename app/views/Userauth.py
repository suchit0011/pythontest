from flask import Flask, Blueprint, render_template, request, jsonify, make_response 
import config
import json
import bson
from bson import json_util
from bson.objectid import ObjectId
import jwt 
import datetime 
from functools import wraps
from kanpai import Kanpai
import smtplib, ssl
import random as r
import pyotp
# from time import sleep
import time
# from datetime import date
# ------ from Email import Mail ---------
port = 587  # For starttls
smtp_server = "smtp.gmail.com"
sender_email = "cps.suchit@gmail.com"
receiver_email = ""
sender_password = "director1613"
context = ssl.create_default_context()
# ------ from Email import Mail --------


usersapp = Flask(__name__)
userauth = Blueprint('userauth', __name__, template_folder='templates',   static_folder='static')
collection = config.connect()
usersapp.config['SECRET_KEY'] = 'thisisthesecretkey'

# user registration form validation
schema = Kanpai.Object({
 "name"    : Kanpai.String().trim().required("Name is required"),
 "email" : Kanpai.Email().required(),
 "password": Kanpai.String().required("Please enter your password"),
})

# user forgot password otp compare validation
forgotschema = Kanpai.Object({
 "email" : Kanpai.Email().required("Email is required"),
 "otp" : Kanpai.String().required("OTP is required"),
 "newpassword": Kanpai.String().required("Newpassword is required"),
})

#  function for generate random number
def otpgen():
    otp=""
    for i in range(4):
        otp+=str(r.randint(1,9))
    return otp

  

# token auth request 
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        # token = request.args.get('token')
         #http://127.0.0.1:5000/route?token=alshfjfjdklsfj89549834ur
        token = request.headers.get('Token')

        if not token:
            return jsonify({'message' : 'Token is missing!'}), 403

        try: 
            print('first token',token)
            data = jwt.decode(token,'thisisthesecretkey')
            print('second token',data)
        except:
            return jsonify({'message' : 'Token is invalid!'}), 403

        return f(*args, **kwargs)

    return decorated

@userauth.route('/login', methods=["POST"])
def login():
    email = request.json['email']
    password = request.json['password']

    if email == 'ankit1@gmail.com' and password == '123456':
        token = jwt.encode({'user' : email, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(seconds=120)},'thisisthesecretkey')

        return jsonify({'status':'true','status_code':200,'message':"User logged in successfully",'token' :  token.decode('UTF-8')})

    return jsonify({'status':'false','status_code':401,'message':"Could not verify!"}) 
    # return make_response('Could not verify!', 401, {'WWW-Authenticate' : 'Basic realm="Login Required"'})   

@userauth.route('/forgotpassword', methods=["POST"])
def forgotpassword():
    email = request.json['email']
    receiver_email = email
    new_result = list(collection.find({'email': email}))
    timeout = "false"
    if new_result:
        receiveotp = otpgen()
        # redirecturl = 'https://www.civilclub.com/reset?'+receiveotp
        redirecturl = 'https://www.civilclub.com/reset?email='+email+'&otp='+receiveotp
    
    # mail sending
        with smtplib.SMTP(smtp_server, port) as server:
            server.ehlo() # Can be omitted   
            server.starttls(context=context)
            server.ehlo() # Can be omitted
            server.login(sender_email, sender_password)
            header = 'To:' + receiver_email + '\n' + 'From: ' + sender_email + '\n' + 'Subject:civil club:	Reset Password \n'
            msg = header + '\n A password reset event has been triggered. The password reset window is limited to two hours. \n\n If you do not reset your password within two hours, you will need to submit a new request. To complete the password reset process, visit the following link: \n\n '+redirecturl
            server.sendmail(sender_email, receiver_email, msg)
    # mail sending close ---------
        # save otp in database 
            date = str(datetime.datetime.now())
    
            # now =  str(datetime.datetime.now())
            # time(now.hour, now.minute, now.second)
            # datetime.combine(today, current_time)
            myquery = { "email": email }
            newvalues = { "$set": { "otp": receiveotp, "otpdate":date } }
            collection.update_one(myquery, newvalues)

        # save otp in database close
        is_user = {'status':'true','status_code':200,'message':"Email resent link sent to entered email"}   
        return jsonify(customers=is_user)
    else: 
        is_newuser = {'status':'false','status_code':200,'message':"User is not registered"}   
        return jsonify(customers=is_newuser )
 
 


   
@userauth.route('/forgotpasswordmatch', methods=["POST"])
def forgotmatch():
    validation_result = forgotschema.validate(request.json) 
    print('new password',validation_result['error']) 
    # if validation_result != "None":
    #     return jsonify("none")

    if validation_result['error'] == None:   
        email = request.json['email']
        password = request.json['newpassword']
        otp = request.json['otp']
    
        email_result = list(collection.find({'email': email}))
        date = str(datetime.datetime.now())
        print('test',email_result[0]['otp'])
        if email_result and email_result[0]['otp']:
                # --------------  logic for manage time difference
            first_time  = datetime.datetime.strptime(email_result[0]['otpdate'], '%Y-%m-%d %H:%M:%S.%f')
            later_time  = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S.%f')
            difference = later_time - first_time
            seconds_in_day = 24 * 60 * 60
            # time difference will get in minute and second
            time_difference = divmod(difference.days * seconds_in_day + difference.seconds, 60)
            get_minute_diff =  time_difference[0]
            # -------------- close logic for manage time difference
            print('date compare +++',time_difference, time_difference[0], time_difference[1])
            if get_minute_diff<120:
                myquery = { "email": email }
                newvalues = { "$set": { "password":password } }
                collection.update_one(myquery, newvalues)
                is_user = {'status':'true','status_code':200,'message':"Password has been updated please login again"}   
                return jsonify(customers=is_user)
            else:

                is_newuser = {'status':'false','status_code':200,'message':"User Token has been Expired"}   
                return jsonify(customers=is_newuser )       
                
        else: 
            is_newuser = {'status':'false','status_code':200,'message':"User Email id is not correct"}   
            return jsonify(customers=is_newuser )  
        
    else:      
        return jsonify("check")  

    # return jsonify({'message' : 'password reset successfully'})   


@userauth.route('/testing', methods=["GET"])
@token_required
def protected():
    return jsonify({'message' : 'This is only available for people with valid tokens.'})


@userauth.route('/register', methods=["POST"])
def register():
         validation_result = schema.validate(request.json)
         if validation_result['success'] == False:
          print('validation test false++',validation_result)
          return jsonify(customers="False") 
       
         else:
            print('validation test ++',validation_result['success'])
            name = request.json['name']
            email = request.json['email']
            password = request.json['password']
            new_result = list(collection.find({'email': email}))

         if new_result:
          is_user = {'status':'false','status_code':200,'message':"User is registered with this mail id"}    
          return jsonify(customers=is_user) 
       
         else:
          results  = collection.insert_one({'name': name,'email':email,'password':password}).inserted_id   
          new_result = list(collection.find({'_id': results}))
          new_user = {'ids':str(new_result[0]['_id']),'name':new_result[0]['name'],'email':new_result[0]['email']}
          token = jwt.encode({'user' : name, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(seconds=120)},'thisisthesecretkey') 
          decodeToken = token.decode('utf-8')
          is_newuser = {'status':'true','status_code':201,'message':"New user created successfully",'token': decodeToken }    
          return jsonify(customers=is_newuser) 
