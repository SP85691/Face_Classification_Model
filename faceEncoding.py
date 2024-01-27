import face_recognition as fr
import cv2 as cv
import pickle
import os
import json
import numpy as np

def find_new_items(folder_path):
    if os.path.exists(folder_path):
        path_list = os.listdir(folder_path)
    else:
        print(f"Path '{folder_path}' does not exist.")
        return [], []

    imageList = []
    student_id = []
    for path in path_list:
        imageList.append(cv.imread(os.path.join(folder_path, path)))
        student_id.append(os.path.splitext(path)[0])

    return student_id, imageList

def findEncoding(imageList):
    encodeList = []
    for image in imageList:
        img = cv.cvtColor(image, cv.COLOR_BGR2RGB)
        encode = fr.face_encodings(img)[0]
        encodeList.append(encode)

    return encodeList

def main():
    folderPath = 'Images'
    studentID, ImageList = find_new_items(folderPath)
    encodeListKnown = [np.random.rand(128) for _ in range(len(studentID))]  # Example encodings
    print(f'Student ID: {[id for id in studentID]}')
    print(f'Image List: {len(ImageList)}')

    print('Encoding Started')
    encodeListKnown = findEncoding(ImageList)
    print('Encoding Completed Successfully')

    encodeListStudent_ID = [encodeListKnown, studentID]
    print('Saving Encodings')
    with open('face_encoding_new.pkl', 'wb') as f:
        pickle.dump(encodeListStudent_ID, f)
        f.close()
    print('Encodings Saved Successfully')


if __name__ == '__main__':
    main()
