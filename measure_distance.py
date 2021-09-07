import cv2

# distance from camera to object(face)
known_distance = 40
#width of face in realworld
known_width = 16

#colors
RED = (0, 0, 255)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
fonts = cv2.FONT_HERSHEY_DUPLEX

face_detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

def FocalLength(measured_distance, real_width, width_in_rf_image):
	focal_length = (width_in_rf_image * measured_distance)/real_width
	return focal_length

def Distance_finder(focal_length, real_face_width, face_width_in_frame):
	distance = (real_face_width * focal_length)/face_width_in_frame
	return distance

def face_data(image):
	face_width = 0
	gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	face = face_detector.detectMultiScale(gray_image,1.3,5)
	for (x, y, h, w) in face:
		cv2.rectangle(image, (x, y), (x+w, y+h), WHITE, 1)
		face_width = w
	return face_width

def main():
	ref_image = cv2.imread("1.jpg")
	ref_image_face_width = face_data(ref_image)
	focal_length_found = FocalLength(known_distance, known_width, ref_image_face_width)
	print(focal_length_found)
	print(ref_image_face_width)
	cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)

	while True:
		_, frame = cap.read()

		face_width_in_frame = face_data(frame)

		if face_width_in_frame !=0:
			distance = Distance_finder(focal_length_found, known_width, face_width_in_frame)
			cv2.putText(frame, f"Distance = {distance}", (50,50), fonts, 1, (GREEN), 2)

		cv2.imshow('web camera', frame)		
		if cv2.waitKey(1)==ord('q'):
			break

	cap.release()
	cv2.destroyAllWindows()

if __name__ == "__main__":
	main()