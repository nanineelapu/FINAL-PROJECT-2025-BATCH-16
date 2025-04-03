from django.shortcuts import render
from django.http import HttpResponse
import os, pickle, random
import pymysql
from datetime import date

# Import hybrid encryption functions
from encryption.hybrid_encryption import (
    CPABE_generate_keys,
    hybrid_encrypt_file,
    hybrid_decrypt_file
)

global username

# -------------------- Authentication and Basic Views --------------------
def AVLoginAction(request):
    global username
    if request.method == 'POST':
        username = request.POST.get('t1', False)
        password = request.POST.get('t2', False)
        if username == 'admin' and password == 'admin':
            status = 'Welcome : ' + username
            context = {'data': status}
            return render(request, 'AVScreen.html', context)
        else:
            context = {'data': 'Invalid username'}
            return render(request, 'AVLogin.html', context)

def UserLogin(request):
    global username
    if request.method == 'POST':
        username = request.POST.get('t1', False)
        password = request.POST.get('t2', False)
        status = "failed"
        con = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='root', database='cybersecurity', charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("SELECT username, password FROM register")
            rows = cur.fetchall()
            for row in rows:
                if row[0] == username and row[1] == password:
                    status = 'success'
                    break
        if status == 'success':
            status = 'Welcome : ' + username
            context = {'data': status}
            return render(request, 'UserScreen.html', context)
        else:
            context = {'data': 'Invalid username or password'}
            return render(request, 'Login.html', context)

# -------------------- File Operations --------------------
def DownloadFileAction(request):
    if request.method == 'GET':
        name = request.GET['option']
        private_key, public_key = CPABE_generate_keys()
        with open('CyberSecurityApp/static/Upload/' + name, 'rb') as file:
            package = pickle.load(file)
        file_data = hybrid_decrypt_file(package, private_key)
        response = HttpResponse(file_data, content_type='application/octet-stream')
        response['Content-Disposition'] = 'attachment; filename=' + name
        return response

def DownloadFile(request):
    if request.method == 'GET':
        global username
        font = '<font size="" color="black">'
        output = '<table border=1 align=center>'
        output += '<tr><th><font size=3 color=black>File ID</font></th>'
        output += '<th><font size=3 color=black>Sender Name</font></th>'
        output += '<th><font size=3 color=black>File Name</font></th>'
        output += '<th><font size=3 color=black>File Description</font></th>'
        output += '<th><font size=3 color=black>Encryption Key (Part)</font></th>'
        output += '<th><font size=3 color=black>Upload Date</font></th>'
        output += '<th><font size=3 color=black>Download File from AV</font></th></tr>'
        con = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='root', database='cybersecurity', charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("SELECT * FROM upload WHERE sender='" + username + "'")
            rows = cur.fetchall()
            for row in rows:
                output += "<tr><td>" + font + str(row[0]) + "</td>"
                output += "<td>" + font + row[1] + "</td>"
                output += "<td>" + font + row[2] + "</td>"
                output += "<td>" + font + row[3] + "</td>"
                output += "<td>" + font + row[4] + "</td>"
                output += "<td>" + font + row[5] + "</td>"
                output += '<td><a href="DownloadFileAction?option=' + str(row[2]) + '"><font size=3 color=black>Click Here</font></a></td></tr>'
        output += '</table><br/><br/><br/><br/><br/>'
        context = {'data': output}
        return render(request, 'UserScreen.html', context)

