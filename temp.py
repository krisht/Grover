import cv2


cap1 = cv2.VideoCapture(1)
cap2 = cv2.VideoCapture(2)


ii = 0
img_counter = 0
while True:
	ii+=1
	_, frame1 = cap1.read()
	#_, frame2 = cap2.read()
	cv2.imshow('a',frame1)
	#cv2.imshow('b', frame2)
	k = cv2.waitKey(1)
	if k%256 == 27:
		print("Escape hit, closing...")
		break
	elif k%256 == 32:
		img_name = "{}.png".format(img_counter)
		cv2.imwrite("framea" + img_name, frame1)
		#cv2.imwrite('frame2' + img_name, frame2)
		print("{} written!".format(img_name))
		img_counter += 1


cap1.release()
cv2.destroyAllWindows()