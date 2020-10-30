import json
import subprocess
from collections import namedtuple
from json.decoder import JSONDecodeError
import alsaaudio
import random

from Clock import AlarmType

Station = namedtuple("Station", "name url")
stations = {}


def load_stations():
    try:
        with open("stations.json", "r") as f:
            for s in json.loads(f.read()):
                station = Station(**s)
                stations[station.url] = station
    except FileNotFoundError or TypeError or JSONDecodeError:
        default_station = Station(name='BBC 6 Music',
                                  url='http://a.files.bbci.co.uk/media/live/manifesto/audio/simulcast/hls/uk/sbr_high/llnw/bbc_6music.m3u8')
        stations[default_station.url] = default_station
    print(stations)


load_stations()


class RadioState:
    mixer = alsaaudio.Mixer('PCM')
    triggered_by_alarm = False
    current_url = subprocess.check_output(f' mpc -f "%file%" playlist', shell=True, stderr=subprocess.STDOUT).decode("utf-8").strip()
    if current_url:
        current_station = stations[current_url]
    else:
        current_station = list(stations.values())[0]


state = RadioState()


def is_playing() -> bool:
    try:
        playlist = subprocess.check_output('mpc status | grep playing', shell=True, stderr=subprocess.STDOUT)
        return bool(playlist)
    except subprocess.CalledProcessError:
        return False


def play(triggered_by_alarm=None):
    try:
        if triggered_by_alarm:
            state.current_station = get_station_for_alarm(triggered_by_alarm)
        state.triggered_by_alarm = bool(triggered_by_alarm)
        subprocess.check_output(f'mpc clear && mpc add {state.current_station.url} && mpc play', shell=True, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError:
        print("Something went wrong while playing radio")


def get_station_for_alarm(alarm):
    if alarm.type is AlarmType.RANDOM_RADIO:
        return list(stations.values())[random.randrange(start=0, stop=len(stations))]
    return state.current_station


def stop():
    try:
        subprocess.check_output(f'mpc stop && mpc clear', shell=True, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError:
        print("Something went wrong while stopping radio")


def was_triggered_by_alarm():
    return state.triggered_by_alarm


def get_stations():
    return list(stations.values())


def set_current_station(url):
    try:
        if state.current_station.url == url:
            return
        state.current_station = stations[url]
        if is_playing():
            stop()
            play()
    except KeyError:
        raise UnknownStationException


def get_volume():
    return state.mixer.getvolume()[0]


def set_volume(volume):
    state.mixer.setvolume(volume)


class UnknownStationException(Exception):
    def __init__(self, url):
        super().__init__(f'No radio station registered for {url}')
