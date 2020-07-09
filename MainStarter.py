from flask import Flask,render_template,request,session,redirect,Response
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_mail import Mail
import json
import os

# Get cofig json
file=open('config.json','r')
configData=json.loads(file.read())["params"]
file.close()
# Create app object
app = Flask(__name__)
app.secret_key='super-secret-key'

# Configure for sending main
app.config.update(
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = '465',
    MAIL_USE_SSL = True,
    MAIL_USERNAME = configData['gmail-user'],
    MAIL_PASSWORD=  configData['gmail-password']
)
app.config['UPLOAD_FOLDER']=configData["upload_folder"]
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
        db.session.add(entry)
        db.session.commit()
        # mail.send_message(f'New Message from {name}',sender=email,recipients=[configData['gmail-user']],body=f'{message}\n Phone No.:{phone}')
    return render_template('contact.html',params=configData)

@app.route('/post/<string:post_slug>',methods=['GET'])
def post_route(post_slug):
    postData=posts.query.filter_by(pslug=post_slug).first()
    return render_template('post.html',params=configData,post=postData)

@app.route('/dashboard',methods=['GET','POST'])
def admin():
    if 'user' in session and session['user']==configData['admin-user']:
        post=posts.query.filter_by().all()
        return render_template('dashboard.html',params=configData,posts=post)
    else:
        if request.method=='POST':
            passw=str(request.form.get('password'))
            user=str(request.form.get('username'))
            remember=request.form.get('remember_me')
            print(remember)
            if passw==configData['admin-password'] and user==configData['admin-user']:
                session['user']=user
                post=posts.query.filter_by().all()
                return render_template('dashboard.html',params=configData,posts=post)
            else:
                return render_template('adminLogin.html')
        else:
            return render_template('adminLogin.html')
@app.route('/edit-post/<string:post_id>', methods=['POST'])
def edit(post_id):
    print("Run")
    if 'user' in session and session['user']==configData['admin-user']:
        title=request.form.get('post-title')
        stitle=request.form.get('post-stitle')
        slug=request.form.get('post-slug')
        author=request.form.get('post-author')
        image=request.form.get('post-image')
        body=request.form.get('post-body')
        post=posts.query.filter_by(pid=post_id).first()
        post.ptitle=title
        post.pslug = slug
        post.pauthor=author
        post.pimage=image
        post.pbody=body
        post.pstitle=stitle
        
        db.session.commit()
        
    return redirect('/dashboard')

@app.route('/addnewpost',methods=['POST','GET'])
def addnewpost():
    print("Start the add new")
    if request.method == "POST":
        if 'user' in session and session['user']==configData['admin-user']:
            title=request.form.get('post-title')
            stitle=request.form.get('post-stitle')
            slug=request.form.get('post-slug')
            author=request.form.get('post-author')
            image=request.form.get('post-image')
            body=request.form.get('post-body')
            tdate=datetime.now()
            new_post=posts(ptitle=title,pstitle=stitle,pslug=slug,pauthor=author,pimage=image,pbody=body,pdate=tdate)
            db.session.add(new_post)
            db.session.commit()
            return Response(status=200)
        else:
            return Response(status=201)
    else:
        return render_template('addnewpost.html',params=configData)


            
    
        
@app.route('/uploadimage',methods=['POST'])
def uploadimage():
    if 'user' in session and session['user']==configData['admin-user']:
        if request.method=='POST':
            f=request.files['image-file']
            fname=request.form.get('image-name')
            f.save(os.path.join(app.config['UPLOAD_FOLDER'],fname))
            return redirect('/addnewpost')

@app.route('/deletePost',methods=['POST'])
def deletePost():
    print("RUN")
    if 'user' in session and session['user']==configData['admin-user']:
        if request.method=='POST':
            post_id=request.form.get('post-id')
            post=posts.query.filter_by(pid=post_id).first()
            db.session.delete(post)
            db.session.commit()
            return Response(status=200)
        else :
            return Response(status=400)
    else:
        return Response(status=400)
 

app.run(debug=True)