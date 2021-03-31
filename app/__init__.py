from flask import Flask, render_template
from .views.Home import home
from .views.Product import product
from .views.Userauth import userauth

app = Flask(__name__)
app.register_blueprint(userauth, url_prefix='/api')
app.register_blueprint(product, url_prefix='/api')
app.register_blueprint(home)







# @app.route('/')
# def user_home():
#     return render_template('layout.html')
  

# @app.route('/profile')
# def user_profile():
#    return render_template('profile.html')   


