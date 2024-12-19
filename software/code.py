# SPDX-FileCopyrightText: 2024 Becky Stern
# SPDX-License-Identifier: MIT

# PS4 Controller Sequencer based on:
# Breakbeat Breadboard by John Park for Adafruit Industries - https://learn.adafruit.com/breakbeat-breadboard
# and
# @todbot / Tod Kurt - https://github.com/todbot/plinkykeeb
# Convert files to appropriate WAV format (mono, 22050 Hz, 16-bit signed) with command:
#  sox loop.mp3 -b 16 -c 1 -r 22050 loop.wav
# put samples in "/wav" folder
print("PS4 Controller Sequencer!")
import time
import board
import keypad
import audiocore
import audiomixer
from audiopwmio import PWMAudioOut as AudioOut

# wait a little bit so USB can stabilize and not glitch audio
time.sleep(3)

# list of (samples to play, mixer gain level)
loop_wav_files = (
    ('wav/loop_10.wav', 0.4),
    ('wav/mfos.wav', 1.0),
)

oneshot1 = audiocore.WaveFile(open('wav/clap_002.wav',"rb"))
oneshot2 = audiocore.WaveFile(open('wav/orchestra_hit.wav',"rb"))
oneshot3 = audiocore.WaveFile(open('wav/vectrex_2.wav',"rb"))
oneshot4 = audiocore.WaveFile(open('wav/test_016.wav',"rb"))
oneshot5 = audiocore.WaveFile(open('wav/alarm.wav',"rb"))
oneshot6 = audiocore.WaveFile(open('wav/crash.wav',"rb"))
oneshot7 = audiocore.WaveFile(open('wav/cthulu.wav',"rb"))
oneshot8 = audiocore.WaveFile(open('wav/tom_001.wav',"rb"))
oneshot9 = audiocore.WaveFile(open('wav/tom_002.wav',"rb"))
oneshot10 = audiocore.WaveFile(open('wav/tom_003.wav',"rb"))
oneshot11 = audiocore.WaveFile(open('wav/tom_004.wav',"rb"))
oneshot12 = audiocore.WaveFile(open('wav/cat.wav',"rb"))




# pins used by keyboard
KEY_PINS = (
            
            board.MISO, # Trackpad button
            board.A1, # PS button
            
            board.D9, # Right joystick button
            board.RX, # L1
            board.A3, # R1
            board.D2, # Square
            board.D3, # Triangle
            board.A2, # O
            board.D4, # X
            board.D5, # D pad down
            board.D6, # D pad right
            board.TX, # D pad left
            board.A0, # D pad up
            board.MOSI # Left joystick button
            
)

km = keypad.Keys( KEY_PINS, value_when_pressed=False, pull=True)

audio = AudioOut( board.D10 )  # RP2040 PWM, use RC filter on breadboard
mixer = audiomixer.Mixer(voice_count=len(KEY_PINS), sample_rate=22050, channel_count=1,
                         bits_per_sample=16, samples_signed=True)
audio.play(mixer) # attach mixer to audio playback

for i in range(len(loop_wav_files)):  # start all samples at once for use w handle_mixer
    wave = audiocore.WaveFile(open(loop_wav_files[i][0],"rb"))
    mixer.voice[i].play(wave, loop=True)
    mixer.voice[i].level = 0

def handle_mixer(num, pressed):
    voice = mixer.voice[num]   # get mixer voice

    if num < len(loop_wav_files):
        if pressed:
            if mixer.voice[num].level == 0:
                voice.level = loop_wav_files[num][1]  # play at level in wav_file list
            elif mixer.voice[num].level > 0:
                voice.level = 0  # mute it
   #     else:
   #         voice.level = 0  # mute it
    elif num == len(loop_wav_files):
        if pressed:
            mixer.voice[num].play(oneshot1)
    elif num == len(loop_wav_files)+1:
        if pressed:
            mixer.voice[num].play(oneshot2)
    elif num == len(loop_wav_files)+2:
        if pressed:
            mixer.voice[num].play(oneshot3)
    elif num == len(loop_wav_files)+3:
        if pressed:
            mixer.voice[num].play(oneshot4)
    elif num == len(loop_wav_files)+4:
        if pressed:
            mixer.voice[num].play(oneshot5)
    elif num == len(loop_wav_files)+5:
        if pressed:
            mixer.voice[num].play(oneshot6)
    elif num == len(loop_wav_files)+6:
        if pressed:
            mixer.voice[num].play(oneshot7)
    elif num == len(loop_wav_files)+7:
        if pressed:
            mixer.voice[num].play(oneshot8)
    elif num == len(loop_wav_files)+8:
        if pressed:
            mixer.voice[num].play(oneshot9)
    elif num == len(loop_wav_files)+9:
        if pressed:
            mixer.voice[num].play(oneshot10)
    elif num == len(loop_wav_files)+10:
        if pressed:
            mixer.voice[num].play(oneshot11)
    elif num == len(loop_wav_files)+11:
        if pressed:
            mixer.voice[num].play(oneshot12)
            
        


while True:
    event = km.events.get()
    if event:
        if event.key_number < len(KEY_PINS):
            if event.pressed:
                handle_mixer(event.key_number, True)
            if event.released:
                handle_mixer(event.key_number, False)
