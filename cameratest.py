import numpy as np
import cv2

cap = cv2.VideoCapture(-1)
cap.set(3,1280)
cap.set(4,720)

lower = np.array([0, 100, 0])
upper = np.array([150, 250, 250])

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) #BGR2HSV

    # Display the resulting frame
    #cv2.imshow('frame',gray)

    shapeMask = cv2.inRange(frame, lower, upper)

# find the contours in the mask
    (cnts, _) = cv2.findContours(shapeMask.copy(), cv2.RETR_EXTERNAL,
    cv2.CHAIN_APPROX_SIMPLE)
    cv2.imshow("Mask", shapeMask)

    
    # loop over the contours
    #for c in cnts:
		# draw the contour and show it
		#cv2.drawContours(frame, [c], -1, (0, 255, 0), 2)
                 #cv2.imshow("Image", frame)
		#cv2.waitKey(0)

#Nupufunktisoonid
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    elif cv2.waitKey(1) & 0xFF == ord('s'):
        open("pilt.png")
        cv2.imwrite('pilt.png',shapeMask)



# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
