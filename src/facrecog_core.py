import dlib
import face_recognition
import glob
import pickle
import cv2
import numpy as np
import os
from PIL import Image,ImageFont, ImageDraw, ImageEnhance

from zipfile import ZipFile 
  
def extract_zip(file_name):  
    with ZipFile(file_name, 'r') as zip: 
        zip.extractall() 
    return file_name.split('.')[0]

def add_target_faces(path):
	faces = {}
	for img in glob.glob(path + "/*.jpg"):
		print("encoding img...")
		f_image = face_recognition.load_image_file(img)
		x = face_recognition.face_encodings(f_image)[0]
		name = img.split('/')[1].split('.')[0]
		# if faces.get(name) is None:
		# 	faces[name] = []
		faces[name] = x
	with open('encoded_faces.pkl', 'wb') as fp:
		pickle.dump(faces, fp)

def load_encoded_faces(path_file='encoded_faces.pkl'):
	return pickle.load(open(path_file,'rb'))

def identify_faces_image(img, faces, save_output=0, isfile=0):
    print(save_output)
    face_enc, name_face = list(faces.values()), list(faces.keys()) # Loading face encoding along with their names.
    group_img = face_recognition.load_image_file(img) if isfile == 0 else img
    coordinates = face_recognition.face_locations(group_img)
    face_encodings =   face_recognition.face_encodings(group_img)
    src_img = Image.open(img).convert("RGB") if isfile == 0 else Image.fromarray(img).convert('RGB')
    draw = ImageDraw.Draw(src_img)
    face_in_img = []
    # print(img," contains faces: ")
    for (c,each_encoding) in zip(coordinates,face_encodings):
        results = face_recognition.compare_faces(face_enc, each_encoding, 0.5)
        indices = [i for i, value in enumerate(results) if value == True] # Should be one       
        # assert(len(indices) == 1)
        for index in indices:
            recog_name = name_face[index]
            face_in_img.append((recog_name, c))
            if save_output:
                draw.rectangle(((c[3],c[0]), (c[1],c[2])), outline='red')
                draw.text((c[3]+1, c[2]-1), recog_name, font = ImageFont.truetype('arial.ttf', 160))
    if save_output:
        if 'output' not in os.listdir():
            os.mkdir('output')
        src_img.save('output/' + img.split('/')[-1])
    return face_in_img

def identify_faces_images(path_folder, faces, save_output=0):
	faces_in_folder = []
	for img in glob.glob(path_folder + "/*.jpg"):
		faces_in_folder.append(identify_faces_image(img, faces, save_output))
	return faces_in_folder

# from google.colab.patches import cv2_imshow
def identify_faces_video(path_video, faces, show_output=0):
    cap = cv2.VideoCapture(path_video)
    frate = cap.get(cv2.CAP_PROP_FPS)
    faces_in_video = []
    i = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if ret == False: break
        i += 1
        if i % frate != 1: continue
        # frame = cv2.resize(frame, (0, 0), fx = 0.25, fy = 0.25)
        frame = np.array(frame[:, :, ::-1])
        # print(frame.shape)
        res = identify_faces_image(frame, faces, isfile=1) #[(name, coordin)]
        faces_in_video.append(res)
        if show_output:
            for (name, (top, right, bottom, left)) in res:
                # top, right, bottom, left = map(int, [top, right, bottom, left]) 
                # print((top, right, bottom, left))
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
            frame = frame[:, :, ::-1]
            cv2.imshow('Video', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    return faces_in_video

z = input("Enter zip file path")
folder_name = extract_zip(z)
add_target_faces(folder_name)
faces = load_encoded_faces('encoded_faces.pkl')
identify_faces_video('al.mp4', faces, 1)
