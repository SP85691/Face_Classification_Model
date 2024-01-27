import cv2
import time
import numpy as np
import face_recognition
import cvzone
import pickle
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db


cred = credentials.Certificate("serviceAccountKey.json")

firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://faceattendancesys-f6e05-default-rtdb.firebaseio.com/'
})

# Load the model
print("Loading Model")
file = open('face_encoding_new.pkl', 'rb')
encodeListStudent_ID = pickle.load(file)
file.close()
encodeListKnown, studentID = encodeListStudent_ID
print("Model Loaded Successfully")

# Open the webcam
cap = cv2.VideoCapture(0)

def frameWindow():
    cap = cv2.VideoCapture(0)  # Initialize the webcam (change the index if needed)
    
    while True:
        # Read frame from the webcam
        ret, frame = cap.read()

        imgs = cv2.resize(frame, (0, 0), None, 0.25, 0.25)
        imgs = cv2.cvtColor(imgs, cv2.COLOR_BGR2RGB)

        facesCurFrame = face_recognition.face_locations(imgs)
        encodesCurFrame = face_recognition.face_encodings(imgs, facesCurFrame)

        for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)

            matchIndex = np.argmin(faceDis)

            if matches[matchIndex]:
                name = studentID[matchIndex].upper()
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cvzone.cornerRect(frame, (x1, y1, x2, y2), 20, rt=0)
                cv2.rectangle(frame, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
                cv2.putText(frame, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                

        # Create a blank image for the right frame
        info_frame = np.zeros((frame.shape[0], frame.shape[1] // 2, 3), dtype=np.uint8)
        cv2.putText(info_frame, "Attendance System", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255, 255, 255), 2)
        cv2.putText(info_frame, "Active", (20, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255, 255, 255), 2)
    
        # Display the name in the info frame
        if 'name' in locals():  # Check if 'name' is defined
            # fetch the all details of 'name' from database
            ref = db.reference('Students')
            data = ref.get()
            if name in data:
                student_data = data[name]
                cv2.putText(info_frame, f"Name: {student_data['name']}", (20, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255, 255, 255), 2)
                cv2.putText(info_frame, f"Major: {student_data['major']}", (20, 200), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255, 255, 255), 2)
                cv2.putText(info_frame, f"Year: {student_data['year']}", (20, 250), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255, 255, 255), 2)
                cv2.putText(info_frame, f"Starting Year: {student_data['starting_year']}", (20, 300), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255, 255, 255), 2)
                cv2.putText(info_frame, f"Total Attendance: {student_data['total_attendance']}", (20, 350), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255, 255, 255), 2)
                cv2.putText(info_frame, f"Last Attendance: {student_data['last_attendance']}", (20, 400), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255, 255, 255), 2)
                # after 5 seconds delay clear all these text from the info_frame
            else:
                cv2.putText(info_frame, "Name not found in database", (20, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255, 255, 255), 2)
                cv2.putText(info_frame, "Please try again", (20, 200), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255, 255, 255), 2)
            
        # Display the combined frame
        combined_frame = np.hstack((frame, info_frame))

        # Check for key press
        cv2.imshow("Attendance System", combined_frame)
        key = cv2.waitKey(1)
        if key == ord('q'):
            break

    # Release the webcam and destroy windows
    cap.release()
    cv2.destroyAllWindows()

def mark_attendance(name):
    print(name)


if __name__ == '__main__':
    frameWindow()