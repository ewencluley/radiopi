from threading import Thread
from flask import Flask, request, send_from_directory
import Clock
import json

app = Flask(__name__)


@app.route('/<path>')
def send_root(path):
    return send_from_directory('static', path)


@app.route('/js/<path>')
def send_js(path):
    return send_from_directory('static/js', path)


@app.route('/images/<path>')
def send_img(path):
    return send_from_directory('static/images', path)


@app.route("/api/v1/alarm", methods=['POST'])
def set_alarm():
    def process_body(data):
        time = data['time']
        if not time:
            return
        hour = int(time.split(':')[0])
        minute = int(time.split(':')[1])
        days_of_week = data['daysOfWeek']
        return Clock.Alarm(hour=hour, minute=minute, day_of_week=days_of_week)
    alarm = process_body(request.json)
    Clock.set_alarm(alarm)
    return f'Hello, Flask! {alarm}'


def serve():
    app.run(host="0.0.0.0", port=8000)


def start_in_background():
    server_thread = Thread(target=serve, daemon=True)
    server_thread.start()


def shutdown():
    print('Shutting down')
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()


if __name__ == "__main__":
    serve()
