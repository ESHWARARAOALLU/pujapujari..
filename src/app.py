from flask import flash
import datetime
from gc import get_count
import os
from bson import ObjectId
from flask import Flask, abort, render_template, request, redirect, send_from_directory, session, jsonify, url_for
from pymongo import MongoClient
from urllib.parse import quote, unquote
from werkzeug.utils import secure_filename

# from twilio.rest import Client

app = Flask(__name__, static_folder='static')
app.secret_key = "qwerty" 

app.config['SESSION_TYPE'] = 'filesystem'
app.config['PERMANENT_SESSION_LIFETIME'] = 86400 

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif','webp'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

client = MongoClient('mongodb+srv://pujapujari:pujapujari@cluster0.atcoq0f.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
db = client['puja'] 
users= db["users"]
puja_items=db['pujaSamagri']
puja_services=db['pujaServices']
cart_item=db['cart']
s_cart=db['servicesCart']
p_list=db['panditlist']
a_pandit=db['apandit']
t_puja=db['Temples']
t_services=db['Tservices']
contactUs=db['contactus']
prasadam1=db['prasadam']
prasad1=db['prasad']
chat=db['chatBot']
banner=db['banner']
loc=db['location']

global n

n=0

@app.route('/register')
def register():
    return render_template('login.html')


@app.route('/main')
def main():
    date1=datetime.datetime.now()

    p_info=puja_items.find()
    p_info1=puja_services.find()
    info1=s_cart.find()       
    l=[]
    l1=[]
    l2=[]
    for i in p_info:
        dummy=[]
        dummy.append(i.get('_id'))
        dummy.append(i.get('name'))
        dummy.append(i.get('description'))
        dummy.append(i.get('price'))
        dummy.append(i.get('image'))
        l.append(dummy)
    for i in p_info1:
        dummy1=[]
        id=i.get('_id')
        dummy1.append(i.get('_id'))
        dummy1.append(i.get('p_name'))
        dummy1.append(i.get('description'))
        dummy1.append(i.get('price'))
        dummy1.append(i.get('image'))
        l1.append(dummy1)
    for i in info1:
         if(session['email']==i.get('email')):
              dummy=[]
              dummy.append(i.get('_id'))
              dummy.append(i.get('name'))
              dummy.append(i.get('price'))
              dummy.append(i.get('date'))
              dummy.append(i.get('time'))
              dummy.append(i.get('location'))
              dummy.append(i.get('reg_date'))
              l2.append(dummy)
    pandit=p_list.find()
    pList=[]
    for i in pandit:
        dummy2=[]
        dummy2.append(i.get('name'))
        dummy2.append(i.get('location'))
        pList.append(dummy2)
    ap=a_pandit.find()
    apandit=[]
    for i in ap:
                    dummy=[]
                    dummy.append(i.get('_id'))
                    dummy.append(i.get('name'))
                    dummy.append(i.get('age'))
                    dummy.append(i.get('location'))
                    dummy.append(i.get('contact'))
                    dummy.append(i.get('email'))
                    apandit.append(dummy)
    info2=t_services.find()
    pujaList=[]
    for i in info2:
            if(session['email']==i.get('email')):
                dummy=[]
                dummy.append(i.get('_id'))
                dummy.append(i.get('p_name'))
                dummy.append(i.get('t_name'))
                dummy.append(i.get('price'))
                dummy.append(i.get('date'))
                dummy.append(i.get('time'))
                dummy.append(i.get('status'))
                pujaList.append(dummy)
    info=cart_item.find()
    info1=s_cart.find()
    l3=[]
    l4=[]
    for i in info:
          if(session['email']==i.get('email')):
               dummy=[]
               dummy.append(i.get('_id'))
               dummy.append(i.get('name'))
               dummy.append(i.get('qty'))
               dummy.append(i.get('price'))
               dummy.append(i.get('total'))
               dummy.append(i.get('reg_date'))
               l3.append(dummy)
    for i in info1:
              if(session['email']==i.get('email')):
                dummy1=[]
                dummy1.append(i.get('_id'))
                dummy1.append(i.get('name'))
                dummy1.append(i.get('price'))
                dummy1.append(i.get('date'))
                dummy1.append(i.get('time'))
                dummy1.append(i.get('location'))
                dummy1.append(i.get('status'))
                dummy1.append(i.get('reg_date'))
                l4.append(dummy1)
    pra1=[]
    info3=prasad1.find()
    for i in info3:
          if session['email']==i.get('email'):
                dummy=[]
                dummy.append(i.get('_id'))
                dummy.append(i.get('prasadam_name'))
                dummy.append(i.get('price'))
                dummy.append(i.get('total'))
                dummy.append(i.get('qty'))
                dummy.append(i.get('date'))
                pra1.append(dummy)

    selected_banner=session.get('selected_banner')
    selected_location=session.get('selected_loc')
    email=session.get('selected_mail')
    num=session.get('selected_num')
    email=session.get('selected_mail')
    address=session.get('selected_address')
        
    n=len(l3)+len(l4)+len(pujaList)+len(pra1)   
    return render_template('main.html',l=l,l1=l1,l2=l2,pList=pList,n=n,date1=date1,selected_banner=selected_banner,apandit=apandit,selected_location=selected_location,email=email,num=num,address=address)

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/adminlogin')
def adminlogin():
    return render_template('adminlogin.html')

@app.route('/forgot')
def forg():
    return render_template("forgot.html")

@app.route('/plogin')
def plogin():
    return render_template("plogin.html")

@app.route('/acceptpuja')
def acceptpuja():
     pujas=s_cart.find()
     request=[]
     accepted=[]
     deny=[]
     for i in pujas:
          if i.get('status')=="pending":
               dummy=[]
               dummy.append(i.get('_id'))
               dummy.append(i.get('pmail'))
               dummy.append(i.get('name'))
               dummy.append(i.get('price'))
               dummy.append(i.get('date'))
               dummy.append(i.get('pname'))
               dummy.append(i.get('pnumber'))
               dummy.append(i.get('time'))
               dummy.append(i.get('location'))
               dummy.append(i.get('status'))
               dummy.append(i.get('email'))
               request.append(dummy)

     
          if i.get('status')=="Accepted":
               
               dummy1=[]
               dummy1.append(i.get('_id'))
               dummy1.append(i.get('pmail'))
               dummy1.append(i.get('name'))
               dummy1.append(i.get('price'))
               dummy1.append(i.get('date'))
               dummy1.append(i.get('pname'))
               dummy1.append(i.get('pnumber'))
               dummy1.append(i.get('time'))
               dummy1.append(i.get('location'))
               dummy1.append(i.get('status'))
               dummy1.append(i.get('email'))
               accepted.append(dummy1)

          if i.get('status')=="Rejected":
               dummy2=[]
               dummy2.append(i.get('_id'))
               dummy2.append(i.get('pmail'))
               dummy2.append(i.get('name'))
               dummy2.append(i.get('price'))
               dummy2.append(i.get('date'))
               dummy2.append(i.get('pname'))
               dummy2.append(i.get('pnumber'))
               dummy2.append(i.get('time'))
               dummy2.append(i.get('location'))
               dummy2.append(i.get('status'))
               dummy2.append(i.get('email'))
               deny.append(dummy2)  
          selected_location=session.get('selected_loc')
          email=session.get('selected_mail')
          num=session.get('selected_num')
          email=session.get('selected_mail')
          address=session.get('selected_address')  
     return render_template("acceptpuja.html",request=request,accepted=accepted,deny=deny,selected_location=selected_location,num=num,address=address,email=email)
   
@app.route('/pandit')
def pandit():
     pujas=s_cart.find()
     request1=[]
     accepted=[]
     deny=[]
     for i in pujas:
          if i.get('pmail')==session['email1']:
            if i.get('status')=="pending":
                dummy=[]
                dummy.append(i.get('_id'))
                dummy.append(i.get('pmail'))
                dummy.append(i.get('name'))
                dummy.append(i.get('price'))
                dummy.append(i.get('date'))
                dummy.append(i.get('pname'))
                dummy.append(i.get('pnumber'))
                dummy.append(i.get('time'))
                dummy.append(i.get('location'))
                dummy.append(i.get('status'))
                dummy.append(i.get('email'))
                request1.append(dummy)
        
            if i.get('status')=="Accepted":
                
                dummy1=[]
                dummy1.append(i.get('_id'))
                dummy1.append(i.get('pmail'))
                dummy1.append(i.get('name'))
                dummy1.append(i.get('price'))
                dummy1.append(i.get('date'))
                dummy1.append(i.get('pname'))
                dummy1.append(i.get('pnumber'))
                dummy1.append(i.get('time'))
                dummy1.append(i.get('location'))
                dummy1.append(i.get('status'))
                dummy1.append(i.get('email'))
                accepted.append(dummy1)

            if i.get('status')=="Rejected":
                dummy2=[]
                dummy2.append(i.get('_id'))
                dummy2.append(i.get('pmail'))
                dummy2.append(i.get('name'))
                dummy2.append(i.get('price'))
                dummy2.append(i.get('date'))
                dummy2.append(i.get('pname'))
                dummy2.append(i.get('pnumber'))
                dummy2.append(i.get('time'))
                dummy2.append(i.get('location'))
                dummy2.append(i.get('status'))
                dummy2.append(i.get('email'))
                deny.append(dummy2)
     info = p_list.find_one({'email':session['email1']})
     id=info['_id']
     name=info['name']
    #  email=info['email']
     phno=info['phno']
     location=info['location']   
     selected_location=session.get('selected_loc')
     email=session.get('selected_mail')
     num=session.get('selected_num')
     email=session.get('selected_mail')
     address=session.get('selected_address')                    
     return render_template('pandit.html',id=id,name=name,phno=phno,location=location,accepted=accepted,deny=deny,request1=request1,selected_location=selected_location,num=num,address=address,email=email)

     

@app.route('/checkout')
def checkout():
    info=cart_item.find()
    info1=s_cart.find()
    # shipping=int(25)
    l=[]
    l1=[]
    for i in info:
        if(session['email']==i.get('email')):
            dummy=[]
            dummy.append(i.get('_id'))
            dummy.append(i.get('name'))
            dummy.append(i.get('qty'))
            dummy.append(int(i.get('price')))
            # samagriTotal=samagriTotal+int(i.get('total'))
            dummy.append(i.get('total'))
            dummy.append(i.get('reg_date'))
            l.append(dummy)
    for i in info1:
        if(session['email']==i.get('email')):
            dummy1=[]
            dummy1.append(i.get('_id'))
            dummy1.append(i.get('name'))
            dummy1.append(i.get('price'))
            # serviceTotal=int(i.get('price'))
            dummy1.append(i.get('date'))
            dummy1.append(i.get('time'))
            dummy1.append(i.get('location'))
            dummy1.append(i.get('status'))
            dummy1.append(i.get('reg_date'))
            l1.append(dummy1)
    pList=[]
    pandit=p_list.find()
    for i in pandit:
        dummy2=[]
        dummy2.append(i.get('name'))
        dummy2.append(i.get('location'))
        pList.append(dummy2)
    info2=t_services.find()
    pujaList=[]
    for i in info2:
         if(session['email']==i.get('email')):
              dummy=[]
              dummy.append(i.get('_id'))
              dummy.append(i.get('p_name'))
              dummy.append(i.get('t_name'))
              dummy.append(i.get('price'))
            #   pujaTotal=int(i.get('price'))
              dummy.append(i.get('date'))
              dummy.append(i.get('time'))
              dummy.append(i.get('status'))
              pujaList.append(dummy)
    pra1=[]
    info3=prasad1.find()
    for i in info3:
          if session['email']==i.get('email'):
                dummy=[]
                dummy.append(i.get('_id'))
                dummy.append(i.get('prasadam_name'))
                dummy.append(i.get('price'))
                dummy.append(i.get('total'))
                # prasadamTotal=prasadamTotal+i.get('total')
                dummy.append(i.get('qty'))
                dummy.append(i.get('date'))
                pra1.append(dummy)
    n=len(l)+len(l1)+len(pujaList) + len(pra1)
    return render_template('checkout.html',n=n)

@app.route('/404')
def error_404():
    return render_template('404.html')

@app.route('/tlogin')
def tlogin():
     return render_template('tlogin.html')

@app.route('/testimonial')
def testimonial():
    return render_template('testimonial.html')

@app.route('/')
def index1():
    p_info = puja_items.find()
    p_info1 = puja_services.find()
    l = []
    l1 = []
    for i in p_info:
        dummy = []  
        dummy.append(i.get('_id'))
        dummy.append(i.get('name'))
        dummy.append(i.get('description'))
        dummy.append(i.get('price'))
        dummy.append(i.get('image'))
        l.append(dummy)
    for i in p_info1:
        dummy1 = []
        dummy1.append(i.get('_id'))
        dummy1.append(i.get('p_name'))
        dummy1.append(i.get('description'))
        dummy1.append(i.get('price'))
        dummy1.append(i.get('image'))
        l1.append(dummy1)
    selected_banner=session.get('selected_banner')
    selected_location=session.get('selected_loc')
    email=session.get('selected_mail')
    num=session.get('selected_num')
    email=session.get('selected_mail')
    address=session.get('selected_address')
    return render_template('index.html', l=l, l1=l1,selected_banner=selected_banner,selected_location=selected_location,num=num,address=address,email=email)


def is_valid_password(psw):
    if len(psw) < 8:
        return False
    if not any(char.isdigit() for char in psw):
        return False
    if not any(char.isupper() for char in psw):
        return False
    if not any(char.islower() for char in psw):
        return False
    if not any(char in '!@#$%^&*()_-+=[]{}|;:,.<>?/' for char in psw):
        return False
    return True

@app.route('/reg', methods=['POST', 'GET'])
def reg():
    name = request.form['name']
    email = request.form['email']
    pwd = request.form['pwd']
    phno = request.form['phno']
    address=request.form['address']
    if not isinstance(name, str) or not any(c.isalpha() for c in name):
            msg1 = 'Invalid name format. Please enter a valid name.'
            return render_template('login.html', msg1=msg1)
    existing_user = users.find_one({'email': email})
    existing_num = users.find_one({'phno': phno})
    if existing_user:
            msg1='Email already exists'
            return render_template('login.html',msg1=msg1)
    if existing_num:
            msg1='Phone Number Already Exists'
            return render_template('login.html',msg1=msg1)
    if not is_valid_password(pwd):
            msg1 = 'Password must be Valid.'

            return render_template('login.html', msg1=msg1)
    reg_date = datetime.datetime.now()
    address_list = [{"address": address, "status": "Not Saved"}]

    user_data = {
        'name': name,
        'email': email,
        'psw': pwd,
        'phno': phno,
        'address': address_list,
        'reg_date': reg_date,
        'status': "Not Saved"
    }

    users.insert_one(user_data)
    msg1='Registration successful'
    # account_sid = 'AC4da61e8f74035eabee3b23f2d68dc2d3'
    # auth_token = '7d4264c8df08ac640d854db91d08f2bd'
    # client = Client(account_sid, auth_token)
    # message = client.messages.create(
    #     body='Your Registration for Puja Pujari is Successful',
    #     from_='+12513135289',
    #     to='+91 9392419102'
    # )
    return render_template('login.html',msg1=msg1)

@app.route('/log', methods=['POST'])
def login_post():
    global e_mail
    global type1
    prasadamTotal=0
    email = request.form['email']
    pwd = request.form['pwd']
    user = users.find_one({'email': email})
    
    pujaList = []  # Initialize pujaList here
    
    if user:
        if user.get('email') == email:
            if user.get('psw') == pwd:
                session['email'] = email
                date1=datetime.datetime.now()
                msg1 = 'Login Successful'
                session.permanent = True 

                p_info = puja_items.find()
                p_info1 = puja_services.find()
                l = []
                l1 = []
                for i in p_info:
                    dummy = []
                    dummy.append(i.get('_id'))
                    dummy.append(i.get('name'))
                    dummy.append(i.get('description')) 
                    dummy.append(i.get('price'))
                    dummy.append(i.get('image'))
                    l.append(dummy)
                for j in p_info1:
                    dummy1 = []
                    dummy1.append(j.get('_id'))
                    dummy1.append(j.get('p_name'))
                    dummy1.append(j.get('description'))
                    dummy1.append(j.get('price'))
                    dummy1.append(j.get('image'))
                    l1.append(dummy1)
                
                pandit = p_list.find()
                pList = []
                for k in pandit:
                    dummy2 = []
                    dummy2.append(k.get('name'))
                    dummy2.append(k.get('location'))
                    pList.append(dummy2)
                ap=a_pandit.find()
                apandit=[]
                for i in ap:
                    dummy=[]
                    dummy.append(i.get('_id'))
                    dummy.append(i.get('name'))
                    dummy.append(i.get('age'))
                    dummy.append(i.get('location'))
                    dummy.append(i.get('contact'))
                    dummy.append(i.get('email'))
                    apandit.append(dummy)
                
                info = cart_item.find()
                info1 = s_cart.find()
                l3 = []
                l4 = []
                for i in info:
                    if session['email'] == i.get('email'):
                        dummy = []
                        dummy.append(i.get('_id'))
                        dummy.append(i.get('name'))
                        dummy.append(i.get('qty'))
                        dummy.append(i.get('price'))
                        dummy.append(i.get('total'))
                        dummy.append(i.get('reg_date'))
                        l3.append(dummy)
                for i in info1:
                    if session['email'] == i.get('email'):
                        dummy1 = []
                        dummy1.append(i.get('_id'))
                        dummy1.append(i.get('name'))
                        dummy1.append(i.get('price'))
                        dummy1.append(i.get('date'))
                        dummy1.append(i.get('time'))
                        dummy1.append(i.get('location'))
                        dummy1.append(i.get('status'))
                        dummy1.append(i.get('reg_date'))
                        l4.append(dummy1)
                
                
                info2 = t_services.find()
                for i in info2:
                    if session['email'] == i.get('email'):
                        dummy = []
                        dummy.append(i.get('_id'))
                        dummy.append(i.get('p_name'))
                        dummy.append(i.get('t_name'))
                        dummy.append(i.get('price'))
                        dummy.append(i.get('date'))
                        dummy.append(i.get('time'))
                        dummy.append(i.get('status'))
                        pujaList.append(dummy)
                
                pra1=[]
                info3=prasad1.find()
                for i in info3:
                    if session['email']==i.get('email'):
                            dummy=[]
                            dummy.append(i.get('_id'))
                            dummy.append(i.get('prasadam_name'))
                            dummy.append(i.get('price'))
                            dummy.append(i.get('total'))
                            prasadamTotal=prasadamTotal+i.get('total')
                            dummy.append(i.get('qty'))
                            dummy.append(i.get('date'))
                            pra1.append(dummy)
                selected_banner=session.get('selected_banner')
                selected_location=session.get('selected_loc')
                email=session.get('selected_mail')
                num=session.get('selected_num')
                email=session.get('selected_mail')
                address=session.get('selected_address')
                
                n = len(l3) + len(l4) + len(pujaList) + len(pra1)
                print("Login Successful")
                return render_template('main.html', user=user, msg1=msg1, l=l, l1=l1, pList=pList, n=n,date1=date1,apandit=apandit,selected_banner=selected_banner,selected_location=selected_location,num=num,address=address,email=email)
            else:
                return render_template("login.html", msg="Password Wrong")
        else:
            msg = 'Invalid email or password. Please try again.'
            return render_template('login.html', msg=msg)
    else:      
        return render_template("login.html", msg="Please Register")
    
@app.route('/alog', methods=['POST','GET'])
def alogin_post():
    email = request.form['email']
    pwd = request.form['pwd']
    

    
    if email == "a@gmail.com":
            if pwd == "admin":
                info=puja_items.find()
                l=[]
                for i in info:
                    dummy=[]
                    dummy.append(i.get('_id'))
                    dummy.append(i.get('name'))
                    dummy.append(i.get('price'))
                    dummy.append(i.get('description'))
                    dummy.append(i.get('image'))
                    l.append(dummy)
                user_details =users.find()
                user=[]
                for j in user_details:
                    dummy=[]
                    dummy.append(j.get('_id'))
                    dummy.append(j.get('name'))
                    dummy.append(j.get('email'))
                    dummy.append(j.get('phno'))
                    user.append(dummy)
                p_details=p_list.find()
                pandit=[]
                for k in p_details:
                    dummy=[]
                    dummy.append(k.get('_id'))
                    dummy.append(k.get('name'))
                    dummy.append(k.get('age'))
                    dummy.append(k.get('location'))
                    dummy.append(k.get('phno'))
                    dummy.append(k.get('email'))
                    pandit.append(dummy)
                ap=a_pandit.find()
                apandit=[]
                for i in ap:
                    dummy=[]
                    dummy.append(i.get('_id'))
                    dummy.append(i.get('name'))
                    dummy.append(i.get('age'))
                    dummy.append(i.get('location'))
                    dummy.append(i.get('contact'))
                    dummy.append(i.get('email'))
                    apandit.append(dummy)
                k=[]
                puja_service=puja_services.find()
                for r in puja_service:
                    dummy=[]
                    dummy.append(r.get('_id'))
                    dummy.append(r.get('p_name'))
                    dummy.append(r.get('description'))
                    dummy.append(r.get('price'))
                    dummy.append(i.get('image'))
                    
                    
                    k.append(dummy)  
                info1 = t_puja.find()
                # info1 = t_puja.find()
                temples = []
                for i in info1:
                    temple_name = i.get('temple_name')
                    pujas = i.get('pujas', [])

                    for puja in pujas:
                        temple_data = {
                            '_id': i.get('_id'),
                            't_name': temple_name,
                            'p_name': puja.get('puja_name'),
                            'location': puja.get('location'),
                            'price': puja.get('price'),
                            'description': puja.get('description')
                        }
                        temples.append(temple_data)
                prasad1=prasadam1.find()
                prasad=[]
                for i in prasad1:
                    mandir_name=i.get('mandir_name')
                    
                    prasadam_items=i.get('prasadam_items',[])
                    for j in prasadam_items:
                        pdata={
                             '_id':i.get('_id'),
                             'mandir_name':mandir_name,
                             'prasadam_name':j.get('prasadam_name'),
                             'price':j.get('price'),
                             'description':j.get('description')
                        }
                        prasad.append(pdata)
                ban1=[]
                ban=banner.find()
                for i in ban:
                    ban1.append(i.get('banner'))
                loc_names=[]
                l_name=loc.find()
                for i in l_name:
                    dummy=[]
                    dummy.append(i.get('_id'))
                    dummy.append(i.get('location'))
                    dummy.append(i.get('name'))
                    dummy.append(i.get('mail'))
                    dummy.append(i.get('location'))
                    loc_names.append(dummy) 
                selected_location=session.get('selected_loc')
                email=session.get('selected_mail')
                num=session.get('selected_num')
                email=session.get('selected_mail')
                address=session.get('selected_address')
                return render_template('admin.html',l=l,user=user,pandit=pandit,k=k,temples=temples,apandit=apandit,prasad=prasad,ban1=ban1,loc_names=loc_names,selected_location=selected_location,num=num,email=email,address=address)
            else:
                return render_template("adminlogin.html", msg="Password Wrong")
    else:
            msg = 'Invalid email or password. Please try again.'
            return render_template('adminlogin.html', msg=msg)
  
    
@app.route('/forgotpassword',methods=['POST','GET'])
def forgot():
    email=request.form['email']
    npwd=request.form['pwd']
    info=users.find_one({'email':email})
    if info:
            users.update_one({'email': email}, {'$set': {'psw': npwd}})
            return render_template('login.html') 
    return render_template("forgot.html",msg="Mail Not Found")

@app.route('/logout')
def logout():
    session.pop('email', None)
    p_info=puja_items.find()
    p_info1=puja_services.find()
    l=[]
    l1=[]
    for i in p_info:
        dummy=[]
        dummy.append(i.get('_id'))
        dummy.append(i.get('name'))
        dummy.append(i.get('description'))
        dummy.append(i.get('price'))
        dummy.append(i.get('image'))
        l.append(dummy)
    for i in p_info1:
        dummy1=[]
        dummy.append(i.get('_id'))
        dummy1.append(i.get('p_name'))
        dummy1.append(i.get('description'))
        dummy1.append(i.get('price'))
        dummy1.append(i.get('image'))
        l1.append(dummy1)
    return render_template('index.html',l=l,l1=l1)

@app.route('/preg', methods=['POST', 'GET'])
def preg():
    name = request.form['name']
    email = request.form['email']
    pwd = request.form['pwd']
    phno = request.form['phno']
    age = request.form['age']
    location = request.form['location']
    if not isinstance(name, str) or not any(c.isalpha() for c in name):
        msg1 = 'Invalid name format. Please enter a valid name.'
        return render_template('login.html', msg1=msg1)
    existing_user = p_list.find_one({'email': email})
    existing_num =p_list.find_one({'phno': phno})
    if existing_user:
        msg1='Email already exists'
        return render_template('plogin.html',msg1=msg1)
    if existing_num:
        msg1='Phone Number Already Exists'
        return render_template('plogin.html',msg1=msg1)
    if not is_valid_password(pwd):
        msg1 = 'Password must be at least 8 characters long and contain at least one uppercase letter, one lowercase letter, one digit, and one special character.'
        return render_template('plogin.html', msg1=msg1)
    reg_date = datetime.datetime.now()
    user_data = {
            'name': name,
            'email': email,
            'pwd': pwd,
            'phno':phno,
            'age':age,
            'location':location,
            'reg_date': reg_date  
        }
    p_list.insert_one(user_data)
    # account_sid = 'AC4da61e8f74035eabee3b23f2d68dc2d3'
    # auth_token = '7d4264c8df08ac640d854db91d08f2bd'
    # client = Client(account_sid, auth_token)
    # message = client.messages.create(
    #     body='Your registration for pandit was Successful!',
    #     from_='+12513135289',
    #     to='+91 9392419102'
    # )
    msg1='Registration successful'
    return render_template('plogin.html',msg1=msg1)


@app.route('/plog', methods=['POST','GET'])
def plogin_post():
        email1 = request.form['email']
        pwd = request.form['pwd']
        user = p_list.find_one({'email': email1})
        request1=[]
        accepted=[]
        deny=[]
        if user:
            if user.get('email')==email1:
                if user.get('pwd')==pwd:
                    session['email1']=email1
                    msg1='Login Successful'
                    # account_sid = ''
                    # auth_token = '7d4264c8df08ac640d854db91d08f2bd'
                    # client = Client(account_sid, auth_token)
                    # message = client.messages.create(
                    #     body='Pandit LoginWas Successful',
                    #     from_='+12513135289',
                    #     to='+91 93924 19102'
                    # )
                    pujas=s_cart.find()
     
                    for i in pujas:
                        if i.get('status')=="pending" and i.get('pmail')==email1:
                            dummy=[]
                            dummy.append(i.get('_id'))
                            dummy.append(i.get('pmail'))
                            dummy.append(i.get('name'))
                            dummy.append(i.get('price'))
                            dummy.append(i.get('date'))
                            dummy.append(i.get('pname'))
                            dummy.append(i.get('pnumber'))
                            dummy.append(i.get('time'))
                            dummy.append(i.get('location'))
                            dummy.append(i.get('status'))
                            dummy.append(i.get('email'))
                            request1.append(dummy)
                    
                        if i.get('status')=="Accepted" and i.get('pmail')==email1:
                            
                            dummy1=[]
                            dummy1.append(i.get('_id'))
                            dummy1.append(i.get('pmail'))
                            dummy1.append(i.get('name'))
                            dummy1.append(i.get('price'))
                            dummy1.append(i.get('date'))
                            dummy1.append(i.get('pname'))
                            dummy1.append(i.get('pnumber'))
                            dummy1.append(i.get('time'))
                            dummy1.append(i.get('location'))
                            dummy1.append(i.get('status'))
                            dummy1.append(i.get('email'))
                            accepted.append(dummy1)

                        if i.get('status')=="Rejected" and i.get('pmail')==email1:
                            dummy2=[]
                            dummy2.append(i.get('_id'))
                            dummy2.append(i.get('pmail'))
                            dummy2.append(i.get('name'))
                            dummy2.append(i.get('price'))
                            dummy2.append(i.get('date'))
                            dummy2.append(i.get('pname'))
                            dummy2.append(i.get('pnumber'))
                            dummy2.append(i.get('time'))
                            dummy2.append(i.get('location'))
                            dummy2.append(i.get('status'))
                            dummy2.append(i.get('email'))
                            deny.append(dummy2)
                    info = p_list.find_one({'email':session['email1']})
                    id=info['_id']
                    name=info['name']
                    phno=info['phno']
                    location=info['location']
                    selected_location=session.get('selected_loc')
                    email=session.get('selected_mail')
                    num=session.get('selected_num')
                    email=session.get('selected_mail')
                    address=session.get('selected_address')
                    return render_template('pandit.html', user=user,msg1=msg1,request1=request1,accepted=accepted,deny=deny,name=name,location=location,phno=phno,id=id,selected_location=selected_location,num=num,address=address,email=email)
                else:
                    return render_template("plogin.html",msg="Password Wrong")
            else:
                msg = 'Invalid email or password. Please try again.'
                return render_template('plogin.html', msg=msg)
        else:      
            return render_template("plogin.html",msg="Please Register")
        
@app.route('/p_update/<id>',methods=['POST','GET'])
def p_update(id):
     info = s_cart.find_one({'_id': ObjectId(id)})
     id=info['_id']
     if info:
          s_cart.update_one(
            {'_id': id},
            {'$set': {'status': "Accepted"}}
        )
        #   account_sid = 'AC4da61e8f74035eabee3b23f2d68dc2d3'
        #   auth_token = '7d4264c8df08ac640d854db91d08f2bd'
        #   client = Client(account_sid, auth_token)
        #   message = client.messages.create(
        #     body='Pandit Accepted Your request!!',
        #     from_='+12513135289',
        #     to='+91 9392419102'
        # )
     pujas=s_cart.find()
     request1=[]
     accepted=[]
     deny=[]
     
     for i in pujas:
                        
                        if i.get('status')=="pending" and i.get('pmail')==session['email1']:
                            dummy=[]
                            dummy.append(i.get('_id'))
                            dummy.append(i.get('pmail'))
                            dummy.append(i.get('name'))
                            dummy.append(i.get('price'))
                            dummy.append(i.get('date'))
                            dummy.append(i.get('pname'))
                            dummy.append(i.get('pnumber'))
                            dummy.append(i.get('time'))
                            dummy.append(i.get('location'))
                            dummy.append(i.get('status'))
                            dummy.append(i.get('email'))
                            request1.append(dummy)
                    
                        if i.get('status')=="Accepted" and i.get('pmail')==session['email1']:
                            
                            dummy1=[]
                            dummy1.append(i.get('_id'))
                            dummy1.append(i.get('pmail'))
                            dummy1.append(i.get('name'))
                            dummy1.append(i.get('price'))
                            dummy1.append(i.get('date'))
                            dummy1.append(i.get('pname'))
                            dummy1.append(i.get('pnumber'))
                            dummy1.append(i.get('time'))
                            dummy1.append(i.get('location'))
                            dummy1.append(i.get('status'))
                            dummy1.append(i.get('email'))
                            accepted.append(dummy1)

                        if i.get('status')=="Rejected" and i.get('pmail')==session['email1']:
                            dummy2=[]
                            dummy2.append(i.get('_id'))
                            dummy2.append(i.get('pmail'))
                            dummy2.append(i.get('name'))
                            dummy2.append(i.get('price'))
                            dummy2.append(i.get('date'))
                            dummy2.append(i.get('pname'))
                            dummy2.append(i.get('pnumber'))
                            dummy2.append(i.get('time'))
                            dummy2.append(i.get('location'))
                            dummy2.append(i.get('status'))
                            dummy2.append(i.get('email'))
                            deny.append(dummy2)
     return redirect(url_for('pandit'))


@app.route('/p_deny/<id>',methods=['POST','GET'])
def p_deny(id):
     info = s_cart.find_one({'_id': ObjectId(id)})
     id=info['_id']
     if info:
          s_cart.update_one(
            {'_id': id},
            {'$set': {'status': "Rejected"}}
        )
        #   account_sid = 'AC4da61e8f74035eabee3b23f2d68dc2d3'
        #   auth_token = '7d4264c8df08ac640d854db91d08f2bd'
        #   client = Client(account_sid, auth_token)
        #   message = client.messages.create(
        #     body='Pandit Denied your Request',
        #     from_='+12513135289',
        #     to='+91 9392419102'
        # )
     pujas=s_cart.find()
     request1=[]
     accepted=[]
     deny=[]
     
     for i in pujas:
                        if i.get('status')=="pending" and i.get('pmail')==session['email1']:
                            dummy=[]
                            dummy.append(i.get('_id'))
                            dummy.append(i.get('pmail'))
                            dummy.append(i.get('name'))
                            dummy.append(i.get('price'))
                            dummy.append(i.get('date'))
                            dummy.append(i.get('pname'))
                            dummy.append(i.get('pnumber'))
                            dummy.append(i.get('time'))
                            dummy.append(i.get('location'))
                            dummy.append(i.get('status'))
                            dummy.append(i.get('email'))
                            request1.append(dummy)
                    
                        if i.get('status')=="Accepted" and i.get('pmail')==session['email1']:
                            
                            dummy1=[]
                            dummy1.append(i.get('_id'))
                            dummy1.append(i.get('pmail'))
                            dummy1.append(i.get('name'))
                            dummy1.append(i.get('price'))
                            dummy1.append(i.get('date'))
                            dummy1.append(i.get('pname'))
                            dummy1.append(i.get('pnumber'))
                            dummy1.append(i.get('time'))
                            dummy1.append(i.get('location'))
                            dummy1.append(i.get('status'))
                            dummy1.append(i.get('email'))
                            accepted.append(dummy1)


                        if i.get('status')=="Rejected" and i.get('pmail')==session['email1']:
                            dummy2=[]
                            dummy2.append(i.get('_id'))
                            dummy2.append(i.get('pmail'))
                            dummy2.append(i.get('name'))
                            dummy2.append(i.get('price'))
                            dummy2.append(i.get('date'))
                            dummy2.append(i.get('pname'))
                            dummy2.append(i.get('pnumber'))
                            dummy2.append(i.get('time'))
                            dummy2.append(i.get('location'))
                            dummy2.append(i.get('status'))
                            dummy2.append(i.get('email'))
                            deny.append(dummy2)
     return redirect(url_for('pandit'))

@app.route('/add_to_cart/<id>', methods=['POST', 'GET'])
def add_to_cart(id):
    info = puja_items.find_one({'_id': ObjectId(id)})
    if info:
        qty = 1
        name = info.get('name')
        price = info.get('price')
        total = price * qty 
        existing_item = cart_item.find_one({'email': session['email'], 'name': name})
        if existing_item:
            msg = "Item Already present in the Cart"
            new_qty = existing_item.get('qty') + qty
            new_total = new_qty * price
            cart_item.update_one(
                {'_id': existing_item['_id']},
                {'$set': {'qty': new_qty, 'total': new_total}}
            )
        else:
            date = str(datetime.datetime.today()).split()[0]
            msg = "Item Added to cart"
            items = {
                'email': session['email'],
                'name': name,
                'price': price,
                'qty': qty,
                'total': total,
                'reg_date': date,
                'status': "pending"
            }
            cart_item.insert_one(items)
            # account_sid = 'AC4da61e8f74035eabee3b23f2d68dc2d3'
            # auth_token = '7d4264c8df08ac640d854db91d08f2bd'
            # client = Client(account_sid, auth_token)
            # message = client.messages.create(
            # body='Item Added to Cart Successfully!!!',
            # from_='+12513135289',
            # to='+91 9392419102'
            # )
    else:
        msg = "Item not found"
    return redirect(url_for('main', msg=msg))

@app.route('/cart')
def cart():
    samagriTotal=0
    overallTotalS=0
    overallTotal=0
    serviceTotal=0
    pujaTotal=0
    prasadamTotal=0
    info=cart_item.find()
    info1=s_cart.find()
    shipping=int(25)
    l=[]
    l1=[]
    for i in info:
        if(session['email']==i.get('email')):
            dummy=[]
            dummy.append(i.get('_id'))
            dummy.append(i.get('name'))
            dummy.append(i.get('qty'))
            dummy.append(int(i.get('price')))
            samagriTotal=samagriTotal+int(i.get('total'))
            dummy.append(i.get('total'))
            dummy.append(i.get('reg_date'))
            l.append(dummy)
    for i in info1:
        if(session['email']==i.get('email')):
            dummy1=[]
            dummy1.append(i.get('_id'))
            dummy1.append(i.get('name'))
            dummy1.append(i.get('price'))
            serviceTotal=serviceTotal+int(i.get('price'))
            dummy1.append(i.get('date'))
            dummy1.append(i.get('time'))
            dummy1.append(i.get('location'))
            dummy1.append(i.get('pname'))
            dummy1.append(i.get('pnumber'))
            dummy1.append(i.get('status'))
            dummy1.append(i.get('reg_date'))
            l1.append(dummy1)
    pList=[]
    pandit=p_list.find()
    for i in pandit:
        dummy2=[]
        dummy2.append(i.get('name'))
        dummy2.append(i.get('location'))
        pList.append(dummy2)
    info2=t_services.find()
    pujaList=[]
    for i in info2:
         if(session['email']==i.get('email')):
              dummy=[]
              dummy.append(i.get('_id'))
              dummy.append(i.get('p_name'))
              dummy.append(i.get('t_name'))
              dummy.append(i.get('price'))
              pujaTotal=pujaTotal+int(i.get('price'))
              dummy.append(i.get('date'))
              dummy.append(i.get('time'))
              dummy.append(i.get('status'))
              pujaList.append(dummy)
    pra1=[]
    info3=prasad1.find()
    for i in info3:
          if session['email']==i.get('email'):
                dummy=[]
                dummy.append(i.get('_id'))
                dummy.append(i.get('prasadam_name'))
                dummy.append(i.get('price'))
                dummy.append(i.get('total'))
                prasadamTotal=prasadamTotal+int(i.get('total'))
                
                dummy.append(i.get('qty'))
                dummy.append(i.get('date'))
                pra1.append(dummy)
    n=len(l)+len(l1)+len(pujaList) + len(pra1)
    overallTotal=samagriTotal+serviceTotal+pujaTotal+prasadamTotal
    overallTotalS=overallTotal+shipping
    selected_location=session.get('selected_loc')
    email=session.get('selected_mail')
    num=session.get('selected_num')
    email=session.get('selected_mail')
    address=session.get('selected_address')   
    return render_template("cart.html",l=l,l1=l1,pList=pList,pujaList=pujaList,n=n,overallTotal=overallTotal,overallTotalS=overallTotalS,shipping=shipping,pra1=pra1,selected_location=selected_location,num=num,address=address,email=email)

@app.route('/increase_quantity/<id>', methods=['POST'])
def increase_quantity(id):
    item = cart_item.find_one({'_id': ObjectId(id)})
    if item and item['qty'] >= 1:
        cart_item.update_one({'_id': ObjectId(id)}, {'$inc': {'qty': 1}})
        price = int(float(item['price']))
        n_total = (item['qty'] + 1) * price
        cart_item.update_one({'_id': ObjectId(id)}, {'$set': {'total': n_total}})
    else:
        abort(400, 'Quantity must be greater than or equal to one')
    return redirect(url_for('cart'))

@app.route('/decrease_quantity/<item_id>', methods=['POST'])
def decrease_quantity(item_id):
    item = cart_item.find_one({'_id': ObjectId(item_id)})
    if item:
        if item['qty'] > 1:
            cart_item.update_one({'_id': ObjectId(item_id)}, {'$inc': {'qty': -1}}, upsert=False)
            n_total = item['qty'] * float(item['price']) - float(item['price'])  # Convert price to float
            cart_item.update_one({'_id': ObjectId(item_id)}, {'$set': {'total': n_total}})
        else:
            cart_item.delete_one({'_id': ObjectId(item_id)})
    else:
        msg = "Quantity must be greater than or equal to one"  
    return redirect(url_for('cart'))

@app.route('/delete/<id>', methods=['POST', 'GET'])
def delete(id):
    uid = cart_item.find_one({'_id': ObjectId(id)})
    if uid:
        cart_item.delete_one({'_id': uid['_id']})     
    return redirect(url_for('cart'))

@app.route('/addservices/<id>', methods=['POST', 'GET'])
def addservice(id):
    pandit_email = None
    pname=None
    pnumber=None 

    if request.method == 'POST':
        # Get form data
        date = request.form['date']
        time=request.form['time']
        location = request.form['location']
        
        # Check if both date and location are selected
        if not (date and location):
            flash('Please select all options before adding to cart', 'error')
            return redirect(url_for('cart'))

        # Split location to get name and loc
        name, loc = location.split('-')

        pandit_data = p_list.find_one({'name': name, 'location': loc})
        if pandit_data:
            pandit_email = pandit_data.get('email')
            pname=pandit_data.get('name')
            pnumber=pandit_data.get('phno')
        else:
            pandit_data = a_pandit.find_one({'name': name, 'location': loc})
            pandit_email = pandit_data.get('email')
            pname=pandit_data.get('name')
            pnumber=pandit_data.get('contact')

        uid = puja_services.find_one({'_id': ObjectId(id)})
        if uid:
            # Create service dictionary
            services = {
                'email': session['email'],
                'name': uid.get('p_name'),
                'price': uid.get('price'),
                'date': date,
                'location': loc,
                'pname':pname,
                'pmail': pandit_email,
                'pnumber':pnumber,
                'time':time,
                'status': "pending"
            }
            # Insert service into cart
            s_cart.insert_one(services)     
            flash('Service added to cart successfully', 'success')

    return redirect(url_for('cart'))

@app.route('/deleteservice/<id>',methods=['POST','GET'])
def deleteService(id):
     uid1=s_cart.find_one({'_id':ObjectId(id)})
     if uid1:
          s_cart.delete_one({'_id':uid1['_id']})
     return redirect(url_for('cart'))

@app.route('/admin')
def admin():
    info=puja_items.find()
    l=[]
    for i in info:
          dummy=[]
          dummy.append(i.get('_id'))
          dummy.append(i.get('name'))
          dummy.append(i.get('price'))
          dummy.append(i.get('description'))
          dummy.append(i.get('image'))
          l.append(dummy)
    user_details =users.find()
    user=[]
    for j in user_details:
          dummy=[]
          dummy.append(j.get('_id'))
          dummy.append(j.get('name'))
          dummy.append(j.get('email'))
          dummy.append(j.get('phno'))
          user.append(dummy)
    p_details=p_list.find()
    pandit=[]
    for k in p_details:
         dummy=[]
         dummy.append(k.get('_id'))
         dummy.append(k.get('name'))
         dummy.append(k.get('age'))
         dummy.append(k.get('location'))
         dummy.append(k.get('phno'))
         dummy.append(k.get('email'))
         pandit.append(dummy)
    ap=a_pandit.find()
    apandit=[]
    for k in ap:
         dummy=[]
         dummy.append(k.get('_id'))
         dummy.append(k.get('name'))
         dummy.append(k.get('age'))
         dummy.append(k.get('location'))
         dummy.append(k.get('contact'))
         dummy.append(k.get('email'))
         apandit.append(dummy)

    k=[]
    puja_service=puja_services.find()
    for r in puja_service:
         dummy=[]
         dummy.append(r.get('_id'))
         dummy.append(r.get('p_name'))
         dummy.append(r.get('description'))
         dummy.append(r.get('price'))
         dummy.append(i.get('image'))
         
         
         k.append(dummy)  
    info1 = t_puja.find()
    temples = []
    for i in info1:
        temple_name = i.get('temple_name')
        pujas = i.get('pujas', [])

        for puja in pujas:
            temple_data = {
                '_id': i.get('_id'),
                't_name': temple_name,
                'p_name': puja.get('puja_name'),
                'location': puja.get('location'),
                'price': puja.get('price'),
                'description': puja.get('description')
            }
            temples.append(temple_data)

    prasad1=prasadam1.find()
    prasad=[]
    for i in prasad1:
                    mandir_name=i.get('mandir_name')
                    prasadam_items=i.get('prasadam_items',[])
                    for j in prasadam_items:
                        pdata={
                             '_id':i.get('_id'),
                             'mandir_name':mandir_name,
                             'prasadam_name':j.get('prasadam_name'),
                             'price':j.get('price'),
                             'description':j.get('description')
                        }
                        prasad.append(pdata)
    ban1=[]
    ban=banner.find()
    for i in ban:
         ban1.append(i.get('banner'))
    loc_names=[]
    l_name=loc.find()
    for i in l_name:
         dummy=[]
         dummy.append(i.get('_id'))
         dummy.append(i.get('location'))
         dummy.append(i.get('name'))
         dummy.append(i.get('mail'))
         dummy.append(i.get('location'))
         loc_names.append(dummy)
    selected_location=session.get('selected_loc')
    email=session.get('selected_mail')
    num=session.get('selected_num')
    address=session.get('selected_address')
         
    
    return render_template('admin.html',l=l,user=user,pandit=pandit,k=k,temples=temples,prasad=prasad,apandit=apandit,ban1=ban1,loc_names=loc_names,selected_location=selected_location,num=num,email=email,address=address)

@app.route('/display',methods=['POST','GET'])
def display():
     info=puja_items.find()
     l=[]
     for i in info:
          dummy=[]
          dummy.append(i.get('_id'))
          dummy.append(i.get('name'))
          dummy.append(i.get('price'))
          dummy.append(i.get('description'))
          l.append(dummy)
     return redirect(url_for('admin'))

@app.route('/p_delete/<id>',methods=['POST','GET'])
def p_delete(id):
     uid1=puja_items.find_one({'_id':ObjectId(id)})
     id1=uid1['_id']
     if id1:
          puja_items.delete_one({'_id':id1})
     return redirect(url_for('admin'))

@app.route('/updateSamagri/<id>', methods=['POST', 'GET'])
def updateSamagri(id):
    if request.method == 'POST':
        info = puja_items.find_one({'_id': ObjectId(id)})
        info1=puja_items.find()
        if info:
            update_fields = {}
            if 'name' in request.form and request.form['name'].strip() != "":
                update_fields['name'] = request.form['name']
            else:
                update_fields['name'] = info['name']
            if 'description' in request.form and request.form['description'].strip() != "":
                update_fields['description'] = request.form['description']
            else:
                update_fields['description'] = info['description']
            if 'price' in request.form and request.form['price'].strip() != "":
                update_fields['price'] = request.form['price']
            else:
                update_fields['price'] = info['price']
            if update_fields:
                puja_items.update_one({'_id': ObjectId(id)}, {'$set': update_fields})
        return redirect(url_for('admin'))

@app.route('/add', methods=['POST'])
def add():
    name = request.form['name']
    description = request.form['description']
    price = request.form['price']
    file = request.files['image']
    if not (name and description and price and file):
        return "All fields are required", 400
    if file.filename == '':
        return "No selected file", 400

    if not allowed_file(file.filename):
        return "File type not allowed", 400
    filename = secure_filename(file.filename)
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    item = {
        'name': name,
        'description': description,
        'price': price,
        'image': filename 
    }
    puja_items.insert_one(item)
    return redirect(url_for('admin'))

@app.route('/viewImage/<filename>')
def viewImage(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

    return redirect(url_for('admin')) 
    

@app.route('/updatePandit/<id>', methods=['POST', 'GET'])
def updatePandit(id):
    info = p_list.find_one({'_id': ObjectId(id)})
    info1=a_pandit.find_one({'_id':ObjectId(id)})
    if info:
        update_fields = {}
        if 'name' in request.form and request.form['name'].strip() != "":
            update_fields['name'] = request.form['name']
        else:
            update_fields['name'] = info['name']
        
        if 'age' in request.form and request.form['age'].strip() != "":
            update_fields['age'] = request.form['age']
        else:
            update_fields['age'] = info['age']

        if 'location' in request.form and request.form['location'].strip() != "":
            update_fields['location'] = request.form['location']
        else:
            update_fields['location'] = info['location']

        if 'phno' in request.form and request.form['phno'].strip() != "":
            update_fields['phno'] = request.form['phno']
        else:
            update_fields['phno'] = info['phno']

        if 'email' in request.form and request.form['email'].strip() != "":
            update_fields['email'] = request.form['email']
            emailp=update_fields['email']
        else:
            update_fields['email'] = info['email']
            emailp=info['email']

        if update_fields:
            p_list.update_one({'_id': ObjectId(id)}, {'$set': update_fields})
        return redirect(url_for('admin'))
    else:
            update_fields = {}
            if 'name' in request.form and request.form['name'].strip() != "":
                update_fields['name'] = request.form['name']
            else:
                update_fields['name'] = info1['name']
            
            if 'age' in request.form and request.form['age'].strip() != "":
                update_fields['age'] = request.form['age']
            else:
                update_fields['age'] = info1['age']

            if 'location' in request.form and request.form['location'].strip() != "":
                update_fields['location'] = request.form['location']
            else:
                update_fields['location'] = info1['location']

            if 'contact' in request.form and request.form['contact'].strip() != "":
                update_fields['contact'] = request.form['contact']
            else:
                update_fields['contact'] = info1['contact']

            if 'email' in request.form and request.form['email'].strip() != "":
                update_fields['email'] = request.form['email']
            else:
                update_fields['email'] = info1['email']

            if update_fields:
                a_pandit.update_one({'_id': ObjectId(id)}, {'$set': update_fields})
            return redirect(url_for('admin'))
    return redirect(url_for('admin'))

@app.route('/contact')
def contact():
     info=cart_item.find()
     info1=s_cart.find()
     l3=[]
     l4=[]
     for i in info:
                                if(session['email']==i.get('email')):
                                    dummy=[]
                                    dummy.append(i.get('_id'))
                                    dummy.append(i.get('name'))
                                    dummy.append(i.get('qty'))
                                    dummy.append(i.get('price'))
                                    dummy.append(i.get('total'))
                                    dummy.append(i.get('reg_date'))
                                    l3.append(dummy)
     for i in info1:
                                    if(session['email']==i.get('email')):
                                        dummy1=[]
                                        dummy1.append(i.get('_id'))
                                        dummy1.append(i.get('name'))
                                        dummy1.append(i.get('price'))
                                        dummy1.append(i.get('date'))
                                        dummy1.append(i.get('time'))
                                        dummy1.append(i.get('location'))
                                        dummy1.append(i.get('status'))
                                        dummy1.append(i.get('reg_date'))
                                        l4.append(dummy1)
     pList=[]
     info2=t_services.find()
     pujaList=[]
     for i in info2:
                                if(session['email']==i.get('email')):
                                    dummy=[]
                                    dummy.append(i.get('_id'))
                                    dummy.append(i.get('p_name'))
                                    dummy.append(i.get('t_name'))
                                    dummy.append(i.get('price'))
                                    dummy.append(i.get('date'))
                                    dummy.append(i.get('time'))
                                    dummy.append(i.get('status'))
                                    pujaList.append(dummy)
     pra1=[]
     info3=prasad1.find()
     for i in info3:
          if session['email']==i.get('email'):
                dummy=[]
                dummy.append(i.get('_id'))
                dummy.append(i.get('prasadam_name'))
                dummy.append(i.get('price'))
                dummy.append(i.get('total'))
                # prasadamTotal=prasadamTotal+i.get('total')
                dummy.append(i.get('qty'))
                dummy.append(i.get('date'))
                pra1.append(dummy)
     n=len(l3)+len(l4)+len(pujaList)+len(pra1)
     selected_location=session.get('selected_loc')
     email=session.get('selected_mail')
     num=session.get('selected_num')
     email=session.get('selected_mail')
     address=session.get('selected_address')
     return render_template('contactus.html',n=n,selected_location=selected_location,num=num,email=email,address=address)

@app.route('/contactus',methods=['POST','GET'])
def contactus():
    if request.method == 'POST':
        # Print form data for debugging
        print(request.form)
        
        try:
            name = request.form['username']
            email = request.form['email']
            message = request.form['message']
        except KeyError as e:
            # Handle missing form data gracefully
            return f"Missing data: {str(e)}", 400
        
        contact = {
            'name': name,
            'email': email,
            'message': message
        }
        # Assume contactUs is a MongoDB collection
        contactUs.insert_one(contact)
        
    return redirect(url_for('contact'))

@app.route('/addprasadam/<id>', methods=['POST', 'GET'])
def addprasadam(id):
    if request.method == 'POST':
        name = request.form['name']
        qty = request.form['qty']

       

       
        uid = t_puja.find_one({'_id': ObjectId(id)})
        
       

        temple_name = uid.get('temple_name')
        puja_name = None
        for puja in uid.get('pujas', []):
                puja_name = puja.get('puja_name')
                break
        
        if not puja_name:
            return render_template('404.html', message='Puja not found')

        # Retrieve the price from the prasadam1 collection
        prasadam = prasadam1.find_one({'mandir_name': temple_name, 'prasadam_items.prasadam_name': name}, 
                                      {'prasadam_items.$': 1})
        
        if not prasadam or not prasadam.get('prasadam_items'):
            return render_template('404.html', message='Prasadam not found')

        pri = prasadam['prasadam_items'][0].get('price')


        existing_item = prasad1.find_one({'email': session['email'], 'prasadam_name': name})
        total = int(pri) * int(qty)
        if existing_item:
            msg = "Item Already present in the Cart"
            new_qty = existing_item.get('qty') + int(qty)
            new_total = new_qty *int(pri)
            
            prasad1.update_one(
                {'_id': existing_item['_id']},
                {'$set': {'qty': new_qty, 'total': new_total}}
            )
        else:
            date = str(datetime.datetime.today()).split()[0]
            prasadam_data = {
                'email': session['email'],
                't_name': temple_name,
                'p_name': puja_name,
                'prasadam_name': name,
                'qty': int(qty),
                'date': date,
                'total': total,
                'price': pri,
                'status': "pending"
            }
            prasad1.insert_one(prasadam_data)

        return redirect(url_for('templepuj', temple_name=temple_name))
@app.route('/increase_qty/<id>', methods=['POST'])
def increase_qty(id):
    item = prasad1.find_one({'_id': ObjectId(id)})
    if item and int(item.get('qty', 0)) >= 1:
        prasad1.update_one({'_id': ObjectId(id)}, {'$inc': {'qty': 1}})
        
        # Convert the price from string to float and then to int
        price = int(float(item.get('price', '0')))
        
        n_total = (item.get('qty', 0) + 1) * price
        prasad1.update_one({'_id': ObjectId(id)}, {'$set': {'total': n_total}})
    else:
        abort(400, 'Quantity must be greater than or equal to one')
    return redirect(url_for('cart'))

@app.route('/decrease_qty/<item_id>', methods=['POST'])
def decrease_qty(item_id):
    item = prasad1.find_one({'_id': ObjectId(item_id)})
    if item:
        qty = int(item.get('qty', '0'))  # Convert qty to an integer
        if qty > 1:
            prasad1.update_one({'_id': ObjectId(item_id)}, {'$inc': {'qty': -1}}, upsert=False)
            price = float(item.get('price', '0'))  # Convert price to a float
            n_total = qty * price - price
            prasad1.update_one({'_id': ObjectId(item_id)}, {'$set': {'total': n_total}})
        else:
            prasad1.delete_one({'_id': ObjectId(item_id)})
    else:
        msg = "Quantity must be greater than or equal to one"
    return redirect(url_for('cart'))

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    info = users.find()
    
    l = []
    l1 = []
    
    name = ''  # Initialize with default value
    email = ''  # Initialize with default value
    phno = ''
    address= ''  # Initialize with default value
    
    for i in info:
        if session['email'] == i.get('email'):
            id=i.get('_id')
            name = i.get('name')
            email = i.get('email')
            phno = i.get('phno')
            address=i.get('address')
            
            info1 = cart_item.find()
            for j in info1:
                if session['email'] == j.get('email'):
                    dummy = []
                    dummy.append(j.get('name'))
                    dummy.append(j.get('qty'))
                    dummy.append(j.get('reg_date'))
                    dummy.append(j.get('price'))
                    l.append(dummy)
                
            info2 = s_cart.find()
            for k in info2:
                if session['email'] == k.get('email'):
                    dummy = [] 
                    dummy.append(k.get('name'))
                    dummy.append(k.get('location'))
                    dummy.append(k.get('date'))
                    dummy.append(k.get('time'))
                    dummy.append(k.get('price')) 
                    l1.append(dummy)  
            info2=t_services.find()
            pujaList=[]
            for i in info2:
                if(session['email']==i.get('email')):
                    dummy=[]
                    dummy.append(i.get('_id'))
                    dummy.append(i.get('p_name'))
                    dummy.append(i.get('t_name'))
                    dummy.append(i.get('price'))
                    dummy.append(i.get('date'))
                    dummy.append(i.get('time'))
                    dummy.append(i.get('status'))
                    pujaList.append(dummy)
            pra1=[]
            info3=prasad1.find()
            for i in info3:
                if session['email']==i.get('email'):
                        dummy=[]
                        dummy.append(i.get('_id'))
                        dummy.append(i.get('prasadam_name'))
                        dummy.append(i.get('price'))
                        dummy.append(i.get('total'))
                        
                        dummy.append(i.get('qty'))
                        dummy.append(i.get('date'))
                        pra1.append(dummy)
            saved_addresses = []
            address_list=[]
            data = users.find_one({'email': session['email']})
            if data:
                address_list = [
                addr["address"] for addr in data.get("address", []) 
                if isinstance(addr, dict) and "address" in addr and addr.get("status") == "Not Saved"
                ]
            if data:
                 saved_addresses = [
                 addr["address"] for addr in data.get("address", []) 
                 if isinstance(addr, dict) and "address" in addr and addr.get("status") == "Saved"
                ]   

    
    return render_template('profile.html', name=name, email=email, phno=phno,address=address, l=l, l1=l1,id=id,address_list=address_list,saved_addresses=saved_addresses,pujaList=pujaList,pra1=pra1)



@app.route('/updateProfile/<id>',methods=['POST','GET'])
def updateProfile(id):
    info = users.find_one({'_id': ObjectId(id)})
    if info:
        update_fields = {}
        if 'name' in request.form and request.form['name'].strip() != "":
            update_fields['name'] = request.form['name']
        else:
            update_fields['name'] = info['name']
        
        if 'email' in request.form and request.form['email'].strip() != "":
            update_fields['email'] = request.form['email']
        else:
            update_fields['email'] = info['email']
        
        if 'phno' in request.form and request.form['phno'].strip() != "":
            update_fields['phno'] = request.form['phno']
        else:
            update_fields['phno'] = info['phno']
        
        if 'address' in request.form and request.form['address'].strip() != "":
            update_fields['address'] = request.form['address']
        else:
            update_fields['address'] = info['address']
        
        if update_fields:
            users.update_one({'_id': ObjectId(id)}, {'$set': update_fields})
    
    return redirect(url_for('profile'))
     
     

@app.route('/temple')
def temple():
    info = t_puja.find()
    l = []
    l3 = []
    l4 = []
    pra1 = []
    pujaList = [] 
    pList = []
    temples = []

    for i in info:
        name = i.get('t_name')
        dummy = []
        if name not in [i[0] for i in l]:
            dummy.append(name)
            dummy.append(i.get('location'))
            dummy.append(i.get('timage'))
            l.append(dummy)

            cart_info = cart_item.find()
            s_cart_info = s_cart.find()
            for i in cart_info:
                if session['email'] == i.get('email'):
                    dummy = []
                    dummy.append(i.get('_id'))
                    dummy.append(i.get('name'))
                    dummy.append(i.get('qty'))
                    dummy.append(i.get('price'))
                    dummy.append(i.get('total'))
                    dummy.append(i.get('reg_date'))
                    l3.append(dummy)
            
            for i in s_cart_info:
                if session['email'] == i.get('email'):
                    dummy1 = []
                    dummy1.append(i.get('_id'))
                    dummy1.append(i.get('name'))
                    dummy1.append(i.get('price'))
                    dummy1.append(i.get('date'))
                    dummy1.append(i.get('time'))
                    dummy1.append(i.get('location'))
                    dummy1.append(i.get('status'))
                    dummy1.append(i.get('reg_date'))
                    l4.append(dummy1)


            pandit = p_list.find()
            for i in pandit:
                dummy2 = []
                dummy2.append(i.get('name'))
                dummy2.append(i.get('location'))
                pList.append(dummy2)

            t_services_info = t_services.find()
            for i in t_services_info:
                if session['email'] == i.get('email'):
                    dummy = []
                    dummy.append(i.get('_id'))
                    dummy.append(i.get('p_name'))
                    dummy.append(i.get('t_name'))
                    dummy.append(i.get('price'))
                    dummy.append(i.get('date'))
                    dummy.append(i.get('time'))
                    dummy.append(i.get('status'))
                    dummy.append(i.get('pimage'))
                    pujaList.append(dummy)


            info1 = t_puja.find()
            
            seen_temples = set()

            for i in info1:
                temple_name = i.get('temple_name')
                temple_image = i.get('temple_image')
                pujas = i.get('pujas', [])

                if temple_name not in seen_temples:
                    if pujas:  # Ensure there is at least one puja
                        puja = pujas[0]  # Take the first puja only
                        temple_data = {
                            '_id': i.get('_id'),
                            't_name': temple_name,
                            'p_name': puja.get('puja_name'),
                            'location': puja.get('location'),
                            'price': puja.get('price'),
                            'description': puja.get('description'),
                            'temple_image': temple_image,
                            'puja_image': puja.get('puja_image')
                        }
                        temples.append(temple_data)
                        seen_temples.add(temple_name)



            prasad_info = prasad1.find()
            for i in prasad_info:
                if session['email'] == i.get('email'):
                    dummy = []
                    dummy.append(i.get('_id'))
                    dummy.append(i.get('prasadam_name'))
                    dummy.append(i.get('price'))
                    dummy.append(i.get('total'))
                    dummy.append(i.get('qty'))
                    dummy.append(i.get('date'))
                    pra1.append(dummy)
    
    n = len(l3) + len(l4) + len(pujaList) + len(pra1)  
    selected_location=session.get('selected_loc')
    email=session.get('selected_mail')
    num=session.get('selected_num')
    email=session.get('selected_mail')
    address=session.get('selected_address')
    return render_template('temple.html', l=l, n=n,temples=temples,selected_location=selected_location,num=num,email=email,address=address)

@app.route('/templeDummy',methods=['POST','GET'])
def templeDummy():
    info = t_puja.find()
    l = []
    l3 = []
    l4 = []
    pra1 = []
    pujaList = [] 
    pList = []
    temples = []

    for i in info:
        name = i.get('t_name')
        dummy = []
        if name not in [i[0] for i in l]:
            dummy.append(name)
            dummy.append(i.get('location'))
            dummy.append(i.get('timage'))
            l.append(dummy)

            cart_info = cart_item.find()
            s_cart_info = s_cart.find()
            for i in cart_info:
                if session['email'] == i.get('email'):
                    dummy = []
                    dummy.append(i.get('_id'))
                    dummy.append(i.get('name'))
                    dummy.append(i.get('qty'))
                    dummy.append(i.get('price'))
                    dummy.append(i.get('total'))
                    dummy.append(i.get('reg_date'))
                    l3.append(dummy)
            
            for i in s_cart_info:
                if session['email'] == i.get('email'):
                    dummy1 = []
                    dummy1.append(i.get('_id'))
                    dummy1.append(i.get('name'))
                    dummy1.append(i.get('price'))
                    dummy1.append(i.get('date'))
                    dummy1.append(i.get('time'))
                    dummy1.append(i.get('location'))
                    dummy1.append(i.get('status'))
                    dummy1.append(i.get('reg_date'))
                    l4.append(dummy1)


            pandit = p_list.find()
            for i in pandit:
                dummy2 = []
                dummy2.append(i.get('name'))
                dummy2.append(i.get('location'))
                pList.append(dummy2)

            t_services_info = t_services.find()
            for i in t_services_info:
                if session['email'] == i.get('email'):
                    dummy = []
                    dummy.append(i.get('_id'))
                    dummy.append(i.get('p_name'))
                    dummy.append(i.get('t_name'))
                    dummy.append(i.get('price'))
                    dummy.append(i.get('date'))
                    dummy.append(i.get('time'))
                    dummy.append(i.get('status'))
                    dummy.append(i.get('pimage'))
                    pujaList.append(dummy)


            info1 = t_puja.find()
            
            seen_temples = set()

            for i in info1:
                temple_name = i.get('temple_name')
                temple_image = i.get('temple_image')
                pujas = i.get('pujas', [])

                if temple_name not in seen_temples:
                    if pujas:  # Ensure there is at least one puja
                        puja = pujas[0]  # Take the first puja only
                        temple_data = {
                            '_id': i.get('_id'),
                            't_name': temple_name,
                            'p_name': puja.get('puja_name'),
                            'location': puja.get('location'),
                            'price': puja.get('price'),
                            'description': puja.get('description'),
                            'temple_image': temple_image,
                            'puja_image': puja.get('puja_image')
                        }
                        temples.append(temple_data)
                        seen_temples.add(temple_name)



            prasad_info = prasad1.find()
            for i in prasad_info:
                if session['email'] == i.get('email'):
                    dummy = []
                    dummy.append(i.get('_id'))
                    dummy.append(i.get('prasadam_name'))
                    dummy.append(i.get('price'))
                    dummy.append(i.get('total'))
                    dummy.append(i.get('qty'))
                    dummy.append(i.get('date'))
                    pra1.append(dummy)
    
    n = len(l3) + len(l4) + len(pujaList) + len(pra1)  
    selected_location=session.get('selected_loc')
    email=session.get('selected_mail')
    num=session.get('selected_num')
    email=session.get('selected_mail')
    address=session.get('selected_address')
    return render_template('templedummy.html', l=l, n=n,temples=temples,selected_location=selected_location,num=num,email=email,address=address)


@app.route('/templepuja/<temple_name>')
def templepuj(temple_name):
    info = t_puja.find({'temple_name': temple_name})
    pujas = []

    for temple in info:
        for puja in temple.get('pujas', []):
            puja_data = {
                '_id': temple.get('_id'),
                'p_name': puja.get('puja_name'),
                'description': puja.get('description'),
                'price': puja.get('price'),
                'puja_image': puja.get('puja_image')
            }
            pujas.append(puja_data)

    l3 = []
    l4 = []
    info = cart_item.find()
    info1 = s_cart.find()
    
    for i in info:
        if session['email'] == i.get('email'):
            dummy = [
                i.get('_id'),
                i.get('name'),
                i.get('qty'),
                i.get('price'),
                i.get('total'),
                i.get('reg_date')
            ]
            l3.append(dummy)
    
    for i in info1:
        if session['email'] == i.get('email'):
            dummy1 = [
                i.get('_id'),
                i.get('name'),
                i.get('price'),
                i.get('date'),
                i.get('time'),
                i.get('location'),
                i.get('status'),
                i.get('reg_date')
            ]
            l4.append(dummy1)
    
    pList = []
    pandit = p_list.find()
    for i in pandit:
        dummy2 = [
            i.get('name'),
            i.get('location')
        ]
        pList.append(dummy2)
    
    info2 = t_services.find()
    pujaList = []
    for i in info2:
        if session['email'] == i.get('email'):
            dummy = [
                i.get('_id'),
                i.get('p_name'),
                i.get('t_name'),
                i.get('price'),
                i.get('date'),
                i.get('time'),
                i.get('status'),
                i.get('pimage')
            ]
            pujaList.append(dummy)
    
    pra1 = []
    info3 = prasad1.find()
    for i in info3:
        if session['email'] == i.get('email'):
            dummy = [
                i.get('_id'),
                i.get('prasadam_name'),
                i.get('price'),
                i.get('total'),
                i.get('qty'),
                i.get('date')
            ]
            pra1.append(dummy)
    
    pra = []
    unique_prasadam_names = set()
    info3 = prasadam1.find()
    for i in info3:
        dummy = [
            i.get('_id'),
            i.get('mandir_name')
        ]
        pra.append(dummy)
        if i.get('mandir_name') == temple_name:
            prasadam_items = i.get('prasadam_items', [])
            for item in prasadam_items:
                prasadam_name = item.get('prasadam_name')
                if prasadam_name:
                    unique_prasadam_names.add(prasadam_name)

    unique_prasadam_list = list(unique_prasadam_names)
    selected_location=session.get('selected_loc')
    email=session.get('selected_mail')
    num=session.get('selected_num')
    email=session.get('selected_mail')
    address=session.get('selected_address')
    
    n = len(l4) + len(l3) + len(pujaList) + len(pra1)

    return render_template('templepuja.html', pujas=pujas, n=n, pra=pra, unique_prasadam_list=unique_prasadam_list,selected_location=selected_location,num=num,address=address,email=email)

# @app.route('/addTService/<id>', methods=['POST', 'GET'])
# def addtService(id):
#     if request.method == 'POST':
#         date = request.form['date']
#         time = request.form['time']
#         uid = t_puja.find_one({'_id': ObjectId(id)})
#         pra = []
#         if uid:
           
#             for puja in uid.get('pujas', []):
#                 tServices = {
#                     'email': session['email'],
#                     't_name': uid.get('temple_name'),
#                     'p_name': puja.get('puja_name'),  
#                     'location': puja.get('location'),
#                     'price': puja.get('price'),  
#                     'date': date,
#                     'time': time,
#                     'status': "pending"
#                 }
#                 t_services.insert_one(tServices)
#         info = t_puja.find({'_id': ObjectId(id)})
#         pujas = []

#         for temple in info:
#             for puja in temple.get('pujas', []):
#                 puja_data = {
#                     '_id': temple.get('_id'),
#                     'p_name': puja.get('puja_name'),
#                     'description': puja.get('description'),
#                     'price': puja.get('price'),
#                     'puja_image': puja.get('puja_image')
#                 }
#                 pujas.append(puja_data)
#             info = t_puja.find()
#             l = []
#             for i in info:
#                 if i.get('t_name') == uid.get('t_name'):
#                     dummy = [
#                         i.get('_id'),
#                         i.get('p_name'),
#                         i.get('description'),
#                         i.get('price'),
#                         i.get('pimage')
#                     ]
#                     l.append(dummy)
#             l3 = []
#             l4 = []
#             info = cart_item.find()
#             info1 = s_cart.find()
#             for i in info:
#                 if session['email'] == i.get('email'):
#                     dummy = [
#                         i.get('_id'),
#                         i.get('name'),
#                         i.get('qty'),
#                         i.get('price'),
#                         i.get('total'),
#                         i.get('reg_date')
#                     ]
#                     l3.append(dummy)
#             for i in info1:
#                 if session['email'] == i.get('email'):
#                     dummy1 = [
#                         i.get('_id'),
#                         i.get('name'),
#                         i.get('price'),
#                         i.get('date'),
#                         i.get('time'),
#                         i.get('location'),
#                         i.get('status'),
#                         i.get('reg_date')
#                     ]
#                     l4.append(dummy1)
#             pList = []
#             pandit = p_list.find()
#             for i in pandit:
#                 dummy2 = [
#                     i.get('name'),
#                     i.get('location')
#                 ]
#                 pList.append(dummy2)
#             info2 = t_services.find()
#             pujaList = []
#             for i in info2:
#                 if session['email'] == i.get('email'):
#                     dummy = [
#                         i.get('_id'),
#                         i.get('p_name'),
#                         i.get('t_name'),
#                         i.get('price'),
#                         i.get('date'),
#                         i.get('time'),
#                         i.get('status')
#                     ]
#                     pujaList.append(dummy)
#             pra1 = []
#             info3 = prasad1.find()
#             for i in info3:
#                 if session['email'] == i.get('email'):
#                     dummy = [
#                         i.get('_id'),
#                         i.get('prasadam_name'),
#                         i.get('price'),
#                         i.get('total'),
#                         i.get('qty'),
#                         i.get('date')
#                     ]
#                     pra1.append(dummy)
#             unique_prasadam_names = set()
#             info3 = prasadam1.find()
#             for i in info3:
#                 dummy = [
#                     i.get('_id'),
#                     i.get('mandir_name')
#                 ]
#                 pra.append(dummy)

#                 prasadam_items = i.get('prasadam_items', [])
#                 for item in prasadam_items:
#                     prasadam_name = item.get('prasadam_name')
#                     if prasadam_name:
#                         unique_prasadam_names.add(prasadam_name)

#             unique_prasadam_list = list(unique_prasadam_names)
#             n = len(l3) + len(l4) + len(pujaList) + len(pra1)
        
#         return redirect(url_for('templepuj', temple_name=uid['temple_name']))

@app.route('/addTService/<id>/<puja_name>', methods=['POST','GET'])
def addtService(id, puja_name):
    if request.method == 'POST':
        date = request.form['date']
        time = request.form['time']
        uid = t_puja.find_one({'_id': ObjectId(id)})
        if uid:
            for puja in uid.get('pujas', []):
                if puja.get('puja_name') == puja_name:
                    tServices = {
                        'email': session['email'],
                        't_name': uid.get('temple_name'),
                        'p_name': puja.get('puja_name'),
                        'location': puja.get('location'),
                        'price': puja.get('price'),
                        'date': date,
                        'time': time,
                        'status': "pending"
                    }
                    t_services.insert_one(tServices)
                    break  # Exit the loop once the puja is found and added
        return redirect(url_for('templepuj', temple_name=uid['temple_name']))

        
        return redirect(url_for('templepuj', temple_name=uid['temple_name']))
     
@app.route('/deleteTemplePuja/<id>',methods=['POST','GET'])
def deleteTemplePuja(id):
     uid=t_services.find_one({'_id':ObjectId(id)})
     if uid:
          t_services.delete_one({'_id':uid['_id']})
     return redirect(url_for('cart'))

@app.route('/addService',methods=['POST','GET'])
def addService():
     p_name=request.form['name']
     description=request.form['description']
     price=request.form['price']
     file = request.files['image']

         # Check if all form fields are filled
     if not (p_name and description and price and file):
        return "All fields are required", 400

    # Check if the file upload is valid
     if file.filename == '':
        return "No selected file", 400

     if not allowed_file(file.filename):
        return "File type not allowed", 400

    # Save the uploaded file
     filename = secure_filename(file.filename)
     file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

     services={
          'p_name':p_name,
          'description':description,
          'price':price,
          'image': filename
     }
     puja_services.insert_one(services)
     return redirect(url_for('admin'))

@app.route('/deleteService/<id>',methods=['POST','GET'])
def deleteServices(id):
     uid1=puja_services.find_one({'_id':ObjectId(id)})
     if uid1:
          puja_services.delete_one({'_id':uid1['_id']})
     return redirect(url_for('admin'))

@app.route('/UpdateService/<id>',methods=['POST','GET'])
def UpdateService(id):
     if request.method == 'POST':
        info0 = puja_services.find_one({'_id': ObjectId(id)})
        if info0:
            update_fields = {}
            if 'name' in request.form and request.form['name'].strip() != "":
                update_fields['p_name'] = request.form['name']
            else:
                update_fields['name'] = info0['p_name']
            if 'price' in request.form and request.form['price'].strip() != "":
                update_fields['price'] = request.form['price']
            else:
                update_fields['price'] = info0['price']
            if 'description' in request.form and request.form['description'].strip() != "":
                update_fields['description'] = request.form['description']
            else:
                update_fields['description'] = info0['description']
           
            if update_fields:
                puja_services.update_one({'_id': ObjectId(id)}, {'$set': update_fields})        
     return redirect(url_for('admin'))

@app.route('/addPandit',methods=['POST','GET'])
def addPandit():
      name=request.form['name']
      age=request.form['age']
      location=request.form['location']
      contact=request.form['contact']
      email=request.form['email']
      p_data= {
            'name':name,
            'age':age,
            'location':location,
            'contact':contact,
            'email':email
      }
      a_pandit.insert_one(p_data)
      return redirect(url_for('admin'))

@app.route('/pandit_delete/<id>', methods=['GET'])
def deletePandit(id):
    uid=p_list.find_one({'_id':ObjectId(id)})
    if uid:
          p_list.delete_one({'_id':uid['_id']})
    else:
          uid1=a_pandit.find_one({'_id':ObjectId(id)})
          a_pandit.delete_one({'_id':uid1['_id']})
    return redirect(url_for('admin'))
      

# @app.route('/addTemples',methods=['POST','GET'])
# def addTemples():
#      t_name=request.form['t_name']
#      location=request.form['location']
#      p_name=request.form['p_name']
#      price=request.form['price']
#      description=request.form['description']
#      file = request.files['timage']
#      file1 = request.files['pimage']
#      if not (t_name and description and price and file):
#         return "All fields are required", 400

#     # Check if the file upload is valid
#      if file.filename == '':
#         return "No selected file", 400

#      if not allowed_file(file.filename):
#         return "File type not allowed", 400

#     # Save the uploaded file
#      filename = secure_filename(file.filename)
#      file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#      if not (p_name and description and price and file):
#         return "All fields are required", 400

#     # Check if the file upload is valid
#      if file1.filename == '':
#         return "No selected file", 400

#      if not allowed_file(file1.filename):
#         return "File type not allowed", 400

#     # Save the uploaded file
#      filename1 = secure_filename(file1.filename)
#      file1.save(os.path.join(app.config['UPLOAD_FOLDER'], filename1))

#      temple={
#           't_name':t_name,
#            'location':location,
#           'p_name':p_name,
         
#           'price':price,
#           'description':description,
#           'timage':filename,
#           'pimage':filename1
#      }
#      t_puja.insert_one(temple)
#      return redirect(url_for('admin'))

@app.route('/addTemples', methods=['POST'])
def add_temples():
    temple_name = request.form['t_name']
    temple_image = request.files['timage']

    puja_names = request.form.getlist('p_name')
    locations = request.form.getlist('location')
    prices = request.form.getlist('price')
    descriptions = request.form.getlist('description')
    puja_images = request.files.getlist('pimage')

    # Validate form inputs
    if not (temple_name and temple_image and all(puja_names) and all(prices) and all(descriptions) and all(puja_images)):
        return "All fields are required", 400

    # Validate temple image
    if temple_image.filename == '' or not allowed_file(temple_image.filename):
        return "Invalid temple image file", 400

    # Save temple image
    temple_image_filename = secure_filename(temple_image.filename)
    temple_image.save(os.path.join(app.config['UPLOAD_FOLDER'], temple_image_filename))

    pujas = []
    for i in range(len(puja_names)):
        if puja_images[i].filename == '' or not allowed_file(puja_images[i].filename):
            return "Invalid puja image file", 400

        puja_image_filename = secure_filename(puja_images[i].filename)
        puja_images[i].save(os.path.join(app.config['UPLOAD_FOLDER'], puja_image_filename))

        puja_data = {
            'puja_name': puja_names[i],
            'location': locations[i],
            'price': int(prices[i]),
            'description': descriptions[i],
            'puja_image': puja_image_filename
        }
        pujas.append(puja_data)

    temple_data = {
        'temple_name': temple_name,
        'temple_image': temple_image_filename,
        'pujas': pujas
    }
    t_puja.insert_one(temple_data)
    return redirect(url_for('admin'))
@app.route('/deletePuja/<temple_id>/<puja_name>', methods=['POST', 'GET'])
def delete_puja(temple_id, puja_name):
        temple = t_puja.find_one({'_id': ObjectId(temple_id)})
        if temple:
            updated_pujas = [puja for puja in temple['pujas'] if puja['puja_name'] != puja_name]
            if len(updated_pujas) == 0:
                t_puja.delete_one({'_id': ObjectId(temple_id)}) 
            else:
                t_puja.update_one({'_id': ObjectId(temple_id)}, {'$set': {'pujas': updated_pujas}})

        return redirect(url_for('admin'))

# @app.route('/updateTemple/<id>',methods=['POST','GET'])
# def updateTemple(id):
#      info=t_puja.find_one({'_id':ObjectId(id)})
#      t=[]
#      if info:
#             update_fields = {}
#             if 't_name' in request.form and request.form['t_name'].strip() != "":
#                 update_fields['t_name'] = request.form['t_name']
#             else:
#                 update_fields['t_name'] = info['t_name']
#             if 'p_name' in request.form and request.form['p_name'].strip() != "":
#                 update_fields['p_name'] = request.form['p_name']
#             else:
#                 update_fields['p_name'] = info['p_name']
#             if 'location' in request.form and request.form['location'].strip() != "":
#                 update_fields['location'] = request.form['location']
#             else:
#                 update_fields['location'] = info['location']
#             if 'price' in request.form and request.form['price'].strip() != "":
#                 update_fields['price'] = request.form['price']
#             else:
#                 update_fields['price'] = info['price']
            
#             if 'description' in request.form and request.form['description'].strip() != "":
#                 update_fields['description'] = request.form['description']
#             else:
#                 update_fields['description'] = info['description']
#             if update_fields:
#                 t_puja.update_one({'_id': ObjectId(id)}, {'$set': update_fields})
#      return redirect(url_for('admin'))

@app.route('/updateTemple/<id>/<puja_name>', methods=['POST','GET'])
def update_temple(id, puja_name):
    info = t_puja.find_one({'_id': ObjectId(id)})
    
    if info:
        
        pujas = info.get('pujas', [])
        for puja in pujas:
            if puja.get('puja_name') == puja_name:
                update_fields = {}
                
                if 'p_name' in request.form and request.form['p_name'].strip() != "":
                    update_fields['pujas.$.p_name'] = request.form['p_name']
                    
                
                if 'location' in request.form and request.form['location'].strip() != "":
                    update_fields['pujas.$.location'] = request.form['location']
                
                if 'price' in request.form and request.form['price'].strip() != "":
                    update_fields['pujas.$.price'] = request.form['price']
                
                if 'description' in request.form and request.form['description'].strip() != "":
                    update_fields['pujas.$.description'] = request.form['description']
                
                if update_fields:
                    t_puja.update_one({'_id': ObjectId(id), 'pujas.puja_name': puja_name}, {'$set': update_fields})
    
    return redirect(url_for('admin'))



@app.route('/addPrasadam',methods=['POST','GET'])
def addPrasadam():
     if request.method == 'POST':
        mandir_name = request.form.get('MandirName')
        prasadam_names = request.form.getlist('PrasadamName')
        prices = request.form.getlist('price')
        descriptions = request.form.getlist('description')

        prasadam_items = []
        for name, price, description in zip(prasadam_names, prices, descriptions):
            prasadam_items.append({
                'prasadam_name': name,
                'price': price,
                'description': description
            })

        existing_mandir = prasadam1.find_one({'mandir_name': mandir_name})

        if existing_mandir:
            # Append new prasadam items to the existing document
            prasadam1.update_one(
                {'mandir_name': mandir_name},
                {'$push': {'prasadam_items': {'$each': prasadam_items}}}
            )
        else:
            # Insert a new document
            prasadam1.insert_one({
                'mandir_name': mandir_name,
                'prasadam_items': prasadam_items
            })

        return redirect(url_for('admin'))
@app.route('/prasadamUpdate/<id>',methods=['POST','GET'])
def prasadamUpdate(id):
     info=prasadam1.find_one({'_id':ObjectId(id)})
     if info:
          update_fields = {}
          if 'name' in request.form and request.form['name'].strip() != "":
                update_fields['name'] = request.form['name']
          else:
            update_fields['name'] = info['name']
          if 'price' in request.form and request.form['price'].strip() != "":
                update_fields['price'] = request.form['price']
          else:
                update_fields['price'] = info['price']
     if update_fields:
                prasadam1.update_one({'_id': ObjectId(id)}, {'$set': update_fields})
     return redirect(url_for('admin'))

@app.route('/deletePrasadam/<id>',methods=['POST','GET'])
def deletePrasadam(id):
     uid=prasadam1.find_one({'_id':ObjectId(id)})
     if uid:
          prasadam1.delete_one({'_id': uid['_id']})
     return redirect(url_for('admin'))

@app.route('/editPandit/<id>', methods=['POST', 'GET'])
def editPandit(id):
    info = p_list.find_one({'_id':ObjectId(id)})
    if info:
        update_fields = {}
        if 'name' in request.form and request.form['name'].strip() != "":
            update_fields['name'] = request.form['name']
        else:
            update_fields['name'] = info['name']
        if 'email' in request.form and request.form['email'].strip() != "":
            update_fields['email'] = request.form['email']
        else:
            update_fields['email'] = info['email']
        if 'phno' in request.form and request.form['phno'].strip() != "":
            update_fields['phno'] = request.form['phno']
        else:
            update_fields['phno'] = info['phno']
        if 'location' in request.form and request.form['location'].strip() != "":
            update_fields['location'] = request.form['location']
        else:
            update_fields['location'] = info['location']
        
        if update_fields:
            p_list.update_one({'_id': ObjectId(id)}, {'$set': update_fields})  
    return redirect(url_for('pandit'))

@app.route('/deleteP/<id>', methods=['POST', 'GET'])
def deleteP(id):
    uid = prasad1.find_one({'_id': ObjectId(id)})
    if uid:
        prasad1.delete_one({'_id': uid['_id']})
    return redirect(url_for('cart'))

@app.route('/send_message', methods=['POST'])
def send_message():
    if request.method == 'POST':
        message = request.form.get('message')
        if message:
            # Store the message in the MongoDB collection
            # chat.insert_one({'message': message})

            # Your chatbot logic to generate a response
            # account_sid = 'AC4da61e8f74035eabee3b23f2d68dc2d3'
            # auth_token = '7d4264c8df08ac640d854db91d08f2bd'
            # client = Client(account_sid, auth_token)
            # message = client.messages.create(
            #     body=message,
            #     from_='+12513135289',
            #     to='+91 9392419102'
            # )
            return 'Message sent and processed'
        else:
            return 'No message provided', 400  # Bad request if message is missing
    else:
        return 'Method Not Allowed', 405  # Method not allowed for other HTTP methods

@app.route('/update_address_status/<address>', methods=['POST'])
def update_address_status(address):
    update_address = unquote(address)
    # update_address=address
    email = session['email']

    # Update the status of the address
    users.update_one(
        {'email': email, 'address.address': update_address},
        {'$set': {'address.$.status': 'Saved'}}
    )

    return redirect(url_for('profile'))

@app.route('/uploadbanner',methods=['POST','GET'])
def addbanner():
        file=request.files['banner']
        if not (file):
            return "All fields are required", 400
        if file.filename == '':
            return "No selected file", 400
        if not allowed_file(file.filename):
            return "File type not allowed", 400
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        banner1= {
             'banner':filename
        }
        banner.insert_one(banner1)
        return redirect(url_for('admin'))

@app.route('/admin_accept/<id>',methods=['POST','GET'])
def aAccept(id):
     info = s_cart.find_one({'_id': ObjectId(id)})
     id=info['_id']
     if info:
          s_cart.update_one(
            {'_id': id},
            {'$set': {'status': "Accepted"}}
        )
     return redirect(url_for('acceptpuja'))

@app.route('/admin_deny/<id>',methods=['POST','GET'])
def adeny(id):
     info = s_cart.find_one({'_id': ObjectId(id)})
     id=info['_id']
     if info:
          s_cart.update_one(
            {'_id': id},
            {'$set': {'status': "Rejected"}}
        )
     return redirect(url_for('acceptpuja'))

@app.route('/deleteUser/<id>',methods=['POST','GET'])
def deleteUser(id):
     data=users.find_one({'_id':ObjectId(id)})
     if data:
        users.delete_one({'_id':data['_id']})
     return redirect(url_for('admin'))

@app.route('/updateUser/<user_id>', methods=['POST','GET'])
def update_user(user_id):
    info = users.find_one({'_id': ObjectId(user_id)})
    if info:
        update_fields = {}
        if 'name' in request.form and request.form['name'].strip() != "":
            update_fields['name'] = request.form['name']
        else:
            update_fields['name'] = info['name']
        
        if 'email' in request.form and request.form['email'].strip() != "":
            update_fields['email'] = request.form['email']
        else:
            update_fields['email'] = info['email']
        
        if 'phno' in request.form and request.form['phno'].strip() != "":
            update_fields['phno'] = request.form['phno']
        else:
            update_fields['phno'] = info['phno']
        
        if update_fields:
            users.update_one({'_id': ObjectId(user_id)}, {'$set': update_fields})
    
    return redirect(url_for('admin'))

@app.route('/deletePrasadam/<id>/<prasadam_name>', methods=['POST', 'GET'])
def delete_prasadam(id, prasadam_name):
    temple = prasadam1.find_one({'_id': ObjectId(id)})
    if temple:
            updated_prasadam = [prasadam for prasadam in temple['prasadam_items'] if prasadam['prasadam_name'] != prasadam_name]
            if len(updated_prasadam) == 0:
                prasadam1.delete_one({'_id': ObjectId(id)})
            else:
                prasadam1.update_one({'_id': ObjectId(id)}, {'$set': {'prasadam_items': updated_prasadam}}) 
    return redirect(url_for('admin'))


@app.route('/updatePrasadam/<id>/<prasadam_name>', methods=['POST', 'GET'])
def update_prasadam(id, prasadam_name):
    temple = prasadam1.find_one({'_id': ObjectId(id)})

    if temple:
        prasadam_items = temple.get('prasadam_items', [])
        for prasadam in prasadam_items:
            if prasadam.get('prasadam_name') == prasadam_name:
                update_fields = {}

                if 'prasadam_name' in request.form and request.form['prasadam_name'].strip() != "":
                    update_fields['prasadam_items.$.prasadam_name'] = request.form['prasadam_name']

                if 'price' in request.form and request.form['price'].strip() != "":
                    update_fields['prasadam_items.$.price'] = request.form['price']

                if 'description' in request.form and request.form['description'].strip() != "":
                    update_fields['prasadam_items.$.description'] = request.form['description']

                if update_fields:
                    prasadam1.update_one({'_id': ObjectId(id), 'prasadam_items.prasadam_name': prasadam_name}, {'$set': update_fields})
                break  # Exit the loop once the matching prasadam is found and updated

    return redirect(url_for('admin'))

@app.route('/addAddress',methods=['POST','GET'])
def addAddress():
     address=request.form['address']

     new_address = {
        "address": address,
        "status": "Not Saved"
    }

    
     users.update_one({'email':session['email']}, {"$push": {"address": new_address}})
     return redirect(url_for('profile'))
@app.route('/addBanner/<banner_name>', methods=['POST','GET'])
def add_banner_to_home(banner_name):
    session['selected_banner'] = banner_name
    ban1=[]
    ban=banner.find()
    for i in ban:
                    ban1.append(i.get('banner'))
    return redirect(url_for('admin',ban1=ban1))

@app.route('/addLocation',methods=['POST','GET'])
def addLocation():
     location=request.form['location']
     name=request.form['name']
     mail=request.form['mail']
     address=request.form['address']
     loc_name={
          'location':location,
          'name':name,
          'mail':mail,
          'address':address
     }
     loc.insert_one(loc_name)
     return redirect(url_for('admin'))

@app.route('/addLoc/<id>',methods=['POST','GET'])
def add_loc(id):
     info=loc.find_one({'_id':ObjectId(id)})
     session['selected_loc']=info.get('location')
     session['selected_num']=info.get('name')
     session['selected_mail']=info.get('mail')
     session['selected_address']=info.get('address')
     print(id)
     loc_names=[]
     l_name=loc.find()
     for i in l_name:
         dummy=[]
         dummy.append(i.get('_id'))
         dummy.append(i.get('address'))
         dummy.append(i.get('name'))
         dummy.append(i.get('mail'))
         dummy.append(i.get('location'))
         loc_names.append(dummy)
     return redirect(url_for('admin'))
               
@app.route('/deleteBanner/<banner_name>', methods=['POST','GET'])
def delete_banner(banner_name):
    ban=banner.find_one({'banner':banner_name})
    if ban:
         banner.delete_one({'banner':ban['banner']})
    ban1=[]
    ban=banner.find()
    for i in ban:
                    ban1.append(i.get('banner'))
    return redirect(url_for('admin',ban1=ban1))

@app.route('/deleteLoc/<id>', methods=['POST','GET'])
def delete_Loc(id):
    ban=loc.find_one({'_id':ObjectId(id)})
    if ban:
         loc.delete_one({'_id':ObjectId(id)})
    return redirect(url_for('admin'))

@app.route('/deleteAdd/<addr>',methods=['POST','GET'])
def deleteAdd(addr):
    user_id = users.find_one({'email':session['email']})
    addr = unquote(addr)
    users.update_one(
        {'email':session['email']},
        {"$pull": {"address": {"address": addr}}}
    )
    return redirect(url_for('profile'))

      
if __name__ == '__main__':
 app.run(debug=True, host='127.0.0.1', port=5000)