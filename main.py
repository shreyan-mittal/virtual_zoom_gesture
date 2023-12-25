import cv2
from cvzone. HandTrackingModule import HandDetector
cap = cv2. VideoCapture (0)
cap. set (3, 1280) 
cap. set (4, 720)

detector = HandDetector (detectionCon=0.8)
startdDist = None
scale = 0
cx,cy= 500,500
while True:
    success, img = cap.read()
    hands, img = detector. findHands (img) 
    img1=cv2.imread("one.jpg")
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    #recognition of hands and fingers.
    if len(hands)==2:  
        print(detector.fingersUp(hands[0]), detector.fingersUp(hands[1])) 

        # If the index finger and thumb are up of both hands, then only it will show the output which
        # is zoom gesture.
        #if detector.fingersUp(hands[0]) == [1,1,0,0,0] and detector.fingersUp(hands[1]) == [1,1,0,0,0]:
            #print("Zoom gesture")
        
        # finding distance bw tip of the index fingers.
        lmList1= hands[0]["lmList"]
        lmList2= hands[1]["lmList"]
        if startdDist is None:
            length, info, img = detector.findDistance([lmList1[8][0], lmList1[8][1]], [lmList2[8][0], lmList2[8][1]], img)
            startdDist  = length

        length, info, img = detector.findDistance([lmList1[8][0], lmList1[8][1]], [lmList2[8][0], lmList2[8][1]], img)
        scale = int((length - startdDist)//2)
        cx,cy = info[4:]
        #print(scale)

    else:
        startdDist = None #if two hands are not detected, then the distance b/w two hands will be 0.
    try:
        h1, w1, _=img1.shape
        newH, newW = ((h1 + scale)//2)*2, ((w1 + scale)//2)*2
        img1 = cv2.resize(img1,(newW, newH))

        img[cy-newH//2:cy+newH//2, cx-newW//2:cx+newW//2] = img1
    except:
        pass
    #img[0:250, 0:250] = img1 
    #adding image to our screen on the left hand side. 0:250 
    # shows the position of the image which is top left corner.
    cv2. imshow ("Image", img) 
    cv2.waitKey (1) 