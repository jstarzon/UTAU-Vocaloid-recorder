import pandas as pd
import os
import pyaudio
import wave

def skipped(word, skipped_words):
    skipped_words.append(word)
    print("Word successfully added to queue:", word)

def mic_rec(sound):
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 44100
    RECORD_SECONDS = 3
    WAVE_OUTPUT_FILENAME = sound + ".wav"

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("* recording")

    frames = []

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("* done recording")

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

    print("Sound has been recorded and saved as", WAVE_OUTPUT_FILENAME)

def record_sound(sound):
    answer = input("Record? (yes/no)")
    if answer == "yes":
        mic_rec(sound)
    elif answer == "no":
        print("No sound will be recorded.")
        print("Skipping...")
        skipped(sound)
    else:
        print("Invalid input, please enter 'yes' or 'no'.")
        record_sound(sound)

skipped_words = []  
phonemes = [
    ('/p/', 'pat'), ('/b/', 'bat'), ('/t/', 'top'), ('/d/', 'dog'),
    ('/k/', 'cat'), ('/g/', 'go'), ('/f/', 'fat'), ('/v/', 'van'),
    ('/θ/', 'think'), ('/ð/', 'this'), ('/s/', 'sat'), ('/z/', 'zoo'),
    ('/ʃ/', 'she'), ('/ʒ/', 'measure'), ('/h/', 'hat'),
    ('/m/', 'mat'), ('/n/', 'not'), ('/ŋ/', 'sing'), ('/l/', 'look'),
    ('/r/', 'run'), ('/j/', 'yes'), ('/w/', 'wet'),
    ('/i/', 'eat'), ('/ɪ/', 'bit'), ('/ɛ/', 'bet'), ('/æ/', 'bat'),
    ('/aɪ/', 'bite'), ('/ɔɪ/', 'boy'), ('/əʊ/', 'boat'),
    ('/ʊ/', 'put'), ('/u/', 'boot'), ('/ɑ/', 'bot'), ('/ɔ/', 'bought'),
    ('/ɒ/', 'cot'), ('/ɜ/', 'burn')
]

diphones = [
    ('/pɪ/', 'pit'), ('/bɪ/', 'bit'), ('/tɪ/', 'tip'), ('/dɪ/', 'dip'),
    ('/kɪ/', 'kit'), ('/gɪ/', 'git'), ('/fɪ/', 'fit'), ('/vɪ/', 'vit'),
    ('/θɪ/', 'thick'), ('/ðɪ/', 'thick'), ('/sɪ/', 'sit'), ('/zɪ/', 'zip'),
    ('/ʃɪ/', 'sheet'), ('/ʒɪ/', 'measurement'), ('/hɪ/', 'hit'),
    ('/mɪ/', 'mit'), ('/nɪ/', 'nit'), ('/ŋɪ/', 'sing'), ('/lɪ/', 'lit'),
    ('/rɪ/', 'rit'), ('/jɪ/', 'jit'), ('/wɪ/', 'wit'),
    ('/ɪi/', 'eat'), ('/ɪɪ/', 'bit'), ('/ɛɪ/', 'beat'), ('/æɪ/', 'bat'),
    ('/aɪɪ/', 'bite'), ('/ɔɪɪ/', 'boy'), ('/əʊɪ/', 'boat'),
    ('/ʊɪ/', 'put'), ('/uɪ/', 'boot'), ('/ɑɪ/', 'buy'), ('/ɔɪ/', 'boy'),
    ('/ɒɪ/', 'coin'), ('/ɜɪ/', 'burn')
]

phonemes_df = pd.DataFrame(phonemes, columns=['Phoneme', 'Example'])
diphones_df = pd.DataFrame(diphones, columns=['Diphone', 'Example'])

for i, row in phonemes_df.iterrows():
    print(f"Phoneme: {row['Phoneme']}, Example: {row['Example']}")
    record_sound(row['Example'])
    
for i, row in diphones_df.iterrows():
    print(f"Diphone: {row['Diphone']}, Example: {row['Example']}")
    record_sound(row['Example'])
    
for word in skipped_words:
    record_sound(skipped_words)