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
