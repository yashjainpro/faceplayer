import os
from tkinter.filedialog import askdirectory
import glob
import pygame
from mutagen.id3 import ID3, TIT2
from tkinter import *
import eyed3
root = Tk()
root.minsize(300,300)


listofsongs = []
realnames = []

v = StringVar()
songlabel = Label(root,textvariable=v,width=100)

index = 0

def directorychooser():
    pat = "./music"
    directory = os.chdir(pat)

    for files in os.listdir(directory):
        if files.endswith(".mp3"):
            print(files)
            realdir = os.path.realpath(files)
            realnames.append(files)


            listofsongs.append(files)

    pygame.mixer.init()
    pygame.mixer.music.load(listofsongs[0])
    pygame.mixer.music.play()
directorychooser()

def updatelabel():
    global index
    global songname
    v.set(realnames[index])
    #return songname



def nextsong(event):
    global index
    index += 1
    if(index==len(listofsongs)):
        index=0
    pygame.mixer.music.load(listofsongs[index])
    pygame.mixer.music.play()
    #a = pygame.mixer.music.get_length()
    #print("length", a.get_length())
    
   # while(pygame.mixer.music.get_busy()):
     #   print ("\r"+str(pygame.mixer.music.get_pos()))
     
    updatelabel()

def prevsong(event):
    global index
    index -= 1
    if(index<0):
        index=len(listofsongs)-1
    pygame.mixer.music.load(listofsongs[index])
    pygame.mixer.music.play()
    print(pygame.mixer.music.get_pos())
    updatelabel()


def stopsong(event):
    pygame.mixer.music.stop()
    v.set("")
    #return songname
    
def playit(event):
   # y=realnames.index(listbox.get('active'))
    pygame.mixer.music.load(listbox.get('active'))
    pygame.mixer.music.play()
    updatelabel()

label = Label(root,text='Music Player')
label.pack()

listbox = Listbox(root,width=50,height=60)
listbox.pack(side="right",padx=5)

#listofsongs.reverse()
realnames.reverse()

for items in realnames:
	listbox.insert(0,items)

realnames.reverse()
#listofsongs.reverse()

playbutton = Button(root,text = 'PLAY')
playbutton.pack()

nextbutton = Button(root,text = 'Next Song')
nextbutton.pack()


previousbutton = Button(root,text = 'Previous Song')
previousbutton.pack()

stopbutton = Button(root,text='Stop Music')
stopbutton.pack()

playbutton.bind("<Button-1>",playit)
nextbutton.bind("<Button-1>",nextsong)
previousbutton.bind("<Button-1>",prevsong)
stopbutton.bind("<Button-1>",stopsong)

songlabel.pack()

def change_volume(val):
	vol = int(val)/100
	pygame.mixer.music.set_volume(vol)

def change_position(val):
	pygame.mixer.music.pause()
	pygame.mixer.music.set_pos(int(val))
	pygame.mixer.music.play(-1, pygame.mixer.music.get_pos()/1000.0)
	seek_scale.set(int(val))
	

volume_scale = Scale(root, from_=0, to=100*pygame.mixer.music.get_volume(), orient=VERTICAL, command=change_volume)
volume_scale.set(50)
volume_scale.pack(side="right")

seek_scale = Scale(root, from_=0, to=100, orient=HORIZONTAL, command=change_position)
seek_scale.set(0)
seek_scale.pack()

#if(pygame.mixer.music.get_busy()):
#	print ("\r"+str(pygame.mixer.music.get_pos()))

	

root.mainloop()
