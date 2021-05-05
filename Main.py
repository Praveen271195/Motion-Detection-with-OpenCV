# Importing OpenCv library
import cv2
# importing sound library
import winsound

# Selecting the web camera connected to the computer to read video
camera = cv2.VideoCapture(0)
# Looping through to retrieve the frames from the video, whenever the camera is on
while camera.isOpened():
    # Saving in respective variables after reading the video data as frame 1 and frame 2
    retrieve, frame1 = camera.read()
    retrieve, frame2 = camera.read()
    # Finding the absolute difference between the frames in order to detect the motion
    difference = cv2.absdiff(frame1, frame2)
    # Converting the colored data into gray scaled data
    gray = cv2.cvtColor(difference, cv2.COLOR_BGR2GRAY)
    # Making the gray scaled data blurred
    blurred = cv2.GaussianBlur(gray,(5,5),0)
    # Setting a threshold to get rid of the noise in the frames
    _, threshold = cv2.threshold(blurred, 20, 225, cv2.THRESH_BINARY)
    # To dilate the required frames
    dilated = cv2.dilate(threshold,None,iterations=3)
    # To find the boxes/contours over the detected motion
    contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    # Ignoring the smaller differences in motion
    for c in contours:
        if cv2.contourArea(c) < 5000:
            continue
        # If difference is not so large, knowing there coordinates, width and height
        x, y, w, h = cv2.boundingRect(c)
        # Displaying the rectangular box over the difference
        cv2.rectangle(frame1, (x, y), (x+w, y+h), (0, 255, 0), 2)
        # Playing sound in sync with the detection of the motion
        winsound.PlaySound("alert.wav", winsound.SND_ASYNC)
    # Breaking the program when teh user exists by pressing "q"
    if cv2.waitKey(10) == ord("q"):
        break
    # Shows the read video data (absolute difference which is in gray scale) on screen
    cv2.imshow("Security Camera", frame1)
