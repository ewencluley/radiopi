from threading import Thread
from flask import Flask, request, send_from_directory
import Clock
import Radio
import json
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app)


@app.route('/')
def send_index():
    return send_from_directory('static', 'index.html')


@app.route('/<path>')
def send_root(path):
    return send_from_directory('static', path)


@app.route('/js/<path>')
def send_js(path):
    return send_from_directory('static/js', path)


@app.route('/css/<path>')
def send_css(path):
    return send_from_directory('static/css', path)


@app.route('/images/<path>')
def send_img(path):
    return send_from_directory('static/images', path)


@app.route("/api/v1/alarm", methods=['POST'])
def set_alarm():
    def process_body(data):
        time = data['time']
        if not time:
            return
        return Clock.Alarm(
            hour=int(time.split(':')[0]),
            minute=int(time.split(':')[1]),
            day_of_week=data['daysOfWeek'],
            enabled=data['enabled'],
            duration_minutes=int(data['durationMinutes']),
            type=Clock.AlarmType(data['type'])
        )
    alarm = process_body(request.json)
    Clock.set_alarm(alarm)
    broadcast_state()
    return json.dumps({'status': 'OK'})


@app.route("/api/v1/alarm/stop", methods=['POST'])
def stop_alarm():
    try:
        if Clock.stop_alarm():
            return json.dumps({'status': 'OK'})
        return json.dumps({'status': 'ALARM_NOT_SOUNDING'}), 400
    finally:
        broadcast_state()


@app.route("/api/v1/radio/", methods=['PATCH'])
def set_radio():
    radio_on = request.json.get('radioOn', Radio.is_playing())
    if radio_on and not Radio.is_playing():
        Radio.play_radio()
    elif not radio_on and Radio.is_playing():
        Radio.stop()
    try:
        Radio.set_current_station(request.json.get('currentStation', Radio.state.current_station.url))
    except Radio.UnknownStationException as e:
        return json.dumps({'status': 'ERROR', 'message': e})

    volume = request.json.get('volume', Radio.get_volume())
    Radio.set_volume(int(volume))
    broadcast_state()
    return json.dumps({'status': 'OK'})


@socketio.on('connect')
def client_connect_event():
    print('client connected')
    broadcast_state()


def broadcast_state():
    alarm = Clock.get_alarm()
    state = {
        'time': Clock.get_datetime(),
        'alarm': {
            'time': f'{str(alarm.hour).zfill(2)}:{str(alarm.minute).zfill(2)}',
            'daysOfWeek': alarm.day_of_week,
            'enabled': alarm.enabled,
            'durationMinutes': alarm.duration_minutes,
            'isSounding': Clock.alarm_is_on(),
            'type': alarm.type.value
        },
        'radio': {
            'on': Radio.is_playing(),
            'stations': [{'name': s.name, 'url': s.url} for s in Radio.get_stations()],
            'currentStation': Radio.state.current_station.url,
            'volume': Radio.get_volume()
        }
    }
    socketio.emit('state_update', json.dumps(state))


@socketio.on('synchronize')
def synchronize_request(data):
    print('sync requested')
    broadcast_state()

def serve():
    # app.run(host="0.0.0.0", port=8000)
    socketio.run(app, host="0.0.0.0", port=8000)


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
