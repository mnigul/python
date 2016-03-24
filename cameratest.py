import numpy as np
import cv2

#640 x 480
cap = cv2.VideoCapture(-1)
cap.set(3,640)
cap.set(4,480)

lower = np.array([1, 60, 60])
upper = np.array([60, 250, 240])

while(True):

    # Capture frame-by-frame
    ret, frame = cap.read()

    cv2.putText(frame,"Hello World!!!", (10,50), cv2.FONT_HERSHEY_SIMPLEX, 2, 255)
    # Our operations on the frame come here
    #color = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) #BGR2HSVBGR2GRAY


    shapeMask = cv2.inRange(frame, lower, upper)

# find the contours in the mask
    (cnts, _) = cv2.findContours(shapeMask.copy(), cv2.RETR_EXTERNAL,
    cv2.CHAIN_APPROX_SIMPLE)


    # Display the resulting frame
    cv2.imshow('frame',frame)
    cv2.imshow("Mask", shapeMask)
    #frameOut = hstack(frame, shapeMask);
    #cv2.imshow (frameOut)
    #CombineVids (frame, shapemask, combined)

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
