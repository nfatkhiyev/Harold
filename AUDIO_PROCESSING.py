import librosa
import os

TEMPO = None

def get_beat_times():
    os.system("ffmpeg -ss 0 -t 30 -i music musicA.wav")

    x, sr = librosa.load('musicA.wav')
    tempo, beat_times = librosa.beat.beat_track(x, sr=sr, start_bpm=60, units='time')

    set_tempo(tempo)

    beat_times_thirty = []

    for t in beat_times:
        if t > 30:
            break
        beat_times_thirty.append(t)
    
    os.remove("musicA.wav")

    double_beat_array = [beat_times_thirty[0]]
    for beat in range(0,len(beat_times_thirty)-1):
        average = (beat_times_thirty[beat]+beat_times_thirty[beat+1])/2
        double_beat_array.append(average)
        double_beat_array.append(beat_times_thirty[beat+1])

    quad_beat_array = [double_beat_array[0]]
    for beat in range(0,len(double_beat_array)-1):
        average = (double_beat_array[beat]+double_beat_array[beat+1])/2
        quad_beat_array.append(average)
        quad_beat_array.append(double_beat_array[beat+1])

    print(beat_times_thirty)
    
    return quad_beat_array

def set_tempo(tempo):
    TEMPO = tempo

def get_tempo():
    return TEMPO
