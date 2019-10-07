from celery import Celery
from flask_socketio import SocketIO, emit
from flask import Flask, render_template, url_for, copy_current_request_context, request
from flask_restplus import Api, Resource, fields

app = Flask(__name__)
app.config['SECRET_KEY'] = 'top-secret!'

api = Api(app, version=3)
socketio = SocketIO(app)

celery = Celery('http_interface')
celery.conf.update(app.config)

name_space = api.namespace('streams', description="APIs to control data streams")

@app.route("/events")
def show_events():
    if request.method == "GET":
        return render_template('index.html')

@celery.task
def add(x, y):
    return x + y

if __name__ == '__main__':
    app.run()
 
