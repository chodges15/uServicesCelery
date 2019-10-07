from celery import Celery
from flask_socketio import SocketIO, emit
from flask import Flask, render_template, url_for, redirect, request, flash
from flask_restplus import Api, Resource, fields
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'top-secret!'

api = Api(app, version=3)
socketio = SocketIO(app)

celery = Celery('http_interface')
celery.conf.update(app.config)

name_space = api.namespace('streams', description="APIs to control data streams")


@app.route("/events", methods=['GET', 'POST'])
def show_events():
    if request.method == "GET":
        return render_template('index.html')
    elif request.form['submit'] == 'start_stream':
        celery.send_task('stream.start', kwargs={'channel_name': os.environ.get("PUBNUB_CHANNEL")})
        flash("Starting event stream")
    return redirect(url_for("show_events"))


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
 
