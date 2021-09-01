import librosa
import os

TEMPO = None

def get_beat_times():
    os.system("ffmpeg -i music musicA.wav")

    x, sr = librosa.load('musicA.wav')
    tempo, beat_times = librosa.beat.beat_track(x, sr=sr, start_bpm=60, units='time')

    set_tempo(tempo)

    beat_times_thirty = []

    for t in beat_times:
        if t > 30:
            break
        beat_times_thirty.append(t)
    
    os.remove("musicA.wav")

    print(beat_times_thirty)
    
    return beat_times_thirty

def set_tempo(tempo):
    TEMPO = tempo

def get_tempo():
    return TEMPO
