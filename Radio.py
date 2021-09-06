import json
import subprocess
import logging
from collections import namedtuple
from json.decoder import JSONDecodeError
from threading import Thread

import os

from Volume import Volume

import alsaaudio
import random
import time

from Clock import AlarmType

Station = namedtuple("Station", "name url")
stations = {}
recent_count = 3

logging.basicConfig(level=logging.INFO)


def load_stations():
    logging.info("Loading stations")
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


def set_volume(volume):
    try:
        state.mixer.setvolume(volume)
    except NameError:
        print("Radio state not yet set")


class RadioState:
    def __init__(self):
        self.mixer = alsaaudio.Mixer('PCM')

        Volume(set_volume, self.mixer.getvolume()[0])
        self.triggered_by_alarm = False
        self.current_url = subprocess.check_output(f'mpc -f "%file%" playlist', shell=True, stderr=subprocess.STDOUT).decode("utf-8").strip()
        self.previous_stations = []
        if self.current_url and self.current_url in stations.keys():
            self.current_station = stations[self.current_url]
        else:
            self.current_station = list(stations.values())[0]

    def get_recent_stations(self):
        logging.info("all previous stations: %s", self.previous_stations)
        if len(self.previous_stations) > recent_count:
            logging.info("truncated previous stations: %s", self.previous_stations[-recent_count:])
            return set(self.previous_stations[-recent_count:])
        return set(self.previous_stations)

    def change_station(self, station):
        if station == self.current_station:
            return
        self.previous_stations.append(self.current_station)
        self.current_station = station


state = RadioState()


def is_playing() -> bool:
    try:
        playlist = subprocess.check_output('mpc status | grep playing', shell=True, stderr=subprocess.STDOUT)
        return bool(playlist)
    except subprocess.CalledProcessError:
        return False


def play():
    try:
        subprocess.check_output(f'mpc clear && mpc add {state.current_station.url} && mpc play', shell=True, stderr=subprocess.STDOUT)
        time.sleep(0.5)
        status = subprocess.getoutput(f'mpc status')
        if 'ERROR:' in status:
            return False
    except subprocess.CalledProcessError:
        print("Something went wrong while playing radio")
        return False
    return True


def play_radio(triggered_by_alarm=None):
    if triggered_by_alarm:
        logging.info("Playing radio from alarm")
        state.change_station(get_station_for_alarm(triggered_by_alarm))
    state.triggered_by_alarm = bool(triggered_by_alarm)
    return play()


def play_mp3(file):
    state.change_station(Station(os.path.basename(file), file))
    return play()


def get_station_for_alarm(alarm):
    logging.info("playing alarm %s", alarm.type)
    if alarm.type is AlarmType.RANDOM_RADIO:
        return get_random_unplayed_station()

    return state.current_station


def get_random_unplayed_station():
    excluded = state.get_recent_stations()
    logging.info("recently played stations: %s", excluded)
    station = get_random_station()
    attempts = 0
    while station in excluded and attempts < 10:
        logging.info("station '%s' played recently, try getting another", station.name)
        station = get_random_station()
        attempts += 1
    logging.info("settling on station '%s'", station.name)
    return station


def get_random_station():
    logging.info("Getting random station")
    return list(stations.values())[random.randrange(start=0, stop=len(stations))]


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
        state.change_station(stations[url])
        if is_playing():
            stop()
            play()
    except KeyError:
        raise UnknownStationException


def get_volume():
    return state.mixer.getvolume()[0]


def fadein(to_volume):
    def do_fadein():
        for i in range(0, to_volume):
            set_volume(i)
            time.sleep(0.2)
    Thread(target=do_fadein, daemon=True).start()


class UnknownStationException(Exception):
    def __init__(self, url):
        super().__init__(f'No radio station registered for {url}')
