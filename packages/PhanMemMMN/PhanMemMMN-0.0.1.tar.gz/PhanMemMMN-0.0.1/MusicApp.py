
from tkinter import filedialog, messagebox
from tkinter import *
from PIL import Image, ImageTk
import threading
import os
import time
import pygame
import customtkinter
import random

root = customtkinter.CTk(fg_color="#36454F")
root.title('Music Player')
root.geometry("400x500")

pygame.mixer.init()

menubar= Menu(root)
root.config(menu=menubar)


songs= []
current_song = ''
paused = False
repeat = False
flag = False
progress_thread = None
stop_progress = False


def load_music():
    global  current_song
    songs.clear()
    songList.delete(0, END)
    try:
        root.directory = filedialog.askdirectory()
        for song in os.listdir(root.directory):
            name, ext = os.path.splitext(song)
            if ext == '.mp3':
                songs.append(song)

        for song in songs:
            songList.insert("end",song)

        songList.select_set(0)
        current_song = songs[songList.curselection()[0]]
    except IndexError:
        messagebox.showinfo("Alert", "Thu muc nay khong co bai hat")

def cal_songLength(length): # tinh thoi gian cho bai hat theo dinh dang 0:00
    duration_minutes = length / 60
    total_seconds = int(duration_minutes * 60)
    minutes, seconds = divmod(total_seconds, 60)
    time_label_end.configure(text=f"{minutes}:{seconds:02d}")

def play_music():
    global current_song, paused, song_length,progress_thread,flag,stop_progress
    flag = False
    try:
        if not paused:

            pygame.mixer.music.load(os.path.join(root.directory, current_song))
            pygame.mixer.music.play()

            sound = pygame.mixer.Sound(os.path.join(root.directory, current_song))
            song_length = sound.get_length()
            cal_songLength(song_length)

            if progress_thread is None or not progress_thread.is_alive():
                progress_thread = threading.Thread(target=update_progress)
                progress_thread.start()


            play_btn.grid_forget()
            pause_btn.grid(row=0, column=2, padx=7, pady=10)
        else:
            play_btn.grid_forget()
            pause_btn.grid(row=0, column=2, padx=7, pady=10)
            pygame.mixer.music.unpause()
            paused = False

    except (AttributeError, IndexError):
        messagebox.showinfo("Alert", "Chon thu muc co chua bai hat")

def pause_music():
    global paused
    pygame.mixer.music.pause()
    paused = True

    pause_btn.grid_forget()
    play_btn.grid(row=0, column=2, padx=7, pady=10)

def next_music():
    global current_song,paused,repeat
    try:
        if repeat :
            play_music()
        else:
            songList.select_clear(0, END)
            if songs.index(current_song) == len(songs) - 1 :
                songList.select_set(0)  # select the first item
            else :
                songList.select_set(songs.index(current_song) + 1)  # select the next item
            current_song = songs[songList.curselection()[0]]
            play_music()
    except:
        pass
def prev_music():
    global current_song, paused
    try :
        songList.select_clear(0, END)
        songList.select_set(songs.index(current_song) - 1)
        current_song = songs[songList.curselection()[0]]
        play_music()
    except :
        pass
def repeat_music():
    global repeat
    if repeat :
        repeat = False
        repeat_btn.configure(image=repeat_btn_image)
    else:
        repeat = True
        repeat_btn.configure(image=repeat1_btn_image)
def shuffle_music():
    global songs, current_song
    random.shuffle(songs)
    songList.delete(0, END)
    for song in songs :
        songList.insert("end", song)
    songList.select_set(0)
    current_song = songs[songList.curselection()[0]]
def on_select(event):
    global current_song,paused
    selection = songList.curselection()

    if selection :
        if paused :
            paused=FALSE
            current_song = songs[selection[0]]
            play_music()
        else:
            current_song = songs[selection[0]]
            play_music()
    else :
        print("Nothing is selected")