def ViewStatus(request):
    if request.method == 'GET':
        global username
        font = '<font size="" color="black">'
        output = '<table border=1 align=center>'
        output += '<tr><th><font size=3 color=black>File ID</font></th>'
        output += '<th><font size=3 color=black>Sender Name</font></th>'
        output += '<th><font size=3 color=black>File Name</font></th>'
        output += '<th><font size=3 color=black>File Description</font></th>'
        output += '<th><font size=3 color=black>Encryption Key (Part)</font></th>'
        output += '<th><font size=3 color=black>Uploaded Date</font></th>'
        output += '<th><font size=3 color=black>Status</font></th></tr>'
        con = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='root', database='cybersecurity', charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("SELECT * FROM upload WHERE sender='" + username + "'")
            rows = cur.fetchall()
            for row in rows:
                output += "<tr><td>" + font + str(row[0]) + "</td>"
                output += "<td>" + font + row[1] + "</td>"
                output += "<td>" + font + row[2] + "</td>"
                output += "<td>" + font + row[3] + "</td>"
                output += "<td>" + font + row[4] + "</td>"
                output += "<td>" + font + row[5] + "</td>"
                output += "<td>" + font + "Uploaded to AV Successfully" + "</td></tr>"
        output += '</table><br/><br/><br/><br/><br/>'
        context = {'data': output}
        return render(request, 'UserScreen.html', context)

def ViewReceived(request):
    if request.method == 'GET':
        global username
        font = '<font size="" color="black">'
        output = '<table border=1 align=center>'
        output += '<tr><th><font size=3 color=black>File ID</font></th>'
        output += '<th><font size=3 color=black>Sender Name</font></th>'
        output += '<th><font size=3 color=black>File Name</font></th>'
        output += '<th><font size=3 color=black>File Description</font></th>'
        output += '<th><font size=3 color=black>Encryption Key (Part)</font></th>'
        output += '<th><font size=3 color=black>Uploaded Date</font></th></tr>'
        con = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='root', database='cybersecurity', charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("SELECT * FROM upload")
            rows = cur.fetchall()
            for row in rows:
                output += "<tr><td>" + font + str(row[0]) + "</td>"
                output += "<td>" + font + row[1] + "</td>"
                output += "<td>" + font + row[2] + "</td>"
                output += "<td>" + font + row[3] + "</td>"
                output += "<td>" + font + row[4] + "</td>"
                output += "<td>" + font + row[5] + "</td></tr>"
        output += '</table><br/><br/><br/><br/><br/>'
        context = {'data': output}
        return render(request, 'AVScreen.html', context)

def UploadAction(request):
    if request.method == 'POST':
        global username
        desc = request.POST.get('t1', False)
        file_obj = request.FILES['t2']
        data = file_obj.read()
        name = file_obj.name
        # Generate CP-ABE keys and get public key.
        private_key, public_key = CPABE_generate_keys()
        # Use hybrid encryption: encrypt file data with AES then encrypt AES key with CP-ABE.
        package = hybrid_encrypt_file(data, "role:admin", public_key)
        # Save the encrypted package to the static/Upload folder.
        with open('CyberSecurityApp/static/Upload/' + name, 'wb') as file:
            pickle.dump(package, file)
        today = str(date.today())
        file_id = 0
        con = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='root', database='cybersecurity', charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("SELECT MAX(file_id) FROM upload")
            rows = cur.fetchall()
            for row in rows:
                file_id = row[0]
                break
        file_id = 1 if file_id is None else file_id + 1
        # For display purposes, show a substring of the public key.
        public_key_str = str(public_key)
        display_key = public_key_str[10:20]
        db_connection = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='root', database='cybersecurity', charset='utf8')
        db_cursor = db_connection.cursor()
        student_sql_query = ("INSERT INTO upload(file_id, sender, filename, file_desc, encrypt_key, msg_date) "
                             "VALUES('" + str(file_id) + "','" + username + "','" + name + "','" + desc + "','" + display_key + "','" + today + "')")
        db_cursor.execute(student_sql_query)
        db_connection.commit()
        if db_cursor.rowcount == 1:
            context = {'data': 'File sent to cloud server with encrypted key ' + display_key}
            return render(request, 'Upload.html', context)
        else:
            context = {'data': 'Error in sending file'}
            return render(request, 'Upload.html', context)

def Upload(request):
    if request.method == 'GET':
        return render(request, 'Upload.html', {})

