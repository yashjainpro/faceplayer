from pymongo import MongoClient
from pprint import pprint
from random import randint
client = MongoClient("mongodb://localhost:27017")
db = client.capstone

collection = db.songs

songs = db.songs
import face_recognition
import cv2
video_capture = cv2.VideoCapture(0)
yash_image = face_recognition.load_image_file("yash.jpg")
yash_face_encoding = face_recognition.face_encodings(yash_image)[0]

tejasvi_image = face_recognition.load_image_file("tejas.jpg")
tejasvi_face_encoding = face_recognition.face_encodings(tejasvi_image)[0]

vishwas_image = face_recognition.load_image_file("vishwas.jpg")
vishwas_face_encoding = face_recognition.face_encodings(vishwas_image)[0]

known_face_encodings = [
    yash_face_encoding,
    vishwas_face_encoding,
    tejasvi_face_encoding
]
known_face_names = [
    "yash jain",
    "vishwas singla",
    "Tejasvi Pal"
]

# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
users_present=[]
process_this_frame = True

while True:
    # Grab a single frame of video
    ret, frame = video_capture.read()

    # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = small_frame[:, :, ::-1]

    # Only process every other frame of video to save time
    if process_this_frame:
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"

            # If a match was found in known_face_encodings, just use the first one.
            if True in matches:
                first_match_index = matches.index(True) 
                users_present.append(first_match_index)              
                name = known_face_names[first_match_index]

            face_names.append(name)

    process_this_frame = not process_this_frame
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    # Display the resulting image
    cv2.imshow('Video', frame)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()
sortedplaylist=[]
#/////////////////////////////////////////////////////////mongo Db part/////////////////////////////////////////
users_present=list(set(users_present))
numbers=len(users_present)
if numbers == 1:
	a = users_present[0] 
	for songs in songs.find( {'user_id':{"$eq": a}}, {'title':1, '_id' :0}):
		sortedplaylist.append(songs['title'])
		print(songs['title'])
elif numbers == 2:
	a = users_present[0]
	b = users_present[1]
	for songs in songs.find( {'user_id':{"$eq": b, "$eq":a}}, {'title':1, '_id' :0}):
		sortedplaylist.append(songs['title'])
		print(songs)
else:
	a = users_present[0]
	b = users_present[1]
	c = users_present[2]
	for songs in songs.find( {'user_id':{"$eq": a, "$eq":b,"$eq":c}}, {'title':1, '_id' :0}):
		sortedplaylist.append(songs['title'])
		print(songs)
print(sortedplaylist)

#//////////////////////////////////////////////////////////////////Music player part/////////////////////////////////////////////////////////////
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
	for names in sortedplaylist:
		realnames.append(names)
		listofsongs.append(names)

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

	

root.mainloop()
