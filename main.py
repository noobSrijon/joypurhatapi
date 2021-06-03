# -*- coding: utf-8 -*-
from flask import Flask, request, jsonify,render_template,redirect,session,url_for
from authenticate import authenticate
import os
from generate import *
import mysql.connector
import json
from hotels import hotel
def prochotel():
    x=[{'name': 'হোটেল প্রমি', 'address': 'সদর রাস্তা, থানার পশ্চিম পার্শ্বে, জয়পুরহাট ', 'contact': '০১৭২৭-৮০৬৬৬৭, ০৫৭১-৬২৯৬০'}, {'name': 'হোটেল পৃথিবী ইন্টারন্যাশনাল', 'address': 'সদর রোড, জয়পুরহাট।', 'contact': '০১৭১৭-৮৬৬৫২৯'}, {'name': 'হক কনভেনশন', 'address': 'জয়পুরহাট শহরের প্রাণকেন্দ্র পাঁচুর মোড় থেকে মাত্র ১.৫০ কিলোমিটার উত্তরে জয়পুরহাট-হিলি রোড সংলগ্ন', 'contact': '০৫৭১-৬২৬৩৩ , ০১৭১৩৩৬৪০৬৬'}, {'name': 'হোটেল সাদ', 'address': '১নং ষ্টেশন রোড, জয়পুরহাট।', 'contact': '০১৭২১-৯০৪৪৮৮, ০৫৭১-৫১০৯৭'}, {'name': 'হোটেল জাহানারা', 'address': 'সদর রোড, জয়পুরহাট।', 'contact': '০৫৭১-৬২৭৭৯'}, {'name': 'হোটেল বৈশাখী', 'address': 'ভাই ভাই মার্কেট,সদর রোড, জয়পুরহাট।', 'contact': '০১৭৮৪-০৩২৯০৮'}, {'name': 'হোটেল সৌরভ', 'address': 'থানা রোড, জয়পুরহাট।', 'contact': '০৫৭১-৬২০০৭'}]
    js={}
    for i in x:
        xv={"address":i["address"],"contact":i["contact"]}
        js[i["name"]]=xv
    return js


conn=mysql.connector.connect(host="remotemysql.com",user="UTvdZjgnr4",password="A9ef3AjDLY",database="UTvdZjgnr4")
cursor=conn.cursor()

app = Flask(__name__)
app.secret_key=os.urandom(24)
@app.route('/hotel', methods=['POST'])

def process_data():
    cursor.execute("""SELECT * FROM `users`""")
    users=cursor.fetchall()
    req_data = request.get_json(force=True)
    api_id=req_data["id"]
    api_key=req_data["key"]
    x=authenticate(users,api_id,api_key)
    if x:
        x=json.dumps(prochotel(),indent=4,ensure_ascii=False).encode("utf8")
        x=x.decode()
        return str(x)
    else:
        return jsonify({'status': 'Authentication Error'})
    
@app.route('/hotel/id=<idn>&key=<key>', methods=['GET'])
def process_datad(idn,key):
    cursor.execute("""SELECT * FROM `users`""")
    users=cursor.fetchall()
    api_id=idn
    api_key=key
    
    x=authenticate(users,api_id,api_key)
    
    #req_data = request.get_json(force=True)
    if x:
        x=json.dumps(prochotel(),indent=4,ensure_ascii=False).encode("utf8")
        x=x.decode()
        return str(x)
    else:
        return jsonify({'status': 'Authentication Error'})



@app.route('/')

def pm():
    return render_template('index.html')

@app.route('/dashboard')

def dash():
    if "user_id" in session:
        return render_template('dashboard.html', name=session['user_name'],api_id=session['api_id'],api_key=session['api_key'])
    else:
        return redirect('/login')


@app.route('/login')
def loginl():
    return render_template('login.html')
    #return str(username)+str(password)
@app.route('/register')
def regl():
    return render_template('register.html')
    #return str(username)+str(password)

@app.route('/login_vali',methods=['POST'])

def login_val():
    username=request.form.get("username")
    password=request.form.get("password")
    cursor.execute("""SELECT * FROM `users` WHERE `username` LIKE '{}' AND `password` LIKE '{}'""".format(username,password))
    users=cursor.fetchall()
    if len(users)>0:

        session['user_id']=users[0][0]
        session['user_name']=users[0][3]
        session['api_id']=users[0][5]
        session['api_key']=users[0][6]
        return redirect(url_for('.dash'))
    else:
        return redirect("/login")

@app.route('/add_user',methods=['POST'])
def reg_val():
    cursor.execute("""SELECT * FROM `users`""")
    users=cursor.fetchall()
    name=request.form.get("name")
    email=request.form.get("email")
    username=request.form.get("username")
    password=request.form.get("password")
    veri=verify(users,username,email)
    print(veri)
    api_id=gen_id(users)
    api_key=gen_key(users)
    if veri==True:
        cursor.execute("""INSERT INTO `users` (`id`, `username`, `password`, `name`, `email`,`api_id`,`api_key`) VALUES (Null, '{}', '{}', '{}', '{}','{}','{}');""".format(username,password,name,email,api_id,api_key))
        conn.commit()
        cursor.execute("""SELECT * FROM `users` WHERE `email` LIKE '{}' """.format(email))
        users=cursor.fetchall()
        session['user_id']=users[0][0]
        session['user_name']=users[0][3]
        session['api_id']=users[0][5]
        session['api_key']=users[0][6]
        return redirect(url_for('.dash'))
    else:
        return redirect('/register')
    
@app.route('/logout')
def logout():
    session.pop('user_id')
    return redirect('/')

@app.route('/test')
def logoudt():
    cursor.execute("""SELECT * FROM `users`""")
    users=cursor.fetchall()
    print(users)
    return "xyz"




    #return str(username)+str(password)
if __name__ == "__main__":
    app.run(debug=True)
