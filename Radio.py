import subprocess

URL = 'http://a.files.bbci.co.uk/media/live/manifesto/audio/simulcast/hls/uk/sbr_high/llnw/bbc_6music.m3u8'

class RadioState:
    triggered_by_alarm = False


state = RadioState()


def is_playing() -> bool:
    try:
        playlist = subprocess.check_output('mpc status | grep playing', shell=True, stderr=subprocess.STDOUT)
        return bool(playlist)
    except subprocess.CalledProcessError:
        return False


def play(triggered_by_alarm=False):
    state.triggered_by_alarm = triggered_by_alarm
    subprocess.check_output(f'mpc clear && mpc add {URL} && mpc play', shell=True, stderr=subprocess.STDOUT)


def stop():
    subprocess.check_output(f'mpc stop && mpc clear', shell=True, stderr=subprocess.STDOUT)


def was_triggered_by_alarm():
    return state.triggered_by_alarm