def Register(request):
    if request.method == 'GET':
        return render(request, 'Register.html', {})

def index(request):
    if request.method == 'GET':
        return render(request, 'index.html', {})

def Login(request):
    if request.method == 'GET':
        return render(request, 'Login.html', {})

def AVLogin(request):
    if request.method == 'GET':
        return render(request, 'AVLogin.html', {})

def RegisterAction(request):
    if request.method == 'POST':
        global username
        username = request.POST.get('t1', False)
        password = request.POST.get('t2', False)
        contact = request.POST.get('t3', False)
        email = request.POST.get('t4', False)
        address = request.POST.get('t5', False)
        output = "none"
        con = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='root', database='cybersecurity', charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("SELECT username FROM register")
            rows = cur.fetchall()
            for row in rows:
                if row[0] == username:
                    output = username + " Username already exists"
        if output == "none":
            db_connection = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='root', database='cybersecurity', charset='utf8')
            db_cursor = db_connection.cursor()
            student_sql_query = ("INSERT INTO register(username, password, contact, email, address) "
                                 "VALUES('" + username + "','" + password + "','" + contact + "','" + email + "','" + address + "')")
            db_cursor.execute(student_sql_query)
            db_connection.commit()
            if db_cursor.rowcount == 1:
                context = {'data': 'Signup Process Completed'}
                return render(request, 'Register.html', context)
            else:
                context = {'data': 'Error in signup process'}
                return render(request, 'Register.html', context)
        else:
            context = {'data': output}
            return render(request, 'Register.html', context)


