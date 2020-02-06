#!/usr/bin/python3
# Imports
from tkinter import *
from pygame import mixer
import os
import random
import eyed3
import requests

# Variables
wind_x = 500
wind_y = 500
music_path = "/home/user/Music/"
song_list = []
site = "" # the site to post your data to
play_status = 0


# define events
def end_program():
    root.quit()


def play_music():
    global play_status
    play_status = 1
    mixer.music.play()


def pause_music():
    mixer.music.pause()


def resume_music():
    mixer.music.unpause()


def stop_music():
    global play_status
    play_status = 0
    mixer.music.stop()


def get_songs():
    global song_list, music_path
    song_list = os.listdir(music_path)
    pick_song()


def pick_song():
    global song_list, music_path, site
    mixer.music.stop()
    random.seed()
    x = random.randint(0, len(song_list)-1)
    mixer.music.load(music_path + song_list[x])
    lab_path.config(text=music_path + song_list[x])

    try:
        audio = eyed3.load(music_path + song_list[x])
        song = audio.tag.title
        artist = audio.tag.artist
        album = audio.tag.album
    except:
        song = song_list[x][:-4]
        artist = "N/A"
        album = "N/A"

    lab_song.config(text="Title: "+song)
    lab_artist.config(text="Artist: " + artist)
    try:
        lab_album.config(text="Album: " + album)
    except:
        lab_album.config(text="Album: Unknown")
    # update website
    my_object = {
        's1': artist,
        's2': album,
        's3': song
    }
    try:
        z = requests.get(site+"?s1="+artist+"&s2="+album+"&s3="+song)
    except:
        z = 0

def song_stat():
    global play_status
    if play_status == 1:
        if mixer.music.get_busy():
            lab_status.config(text="Song Playing")
        else:
            pick_song()
            mixer.music.play()

    root.after(1000, song_stat)

# Mixer Elements
mixer.init()

# define widgets
# window
root = Tk()
root.title("Main Window")

# labels
lab_title = Label(root, text="Generic Music Player")
lab_path = Label(root, text=music_path)
lab_song = Label(root, text="")
lab_artist = Label(root, text="")
lab_album = Label(root, text="")
lab_status = Label(root, text="")

# buttons
button01 = Button(root, text="Play", padx=50, command=play_music)
button03 = Button(root, text="Pause", padx=50, command=pause_music)
button04 = Button(root, text="Resume", padx=50, command=resume_music)
button05 = Button(root, text="stop", padx=50, command=stop_music)
button06 = Button(root, text="New Song", padx=50, command=pick_song)
button02 = Button(root, text="Exit", padx=50, command=end_program)


# place widgets
lab_title.grid(row=0, columnspan=4)
button01.grid(row=1, column=0)
button03.grid(row=1, column=1)
button04.grid(row=1, column=2)
button05.grid(row=1, column=3)
lab_path.grid(row=2, column=0, columnspan=4)
lab_song.grid(row=3, column=0, columnspan=4)
lab_artist.grid(row=4, column=0, columnspan=4)
lab_album.grid(row=5, column=0, columnspan=4)
lab_status.grid(row=6, column=0, columnspan=4)
button06.grid(row=7, column=0, columnspan=2)
button02.grid(row=7, column=2, columnspan=2)

get_songs()

# Main Loop
root.after(1000, song_stat)
root.mainloop()

# Exit Operations
