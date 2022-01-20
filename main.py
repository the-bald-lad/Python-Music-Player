from operator import index
import tkinter as t
from tkinter import TclError, filedialog
import pygame.mixer as mixer
from threading import Thread
import os
os.system("cls")

current = "N/A"
stop_threads = False
tracks = []
names = []


def play_song(song_name: t.StringVar, songs_list: t.Listbox, status: t.StringVar):
    global current, tracks, names
    if current not in ["Play", "Pause"]:
        song_name.set(names[0])
        names.remove(names[0])
        mixer.music.load(songs_list.get(t.ACTIVE))
        mixer.music.play()
        for i in tracks[:]:
            mixer.music.queue(i)
            tracks.remove(i)
        status.set("Song Playing")
        current = "Pause"
    elif current == "Play":
        print("Playing")
        current = "Pause"
        mixer.music.unpause()
        status.set("Song Playing")
    
def stop_song(status: t.StringVar):
    global current
    mixer.music.stop()
    print("Stopping")
    status.set("Song Stopped")
    current = "N/A"
    root.update()

def load(listbox, status: t.StringVar):
    global current, tracks, names
    listbox.delete(0, t.END)
    try:
        tracks.clear()
        os.chdir(filedialog.askdirectory(title='Please ensure files are encoded using the MP3 format!'))
        tracks = os.listdir()
        for track in tracks:
            listbox.insert(t.END, track)
        for track in tracks:
            names.append(track)
        status.set("Directory Loaded Successfully")
        print("Directory loaded")
        print(names)
    except OSError:
        status.set("Stopped Loading Directory")
        print(OSError)
        
def pause_song(status: t.StringVar):
    global current
    print(current)
    if current == "Pause":
        print("Pausing")
        current = "Play"
        mixer.music.pause()
        status.set("Song Paused")
    root.update()

def restart():
    stop_song(song_status)
    play_song(current_song, playlist, song_status)
    root.update()

def check(song_name: t.StringVar):
    global current, stop_threads
    while True:
        root.update()
        try:
            print(names[0], current)
            if not mixer.music.get_busy() and current == "Pause":
                song_name.set(names[0])
                names.remove(names[0])
            if stop_threads:
                break
        except IndexError:
            print("Empty directory")
        

def on_closing():
    root.destroy()

mixer.init()
root = t.Tk()
root.geometry('700x220')
root.title("Python Music Player")
root.resizable(0, 0)

font_ = "Comic Sans MS"

song_frame = t.LabelFrame(root, text='Now Playing:', bg='LightBlue', width=450, height=80)
song_frame.place(x=0, y=0)
control_frame = t.LabelFrame(root, text='Control Panel: ', bg='LightBlue', width=450, height=120)
control_frame.place(y=80)
playListbox_frame = t.LabelFrame(root, text='Up Next: ', bg='RoyalBlue')
playListbox_frame.place(x=450, y=0, height=200, width=250)
playlist = t.Listbox(playListbox_frame, font=(font_, 11), selectbackground='Gold')

scroll_bar = t.Scrollbar(playListbox_frame, orient=t.VERTICAL)
scroll_bar.pack(side=t.RIGHT, fill=t.BOTH)

playlist.config(yscrollcommand=scroll_bar.set)
scroll_bar.config(command=playlist.yview)
playlist.pack(fill=t.BOTH, padx=5, pady=5)

current_song = t.StringVar(root, value='No Song Playing')
song_status = t.StringVar(root, value='Please Load a Directory')

# SongFrame Labels
t.Label(song_frame, text='CURRENTLY PLAYING:', bg='LightBlue', font=(font_, 10, 'bold')).place(x=3, y=20)
song_lbl = t.Label(song_frame, textvariable=current_song, bg='Goldenrod', font=(font_, 12), width=25)
song_lbl.place(x=160, y=20)

# Buttons in the main screen
play_btn = t.Button(control_frame, text="Play", bg='Aqua', font=(font_, 13), width=7, command=lambda: play_song(current_song, playlist, song_status))
play_btn.place(x=15, y=10)
pause_btn = t.Button(control_frame, text='Pause', bg='Aqua', font=(font_, 13), width=7, command=lambda: pause_song(song_status))
pause_btn.place(x=105, y=10)
stop_btn = t.Button(control_frame, text='Stop', bg='Aqua', font=(font_, 13), width=7, command=lambda: stop_song(song_status))
stop_btn.place(x=195, y=10)
restart_btn = t.Button(control_frame, text='Restart', bg='Aqua', font=(font_, 13), width=7, command=lambda: restart())
restart_btn.place(x=285, y=10)
load_btn = t.Button(control_frame, text='Load Directory', bg='Aqua', font=(font_, 13), width=34, command=lambda: load(playlist, song_status))
load_btn.place(x=15, y=55)

t.Label(root, textvariable=song_status, bg='SteelBlue', font=(font_, 9), justify=t.LEFT).pack(side=t.BOTTOM, fill=t.X)

beans = Thread(target=check, args=(current_song, ))
beans.daemon = True 
beans.start()
root.protocol("WM_DELETE_WINDOW", on_closing)
root.update()
root.mainloop()
stop_threads = True