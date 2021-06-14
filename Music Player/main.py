import pygame
import os
import time
import threading
import timeit
from tkinter import *
from tkinter import ttk
from tkinter.filedialog import *
from tkinter.tix import *
from PIL import Image, ImageTk

pygame.mixer.init()

class Song:
    def __init__(self, name, next=None, prev=None):
        self.name = name
        self.next = next
        self.prev = prev


class Player:
    def __init__(self, master):
        self.master = master
        self.paused = False
        self.showing_volume = False
        self.song_queue = []
        self.changed_song = False
        self.canvas = Canvas(self.master, width=800, height=500, bg='black')
        self.canvas.pack()
        self.draw_layout()
    #--------------------------------------------------------------------------------------------------------------------------------------

    def draw_layout(self):
        self.canvas.create_rectangle(5, 440, 795, 495, fill='white', outline='blue', width=4)
        i = Image.open('Assets/audioicon.png')
        i.thumbnail((50, 50))
        img = ImageTk.PhotoImage(i)
        Label(image=img, bg='black').place(x=375,  y=215)

        # Volume button
        s = Image.open('Assets/speaker.png')
        speaker_img = ImageTk.PhotoImage(s, size=5)
        self.volume_btn = Button(self.master, image=speaker_img, bg='#01a6fe', font='Verdana 24', bd=4,
                                state=DISABLED, command=self.volume_slider)
        self.volume_btn.place(x=749, y=450)

        # Pause button
        p = Image.open('Assets/pause.png')
        p.thumbnail((50, 45))
        self.pause_icon = ImageTk.PhotoImage(p)
        pl = Image.open('Assets/play.png')
        pl.thumbnail((50, 45))
        self.play_icon = ImageTk.PhotoImage(pl)
        self.pause_play_btn = Button(self.master, image=self.pause_icon, font='Verdana 32', bg='white',
                                relief=FLAT, command=self.control_pause, state=DISABLED)
        self.pause_play_btn.place(x=377, y=442)
        
        #Previous button
        pr = Image.open('Assets/back.png')
        pr.thumbnail((50, 45))
        previous_icon = ImageTk.PhotoImage(pr)
        self.prev_btn = Button(self.master, image=previous_icon, font='Verdana 32', bg='white',
                         relief=FLAT, command=self.prev_song, state=DISABLED)
        self.prev_btn.place(x=327, y=442)

        # Next button
        ne = Image.open('Assets/next.png')
        ne.thumbnail((50, 45))
        next_icon = ImageTk.PhotoImage(ne)
        self.next_btn = Button(self.master, image=next_icon, font='Verdana 32', bg='white',
                         relief=FLAT, command=self.next_song, state=DISABLED)
        self.next_btn.place(x=427, y=442)

        # Open Button
        op = Image.open('Assets/open.png')
        op.thumbnail((50, 45))
        op_icon = ImageTk.PhotoImage(op)
        op_btn = Button(self.master, image=op_icon, font='Verdana 32', bg='white',
                        relief=FLAT, command=self.load)
        op_btn.place(x=10, y=442)

        tip = Balloon(self.master)
        tip.bind_widget(op_btn, balloonmsg='Open Audio File(s)')
        self.master.update()
        self.load()
        self.master.mainloop()
    #------------------------------------------------------------------------------------------------------------------------------------------
    
    def seekThread(self, seek_pos, seekdist, curr_time):
        while curr_time <= self.song_length:
            if self.changed_song:
                return
            if not self.paused:
                rect = self.canvas.create_line(0, 430, seek_pos, 430, width=10, fill='blue', capstyle=ROUND)
                seek_pos += seekdist
                time.sleep(1)
                curr_time += 1
                self.master.update()
                self.canvas.delete(rect)
                del rect
    #-----------------------------------------------------------------------------------------------------------------------------------        

    def volume_slider(self):
        if not self.showing_volume:
            t = 0
            while t < 100:
                slider = ttk.Scale(root, from_=1, to_=100, length=t, orient='vertical', value=self.volume)
                slider.place(x=758, y=343)
                root.update()
                t += 1.5
                slider.destroy()
                del slider
            self.slider = ttk.Scale(self.master, from_=1, to_=100, length=100, orient='vertical',
                                command=self.set_volume, value=self.volume)
            self.slider.place(x=758, y=343)
            self.showing_volume = True
        else:
            self.slider.destroy()
            t = 100
            while t > 0:
                slider = ttk.Scale(root, from_=1, to_=100, length=t, orient='vertical', value=self.volume)
                slider.place(x=758, y=343)
                root.update()
                t -= 1.5
                slider.destroy()
                del slider

            self.slider.destroy()
            self.showing_volume = False
    #-----------------------------------------------------------------------------------------------------------------------------------        

    def set_volume(self, volume):
        v = round((float(volume)/100), 1)
        self.song.set_volume(v)
        self.volume = volume
    #-----------------------------------------------------------------------------------------------------------------------------------        

    def control_pause(self):
        if not self.paused:
            pygame.mixer.pause()
            self.paused = True
            self.pause_play_btn.configure(image=self.play_icon)
        else:
            pygame.mixer.unpause()
            self.paused = False
            self.pause_play_btn.configure(image=self.pause_icon)
    #-----------------------------------------------------------------------------------------------------------------------------------        

    def playsong(self, name, data):
        self.song = pygame.mixer.Sound(name)
        self.song.play()
        self.volume = 100
        self.song_length = self.song.get_length()

        seek_pos = 0
        seekdist = 800 // self.song_length
        curr_time = 0
        self.changed_song = False
        self.seeking = threading.Thread(target=self.seekThread, args=(seek_pos, seekdist, curr_time))
        self.seeking.start()
        
        min, secs = divmod(self.song.get_length(), 60)
        self.canvas.itemconfig(self.length_text, text='{:02d}:{}'.format(round(min), round(secs)))
    #-----------------------------------------------------------------------------------------------------------------------------------        
    
    def next_song(self):
        self.song.stop()
        new = self.curr_song.next
        self.curr_song = self.song_queue[self.pos+1]
        curr_name = self.curr_song.name

        g = threading.Thread(target=self.playsong, args=(new, 3))
        g.start()
        
        self.pos += 1
        self.changed_song = True
        self.seek_pos = 0
        self.seekdist = 800 // self.song_length
        self.curr_time = 0

        s = os.path.splitext(curr_name)[0]
        name = s.split(os.path.dirname(s) + '/')[1]
        self.master.title(name)
    #-----------------------------------------------------------------------------------------------------------------------------------        

    def prev_song(self):
    
        self.song.stop()

        new = self.curr_song.prev
        self.curr_song = self.song_queue[self.pos-1]
        curr_name = self.curr_song.name

        g = threading.Thread(target=self.playsong, args=(new, 3))
        g.start()

        self.pos -= 1
        self.changed_song = True
        self.seek_pos = 0
        self.seekdist = 800 // self.song_length
        self.curr_time = 0

        s = os.path.splitext(curr_name)[0]
        name = s.split(os.path.dirname(s) + '/')[1]
        self.master.title(name)
    #-----------------------------------------------------------------------------------------------------------------------------------        

    def check_changes(self):
        while not self.paused:
            if (self.pos + 1) ==  self.queue_length:
                self.next_btn.configure(state=DISABLED)
            else:
                self.next_btn.configure(state=NORMAL)
                
        
            if self.pos == 0:
                self.prev_btn.configure(state=DISABLED)
            else:
                self.prev_btn.configure(state=NORMAL)
            
            self.master.update()
    #-----------------------------------------------------------------------------------------------------------------------------------        

    def load(self):
        self.song_queue.clear()
        try:
            self.song.stop()
        except AttributeError:
            pass
        loaded_songs = askopenfilenames(
                                   filetypes=[('Audio files', '.mp3 .wav .ogg .mid')])   
        if len(loaded_songs) > 1:
            first = Song(loaded_songs[0], next=loaded_songs[1], prev=None)
            self.song_queue.append(first)
            try:
                for s in range(1, len(loaded_songs)):
                    i = Song(loaded_songs[s], next=loaded_songs[s+1], prev=loaded_songs[s-1])
                    self.song_queue.append(i)
            except IndexError:
                last = Song(loaded_songs[-1], next=None, prev=loaded_songs[-2])
                self.song_queue.append(last)
        else:
            self.song_queue.append(Song(loaded_songs[0], next=None, prev=None))
        self.queue_length = len(loaded_songs)
        self.pos = 0
        self.curr_song = self.song_queue[0]
        curr_name = self.curr_song.name
        
        self.song = pygame.mixer.Sound(curr_name)
        min, secs = divmod(self.song.get_length(), 60)
        self.length_text = self.canvas.create_text(770, 415, text='{:02d}:{}'.format(round(min), round(secs)), fill='white')

        self.volume = 100
        self.song.play()
        self.song_length = self.song.get_length()
        seek_pos = 0
        seekdist = 800 // self.song_length
        curr_time = 0

        self.seeking = threading.Thread(target=self.seekThread, args=(seek_pos, seekdist, curr_time))
        self.seeking.start()

        self.volume_btn.configure(state=NORMAL)
        self.next_btn.configure(state=NORMAL)
        self.prev_btn.configure(state=NORMAL)
        self.pause_play_btn.configure(state=NORMAL)

        s = os.path.splitext(curr_name)[0]
        name = s.split(os.path.dirname(s) + '/')[1]
        self.master.title(name)

        check = threading.Thread(target=self.check_changes)
        check.start()
#=====================================================================================================================================================================

root = Tk()
root.geometry('800x500')
root.resizable(0,0)


s = Player(root)

























