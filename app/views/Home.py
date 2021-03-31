from flask import Blueprint, render_template
home = Blueprint('home', __name__, template_folder='templates',   static_folder='static')


@home.route('/home')
@home.route('/')
def index():
        # Do some stuff
        return render_template('layout.html')


# @home.route('/<user_url_slug>/profile') 
@home.route('/profile') 
def timeline():
        # Do some stuff
        return render_template('home/profile.html')
       
  
@home.route('/faq')
def photos():
        # Do some stuff
        return render_template('home/faq.html')
      

         

@home.route('/aboutus')
def about():
                # Do some stuff
         return render_template('home/about.html')
