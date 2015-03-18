import os
import uuid
import psycopg2
import psycopg2.extras
from flask import Flask, session, render_template, request
from flask.ext.socketio import SocketIO,emit
#from flask import Flask, render_temate
#from flask.ext.socketio import SocketIO, emit

app = Flask(__name__, static_url_path='')
app.config['SECRET_KEY'] = 'secret!'

socketio = SocketIO(app)

messages = [{'text':'test', 'name':'testName'}]
searchMsg = [{'text':'test', 'name':'testName'}]
users = {}


def connectToDB():
  connectionString = 'dbname=messenger user=postgres password=matsutaka host=localhost'
  try:
    return psycopg2.connect(connectionString)
  except:
    print("Can't connect to database")

def updateRoster():
    names = []
    for user_id in  users:
        print users[user_id]['username']
        if len(users[user_id]['username'])==0:
           names.append('Anonymous')
        else:
            names.append(users[user_id]['username'])
    print 'broadcasting names'
    emit('roster', names, broadcast=True)
    

@socketio.on('connect', namespace='/chat')
def test_connect():
    session['uuid']=uuid.uuid1()
    session['username']='starter name'
    print 'connected'
    
    users[session['uuid']]={'username':'New User'}
    if session['uuid'] in users:
        del users[session['uuid']]

    updateRoster()

    del messages[:]
    for message in messages:
        emit('message', message)
        
    

@socketio.on('message', namespace='/chat')
def new_message(message):
    
        conn = connectToDB()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        try:
            #tmp = {'text':message, 'name':'testName'}
            tmp = {'text':message, 'name':users[session['uuid']]['username']}
            print (tmp)
            query = "INSERT INTO messages VALUES (%s, %s) "
            cur.execute(query, (message, users[session['uuid']]['username']))
            conn.commit()
            cur.close()
            conn.close()
            messages.append(tmp)
            emit('message', tmp, broadcast=True)
        except:
            print("INSERT MESSAGE FAIL")
            
@socketio.on('search', namespace='/chat')
def new_search(search):
    
    print("HERE")
    if search!='':
        print("REALLY IN HERE")
        conn = connectToDB()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        try:
        
            search = '%'+search+'%'
            query = "SELECT message, username FROM messages WHERE message LIKE '%s' " % (search)
            cur.execute(query)
            rows = cur.fetchall()
            conn.commit()
            cur.close()
            conn.close()
            
            del searchMsg[:]
            for row in rows:
                 str = '***'
                 row = str.join(row)
                 t = row.partition("***")
                 tmp = {'text':t[0], 'name':t[2]}
                 searchMsg.append(tmp)
                 
            print("HERE")
            print(searchMsg)
            for message in searchMsg:
                emit('search', message)
        
        except:
            print("SEARCH MESSAGE FAIL")
         
@socketio.on('identify', namespace='/chat')
def on_identify(message):
    print 'identify' + message
    users[session['uuid']]={'username':message}
    updateRoster()
    
    
@socketio.on('login', namespace='/chat')
def on_login(pw):
    
    updateRoster()
    
#    if pw or users[session['uuid']]['username'] == "":
        
    conn = connectToDB()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    query = "SELECT * FROM users WHERE username LIKE '%s' AND password LIKE '%s' " % (users[session['uuid']]['username'], pw)
    cur.execute(query)
    results = cur.fetchall()
    conn.commit()
    cur.close()
    conn.close()
    print("RESULTS ARE: ")
    print(results)
    if results == []:
        emit('login')
        #emit(registered,users[session['uuid']]['username'])
    elif results!=[]:
        emit('run')
        print("Welcome Back " + users[session['uuid']]['username'])
        conn = connectToDB()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        try:
            query = "SELECT message, username FROM messages" 
            print(query)
            cur.execute(query)
            rows = cur.fetchall()
            conn.commit()
            cur.close()
            conn.close()
            
            del messages[:]
            for row in rows:
                 str = '***'
                 row = str.join(row)
                 t = row.partition("***")
                 tmp = {'text':t[0], 'name':t[2]}
                 messages.append(tmp)
                 print(tmp)
                 
            for message in messages:
                emit('message', message)
        
        
        except:
            print("ERROR SELECTING MESSAGES")
    #users[session['uuid']]={'username':message}
    #updateRoster()

@socketio.on('disconnect', namespace='/chat')
def on_disconnect():
    print 'disconnect'
    if session['uuid'] in users:
        del users[session['uuid']]
        updateRoster()

@app.route('/')
def hello_world():
    print 'in hello world'
    return app.send_static_file('index.html')
    return 'Hello World!'

@app.route('/js/<path:path>')
def static_proxy_js(path):
    # send_static_file will guess the correct MIME type
    return app.send_static_file(os.path.join('js', path))
    
@app.route('/css/<path:path>')
def static_proxy_css(path):
    # send_static_file will guess the correct MIME type
    return app.send_static_file(os.path.join('css', path))
    
@app.route('/img/<path:path>')
def static_proxy_img(path):
    # send_static_file will guess the correct MIME type
    return app.send_static_file(os.path.join('img', path))
    
if __name__ == '__main__':
    print "A"

    socketio.run(app, host=os.getenv('IP', '0.0.0.0'), port=int(os.getenv('PORT', 8080)))
     