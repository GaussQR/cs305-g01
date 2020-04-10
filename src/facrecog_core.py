import dlib
import face_recognition
import glob
import pickle
from PIL import Image,ImageFont, ImageDraw, ImageEnhance
#import sqlite3

def add_target_faces(path):
	faces = {}
	for img in glob.glob("known/*.jpg"):
		print("encoding img...")
		f_image = face_recognition.load_image_file(img)
		x = face_recognition.face_encodings(f_image)[0]
		name = img.split('/')[1].split('.')[0]
		# if faces.get(name) is None:
		#     faces[name] = []
		faces[name] = x
		with open('encoded_faces.pkl', 'wb') as fp:
			pickle.dump(encoded_faces, fp)

def load_encoded_faces(path_file):
	return pickle.load(open(path_file,'rb'))

def identify_faces_image(img):
	faces = load_encoded_faces('encoded_faces.pkl')
	face_enc, name_face = list(faces.values()), list(faces.keys()) # Loading face encoding along with their names.

	group_img = face_recognition.load_image_file(img)
	src_img = Image.open(img).convert("RGB")
	coordinates = face_recognition.face_locations(group_img)
	face_encodings =   face_recognition.face_encodings(group_img)
	draw = ImageDraw.Draw(src_img)
	face_in_img = []

	print(img," contains faces: ")
	for (c,each_encoding) in zip(coordinates,face_encodings):
		results = face_recognition.compare_faces(face_enc, each_encoding, 0.5)
		index = results.index(True)
		indices = [i for i, value in enumerate(results) if value == True] # Should be one		
#		assert(len(indices) == 1)
		for index in indices:
			recog_name = name_face[index]
			face_in_img.append((recog_name, c))
			# draw.rectangle(((c[3],c[0]), (c[1],c[2])), outline='red')
			# draw.text((c[3]+1, c[2]-1), recog_name, font = ImageFont.truetype('arial.ttf', 160))
			# src_img.save(img.split('.')[0]+"output.jpg")
	return face_in_img

def identify_faces_images(path_folder):
	faces_in_folder = []
	for img in glob.glob(path_folder + "*.jpg"):
		faces_in_folder.append(identify_faces_images(img))
	return faces_in_folder

def identify_faces_video(path_video):
	