'''

from django.shortcuts import render
from django.template import RequestContext
from django.contrib import messages
from django.http import HttpResponse
from django.conf import settings
import os
import pymysql
from django.core.files.storage import FileSystemStorage
from datetime import date
from ecies.utils import generate_eth_key, generate_key
from ecies import encrypt, decrypt
import base64
import pickle
import random

global username

#function to generate public and private keys for CP-ABE algorithm
def CPABEgenerateKeys():
    if os.path.exists("CyberSecurityApp/static/public") == False:
        secret_key = generate_eth_key()
        private_key = secret_key.to_hex()  # hex string
        public_key = secret_key.public_key.to_hex()
        with open('CyberSecurityApp/static/public', 'wb') as file:
            pickle.dump(public_key, file)
        file.close()
        with open('CyberSecurityApp/static/private', 'wb') as file:
            pickle.dump(private_key, file)
        file.close()
    else:
        with open('CyberSecurityApp/static/public', 'rb') as file:
            public_key = pickle.load(file)
        file.close()
        with open('CyberSecurityApp/static/private', 'rb') as file:
            private_key = pickle.load(file)
        file.close()        
    return private_key, public_key

#CP-ABE will encrypt data using plain text adn public key
def CPABEEncrypt(plainText, public_key):
    cpabe_encrypt = encrypt(public_key, plainText)
    return cpabe_encrypt

#CP-ABE will decrypt data using private key and encrypted text
def CPABEDecrypt(encrypt, private_key):
    cpabe_decrypt = decrypt(private_key, encrypt)
    return cpabe_decrypt


def AVLoginAction(request):
    global username
    if request.method == 'POST':
        username = request.POST.get('t1', False)
        password = request.POST.get('t2', False)
        if username == 'admin' and password == 'admin':
            status = 'Welcome : '+username
            context= {'data':status}
            return render(request, 'AVScreen.html', context)
        else:
            context= {'data':'Invalid username'}
            return render(request, 'AVLogin.html', context)

def UserLogin(request):
    global username
    if request.method == 'POST':
        username = request.POST.get('t1', False)
        password = request.POST.get('t2', False)
        status = "failed"
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'cybersecurity',charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("select username,password FROM register")
            rows = cur.fetchall()
            for row in rows:
                if row[0] == username and row[1] == password:
                    status = 'success'
                    break
        if status == 'success':
            status = 'Welcome : '+username
            context= {'data':status}
            return render(request, 'UserScreen.html', context)
        else:
            context= {'data':'Invalid username'}
            return render(request, 'Login.html', context)

def DownloadFileAction(request):
    if request.method == 'GET':
        name = request.GET['option']
        private_key, public_key = CPABEgenerateKeys()
        with open('CyberSecurityApp/static/Upload/'+name, 'rb') as file:
            encrypted_data = pickle.load(file)
        file.close()
        decryptedData = CPABEDecrypt(encrypted_data, private_key)
        response = HttpResponse(decryptedData,content_type='application/octet-stream')
        response['Content-Disposition'] = 'attachment; filename='+name
        return response   

def DownloadFile(request):
    if request.method == 'GET':
        global username
        font = '<font size="" color="black">'
        output = '<table border=1 align=center>'
        output+='<tr><th><font size=3 color=black>File ID</font></th>'
        output+='<th><font size=3 color=black>Sender Name</font></th>'
        output+='<th><font size=3 color=black>File Name</font></th>'
        output+='<th><font size=3 color=black>File Description</font></th>'
        output+='<th><font size=3 color=black>Encryption Key</font></th>'
        output+='<th><font size=3 color=black>Upload Date</font></th>'
        output+='<th><font size=3 color=black>Download File from AV</font></th></tr>'
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'cybersecurity',charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("select * FROM upload where sender='"+username+"'")
            rows = cur.fetchall()
            for row in rows:
                output += "<tr><td>"+font+str(row[0])+"</td>"
                output += "<td>"+font+row[1]+"</td>"
                output += "<td>"+font+row[2]+"</td>"
                output += "<td>"+font+row[3]+"</td>"
                output += "<td>"+font+row[4]+"</td>"
                output += "<td>"+font+row[5]+'</td>'
                output += '<td><a href=\'DownloadFileAction?option='+str(row[2])+'\'><font size=3 color=black>Click Here</font></a></td></tr>'
        output+='</table>'
        output+="<br/><br/><br/><br/><br/>"
        context= {'data':output}
        return render(request, 'UserScreen.html', context)        

def ViewStatus(request):
    if request.method == 'GET':
        global username
        font = '<font size="" color="black">'
        output = '<table border=1 align=center>'
        output+='<tr><th><font size=3 color=black>File ID</font></th>'
        output+='<th><font size=3 color=black>Sender Name</font></th>'
        output+='<th><font size=3 color=black>File Name</font></th>'
        output+='<th><font size=3 color=black>File Description</font></th>'
        output+='<th><font size=3 color=black>Encryption Key</font></th>'
        output+='<th><font size=3 color=black>Uploaded Date</font></th>'
        output+='<th><font size=3 color=black>Status</font></th></tr>'
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'cybersecurity',charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("select * FROM upload where sender='"+username+"'")
            rows = cur.fetchall()
            for row in rows:
                output += "<tr><td>"+font+str(row[0])+"</td>"
                output += "<td>"+font+row[1]+"</td>"
                output += "<td>"+font+row[2]+"</td>"
                output += "<td>"+font+row[3]+"</td>"
                output += "<td>"+font+row[4]+"</td>"
                output += "<td>"+font+row[5]+'</td>'
                output += "<td>"+font+"Uploaded to AV Successfully"+'</td></tr>'
        output+='</table>'
        output+="<br/><br/><br/><br/><br/>"
        context= {'data':output}
        return render(request, 'UserScreen.html', context)

def ViewReceived(request):
    if request.method == 'GET':
        global username
        font = '<font size="" color="black">'
        output = '<table border=1 align=center>'
        output+='<tr><th><font size=3 color=black>File ID</font></th>'
        output+='<th><font size=3 color=black>Sender Name</font></th>'
        output+='<th><font size=3 color=black>File Name</font></th>'
        output+='<th><font size=3 color=black>File Description</font></th>'
        output+='<th><font size=3 color=black>Encryption Key</font></th>'
        output+='<th><font size=3 color=black>Uploaded Date</font></th></tr>'
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'cybersecurity',charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("select * FROM upload")
            rows = cur.fetchall()
            for row in rows:
                output += "<tr><td>"+font+str(row[0])+"</td>"
                output += "<td>"+font+row[1]+"</td>"
                output += "<td>"+font+row[2]+"</td>"
                output += "<td>"+font+row[3]+"</td>"
                output += "<td>"+font+row[4]+"</td>"
                output += "<td>"+font+row[5]+'</td></tr>'
        output+='</table>'
        output+="<br/><br/><br/><br/><br/>"
        context= {'data':output}
        return render(request, 'AVScreen.html', context)      

def UploadAction(request):
    if request.method == 'POST':
        global username
        desc = request.POST.get('t1', False)
        data = request.FILES['t2'].read()
        name = request.FILES['t2'].name
        private_key, public_key = CPABEgenerateKeys()
        encrypted = CPABEEncrypt(data, public_key)
        with open('CyberSecurityApp/static/Upload/'+name, 'wb') as file:
            pickle.dump(encrypted, file)
        file.close()
        today = str(date.today())
        file_id = 0
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'cybersecurity',charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("select max(file_id) from upload")
            rows = cur.fetchall()
            for row in rows:
                file_id = row[0]
                break
        if file_id is None:
            file_id = 1
        else:
            file_id = file_id + 1
        public_key = str(public_key)
        start = random.randrange(10, 15)
        end = random.randrange(15, 30)
        public_key = public_key[start:end]
        db_connection = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'cybersecurity',charset='utf8')
        db_cursor = db_connection.cursor()
        student_sql_query = "INSERT INTO upload(file_id,sender,filename,file_desc,encrypt_key,msg_date) VALUES('"+str(file_id)+"','"+username+"','"+name+"','"+desc+"','"+str(public_key)+"','"+today+"')"
        db_cursor.execute(student_sql_query)
        db_connection.commit()
        print(db_cursor.rowcount, "Record Inserted")
        if db_cursor.rowcount == 1:
            context= {'data':'File sent to cloud server with encrypted key '+str(public_key)}
            return render(request, 'Upload.html', context)
        else:
            context= {'data':'Error in sending file'}
            return render(request, 'Upload.html', context)       
        

def Upload(request):
    if request.method == 'GET':
       return render(request, 'Upload.html', {})

def Register(request):
    if request.method == 'GET':
       return render(request, 'Register.html', {})    

def index(request):
    if request.method == 'GET':
       return render(request, 'index.html', {})

def Login(request):
    if request.method == 'GET':
       return render(request, 'Login.html', {})

def AVLogin(request):
    if request.method == 'GET':
       return render(request, 'AVLogin.html', {})    

def RegisterAction(request):
    if request.method == 'POST':
        global username
        username = request.POST.get('t1', False)
        password = request.POST.get('t2', False)
        contact = request.POST.get('t3', False)
        email = request.POST.get('t4', False)
        address = request.POST.get('t5', False)
        output = "none"
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'cybersecurity',charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("select username FROM register")
            rows = cur.fetchall()
            for row in rows:
                if row[0] == username:
                    output = username+" Username already exists"                    
        if output == "none":                      
            db_connection = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'cybersecurity',charset='utf8')
            db_cursor = db_connection.cursor()
            student_sql_query = "INSERT INTO register(username,password,contact,email,address) VALUES('"+username+"','"+password+"','"+contact+"','"+email+"','"+address+"')"
            db_cursor.execute(student_sql_query)
            db_connection.commit()
            print(db_cursor.rowcount, "Record Inserted")
            if db_cursor.rowcount == 1:
                context= {'data':'Signup Process Completed'}
                return render(request, 'Register.html', context)
            else:
                context= {'data':'Error in signup process'}
                return render(request, 'Register.html', context)
        else:
            context= {'data':output}
            return render(request, 'Register.html', context)    
    

'''