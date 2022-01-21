import os
import threading
import time
import tkinter.messagebox
from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from ttkthemes import themed_tk as tk
from mutagen.mp3 import MP3
from pygame import mixer

root = tk.ThemedTk()
root.get_themes()
root.set_theme("radiance")

statusbar = ttk.Label(root, text="Not Playing", relief=SUNKEN, anchor=W, font='Helvetica 10 italic')
statusbar.pack(side=BOTTOM, fill=X)

menubar = Menu(root)
root.config(menu=menubar)

subMenu = Menu(menubar, tearoff=0)
subMenu2 = Menu(menubar, tearoff=0)

playlist = []


def browse_file():
    global filename_path
    filename_path = filedialog.askopenfilename()
    add_to_playlist(filename_path)

    mixer.music.queue(filename_path)


def browse_dir():
    global filename_path
    path_of_the_directory = filedialog.askdirectory(title='Open a songs directory')
    for filename in os.listdir(path_of_the_directory)[::-1]:
        filename_path = os.path.join(path_of_the_directory, filename)
        add_to_playlist(filename_path)
        mixer.music.queue(filename_path)
            

def add_to_playlist(filename):
    filename = os.path.basename(filename)
    index = 0
    playlistbox.insert(index, filename)
    playlist.insert(index, filename_path)
    index += 1

def del_song():
    try:
        selected_song = playlistbox.curselection()
        selected_song = int(selected_song[0])
        playlistbox.delete(selected_song)
        playlist.pop(selected_song)
    except IndexError:
        tkinter.messagebox.showerror('No Song Selected', 'Please select a song from the menu on the left to delete.')

def del_songs():
    playlistbox.delete(0, len(playlist))
    playlist.clear()

def help():
    tkinter.messagebox.showinfo("Help", "+ Add -> This adds one song to the playlist\n+ AddDir -> This adds all songs from a given directory\n- Del -> This removes the selected song from the playlist.")
   
def about():
    tkinter.messagebox.showinfo("About", "This is a small project that is published at https://github.com/the-bald-lad/Python-Music-Player.\n It was made in my spare time and is probably full of bugs.")

menubar.add_cascade(label="File", menu=subMenu)
menubar.add_cascade(label="Help", menu=subMenu2)
menubar.add_cascade(label="Exit", command=root.destroy)
subMenu.add_command(label="Add Song", command=browse_file)
subMenu.add_command(label="Remove All Songs", command=del_songs)
subMenu2.add_command(label="Help about buttons", command=help)
subMenu2.add_command(label="About", command=about)

subMenu = Menu(menubar, tearoff=0)

mixer.init()

root.title("Python Music Player")

leftframe = Frame(root)
leftframe.pack(side=LEFT, padx=30, pady=30)

playlistbox = Listbox(leftframe, width=46)
playlistbox.pack()

addBtn = ttk.Button(leftframe, text="+ Add", command=browse_file)
addBtn.pack(side=LEFT)

addDirBtn = ttk.Button(leftframe, text="+ AddDir", command=browse_dir)
addDirBtn.pack(side=LEFT)

delBtn = ttk.Button(leftframe, text="- Del", command=del_song)
delBtn.pack(side=LEFT)

rightframe = Frame(root)
rightframe.pack(pady=30)

topframe = Frame(rightframe)
topframe.pack()

currenttimelabel = ttk.Label(topframe, text='Current Time : --:--')
currenttimelabel.pack()

lengthlabel = ttk.Label(topframe, text='Total Length : --:--')
lengthlabel.pack(pady=5)


def show_details(play_song):
    file_data = os.path.splitext(play_song)

    if file_data[1] == '.mp3':
        audio = MP3(play_song)
        total_length = audio.info.length
    else:
        a = mixer.Sound(play_song)
        total_length = a.get_length()

    mins, secs = divmod(total_length, 60)
    mins = round(mins)
    secs = round(secs)
    timeformat = '{:02d}:{:02d}'.format(mins, secs)
    lengthlabel['text'] = "Total Length" + ' - ' + timeformat

    t1 = threading.Thread(target=start_count, args=(total_length,))
    t1.start()


def start_count(t):
    global paused
    current_time = 0
    while current_time <= t and mixer.music.get_busy():
        if paused:
            continue
        else:
            mins, secs = divmod(current_time, 60)
            mins = round(mins)
            secs = round(secs)
            timeformat = '{:02d}:{:02d}'.format(mins, secs)
            currenttimelabel['text'] = "Current Time" + ' - ' + timeformat
            time.sleep(1)
            current_time += 1


def play_music():
    global paused
    if paused:
        mixer.music.unpause()
        statusbar['text'] = "Music Resumed"
        paused = FALSE
    else:
        try:
            stop_music()
            time.sleep(1)
            selected_song = playlistbox.curselection()
            selected_song = int(selected_song[0])
            play_it = playlist[selected_song]
            mixer.music.load(play_it)
            mixer.music.play()
            statusbar['text'] = "Playing music" + ' - ' + os.path.basename(play_it)
            show_details(play_it)
        except IndexError:
            tkinter.messagebox.showerror('File not found', 'Please select a song from the menu on the left to play.')

paused = FALSE
muted = FALSE


def stop_music():
    mixer.music.stop()
    statusbar['text'] = "Music Stopped"

def pause_music():
    global paused
    paused = TRUE
    mixer.music.pause()
    statusbar['text'] = "Music Paused"

def rewind_music():
    play_music()
    statusbar['text'] = "Music Rewinded"

def set_vol(val):
    volume = float(val) / 100
    mixer.music.set_volume(volume)

def mute_music():
    global muted
    if muted:
        mixer.music.set_volume(0.7)
        volumeBtn.configure(text="Mute")
        scale.set(70)
        muted = FALSE
    else:
        mixer.music.set_volume(0)
        volumeBtn.configure(text="Unmute")
        scale.set(0)
        muted = TRUE


middleframe = Frame(rightframe)
middleframe.pack(pady=30, padx=30)

playBtn = ttk.Button(middleframe, text="Play", command=play_music)
playBtn.grid(row=0, column=0, padx=10)

stopBtn = ttk.Button(middleframe, text="Stop", command=stop_music)
stopBtn.grid(row=0, column=1, padx=10)

pauseBtn = ttk.Button(middleframe, text="pause", command=pause_music)
pauseBtn.grid(row=0, column=2, padx=10)

bottomframe = Frame(rightframe)
bottomframe.pack()

rewindBtn = ttk.Button(bottomframe, text="Rewind", command=rewind_music)
rewindBtn.grid(row=0, column=0)

volumeBtn = ttk.Button(bottomframe, text="Mute", command=mute_music)
volumeBtn.grid(row=0, column=1)

scale = ttk.Scale(bottomframe, from_=0, to=100, orient=HORIZONTAL, command=set_vol)
scale.set(70)
mixer.music.set_volume(0.7)
scale.grid(row=0, column=2, pady=15, padx=30)


def on_closing():
    stop_music()
    root.destroy()


root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()