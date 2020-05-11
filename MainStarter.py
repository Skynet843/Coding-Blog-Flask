from flask import Flask,render_template,request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_mail import Mail
import json

# Get cofig json
file=open('config.json','r')
configData=json.loads(file.read())["params"]
file.close()
# Create app object
app = Flask(__name__)

# Configure for sending main
app.config.update(
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = '465',
    MAIL_USE_SSL = True,
    MAIL_USERNAME = configData['gmail-user'],
    MAIL_PASSWORD=  configData['gmail-password']
)
mail=Mail(app)
# Create database obj
if configData["local_server"]:
    app.config['SQLALCHEMY_DATABASE_URI']=configData["local_uri"]
else:
    app.config['SQLALCHEMY_DATABASE_URI']=configData["prod_uri"]
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db=SQLAlchemy(app)

class Contacts(db.Model):
    cid=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(50),nullable=False)
    email=db.Column(db.String(50),nullable=False)
    phone=db.Column(db.String(20),nullable=False)
    message=db.Column(db.String(2000),nullable=False)
    Adate=db.Column(db.String(20),nullable=True)

class posts(db.Model):
    pid=db.Column(db.Integer,primary_key=True)
    pslug=db.Column(db.String(50),nullable=False)
    pauthor=db.Column(db.String(50),nullable=False)
    pdate=db.Column(db.String(20),nullable=False)
    ptitle=db.Column(db.String(),nullable=False)
    pstitle=db.Column(db.String(),nullable=False)
    pbody=db.Column(db.String(),nullable=True)
    pimage=db.Column(db.String(50),nullable=False)



@app.route('/')
def index():
    post=posts.query.filter_by().all()[0:configData["no-of-post"]]
    for item in post:
        print(item.pslug)
    return render_template('index.html',params=configData,posts=post)

@app.route('/about')
def about():
    return render_template('about.html',params=configData)

@app.route('/contact',methods=['GET','POST'])
def contact():
    if request.method=='POST':
        name=request.form.get('name')
        email=request.form.get('email')
        phone=request.form.get('phone')
        message=request.form.get('message')
        tdate=datetime.now()
        entry=Contacts(name=name,email=email,phone=phone,message=message,Adate=tdate)
        #setup mail
        mail.send_message(f'New Message from {name}',sender=email,recipients=[configData['gmail-user']],body=f'{message}\n Phone No.:{phone}')
        db.session.add(entry)
        db.session.commit()
    return render_template('contact.html',params=configData)

@app.route('/post/<string:post_slug>',methods=['GET'])
def post_route(post_slug):
    postData=posts.query.filter_by(pslug=post_slug).first()
    return render_template('post.html',params=configData,post=postData)

app.run(port=80,debug=True,host="192.168.0.105")