def update_progress():
    global flag,new_position,paused
    # khi set thoi gian bai hat
    # Get the total length of the music in milliseconds
    total_length = song_length * 1000
    while not stop_progress:
        while pygame.mixer.music.get_busy():

                    if not flag :
                    # Get the current position of the music in milliseconds
                        current_position = pygame.mixer.music.get_pos()

                        current_time = time.strftime("%M:%S", time.gmtime(current_position // 1000))
                        # Calculate the progress of the music as a percentage
                        progress_percent = current_position / total_length

                        # Update the value of the music progress bar
                        progressbar.set(progress_percent)
                        time_label_start.configure(text=current_time)

                        # Wait for a short period of time before updating again
                        pygame.time.delay(1000)
                    else:
                        current_position = new_position * 1000
                        current_time = time.strftime("%M:%S", time.gmtime(current_position // 1000))
                        # Calculate the progress of the music as a percentage
                        progress_percent = current_position / total_length
                        progressbar.set(progress_percent)

                        # Update the value of the music progress bar
                        time_label_start.configure(text=current_time)
                        new_position +=1

                        pygame.time.delay(1000)
        next_music()

def on_click_progress_change(event):
    global flag,new_position,stop_progress
    new_position = 0
    flag =True
    x = event.x
    new_position =int(x / progressbar.winfo_width() * song_length)
    # Set the position of the music
    pygame.mixer.music.rewind()
    pygame.mixer.music.play(start=new_position)
def on_click_volume_change(event):
    x = event.x
    percent = x / volumnbar.winfo_width()
    volumnbar.set(percent)
    print(percent)
    pygame.mixer.music.set_volume(percent)


organise_menu = Menu(menubar,tearoff = False)
organise_menu.add_command(label='Select Folder', command=load_music)
menubar.add_cascade(label='Organise',menu=organise_menu)

songList=Listbox(root,bg='black',fg='white',width=200,height=15)
songList.pack()
songList.bind("<<ListboxSelect>>", on_select)


play_btn_image = customtkinter.CTkImage(light_image=Image.open("img/play-button1.png"),size=(40,40))
pause_btn_image = customtkinter.CTkImage(light_image=Image.open("img/pause.png"),size=(40,40))
next_btn_image = customtkinter.CTkImage(light_image=Image.open("img/next-button.png"),size=(40,40))
previous_btn_image= customtkinter.CTkImage(light_image=Image.open("img/previous.png"),size=(40,40))
repeat_btn_image = customtkinter.CTkImage(light_image=Image.open("img/repeat.png"),size=(40,40))
repeat1_btn_image = customtkinter.CTkImage(light_image=Image.open("img/repeat-one.png"),size=(40,40))
shuffle_btn_image =customtkinter.CTkImage(light_image=Image.open("img/shuffle.png"),size=(40,40))

control_frame = customtkinter.CTkFrame(master=root,fg_color="#36454F")
control_frame.pack()

play_btn = customtkinter.CTkButton(master=control_frame,width=40,text="",image=play_btn_image,command=play_music,fg_color="#36454F",hover=False)
pause_btn = customtkinter.CTkButton(master=control_frame,width=40,text="",image=pause_btn_image,command=pause_music,fg_color="#36454F",hover=False)
next_btn = customtkinter.CTkButton(master=control_frame,width=40,text="",image=next_btn_image,command=next_music,fg_color="#36454F",hover=False)
prev_btn = customtkinter.CTkButton(master=control_frame,width=40,text="",image=previous_btn_image,command=prev_music,fg_color="#36454F",hover=False)
repeat_btn =customtkinter.CTkButton(master=control_frame,width=40,text="",image=repeat_btn_image,command=repeat_music,fg_color="#36454F",hover=False)
shuffle_btn =customtkinter.CTkButton(master=control_frame,width=40,text="",image=shuffle_btn_image,command=shuffle_music,fg_color="#36454F",hover=False)

play_btn.grid(row=0,column=2,padx=7,pady=10)
next_btn.grid(row=0,column=3,padx=7,pady=10)
prev_btn.grid(row=0,column=1,padx=7,pady=10)
repeat_btn.grid(row=0,column=4,padx=7,pady=10)
shuffle_btn.grid(row=0,column=0,padx=7,pady=10)


musicbar_frame = customtkinter.CTkFrame(master=root)
musicbar_frame.pack()

#music_bar = MusicBar(musicbar_frame, bg="white", fg="#87CEEB", width=300, height=10)
progressbar = customtkinter.CTkProgressBar(master=musicbar_frame,width=250, height=10,progress_color="#87CEEB")
progressbar.pack(padx=20, pady=10)
progressbar.set(0)
progressbar.bind("<Button-1>", on_click_progress_change)

time_label_start = customtkinter.CTkLabel(master=musicbar_frame,text="0:00")
time_label_end = customtkinter.CTkLabel(master=musicbar_frame,text="0:00")

progressbar.grid(row=0,column=1,padx=7,pady=10)
time_label_start.grid(row=0,column=0,padx=7,pady=10)
time_label_end.grid(row=0,column=2,padx=7,pady=10)

volumnframe=customtkinter.CTkFrame(master=root,fg_color="#36454F")
volumnframe.pack(pady = 10)
volumn_picture = customtkinter.CTkImage(light_image=Image.open("img/low-volume.png"),size=(40,40))
volumn_btn = customtkinter.CTkButton(master=volumnframe,width=40,text="",image=volumn_picture,command=play_music,fg_color="#36454F",hover=False)
volumn_btn.grid(row=1,column=0)
volumnbar = customtkinter.CTkProgressBar(master=volumnframe,width=100, height=5,progress_color="#87CEEB")
volumnbar.grid(row=1,column=1)
volumnbar.bind("<Button-1>", on_click_volume_change)

root.mainloop()
