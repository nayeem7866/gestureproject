from django.http import HttpResponse
from django.shortcuts import render

def index(request):
    return render(request,'index.html')

def project(request):
    import cv2
    from cvzone.HandTrackingModule import HandDetector
    import numpy as np
    import math
    import time
    import pyautogui
    from pynput.keyboard import Key, Controller

    cap = cv2.VideoCapture(0)
    detector = HandDetector(detectionCon=0.8, maxHands=2)
    keyboard = Controller()

    frameR = 100
    smoothening = 7
    plocX, plocY = 0, 0 # Previous x and y location
    clocX, clocY = 0, 0 # Current x and y location
    wCam, hCam = 640, 480
    wScr, hScr = pyautogui.size() ## Outputs the high and width of the screen (1920 x 1080)

    while True:
        success, img = cap.read()
        hands, img = detector.findHands(img)  # With Draw
        # hands = detector.findHands(img, draw=False)  # No Draw

        if hands:
            # Hand 1
            hand1 = hands[0]
            lmList1 = hand1["lmList"]  # List of 21 Landmarks points
            bbox1 = hand1["bbox"]  # Bounding Box info x,y,w,h
            handType1 = hand1["type"]  # Hand Type Left or Right

            # print(len(lmList1),lmList1)
            # print(bbox1)
            # fingers1 = detector.fingersUp(hand1)
            if len(lmList1) != 0:
                x1, y1 = lmList1[8][0], lmList1[8][1] # Gets index 8s x and y values (for both hands hand1,hand2)
                x2, y2 = lmList1[12][0], lmList1[12][1]  # Gets index 12s x and y values (for both hands hand1,hand2)
                x3, y3 = lmList1[4][0], lmList1[4][1]     # Gets index 4s x and y values (for both hands hand1,hand2)
                x4, y4 = lmList1[16][0], lmList1[16][1]    # Gets index 16s x and y values (for both hands hand1,hand2)
                x5, y5 = lmList1[20][0], lmList1[20][1]     # Gets index 20s x and y values (for both hands hand1,hand2)
                # for thumb
                # print(x1,x2,x3, y1,y2,y3)
                cv2.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR),
                              (255, 0, 255), 2)

            if detector.fingersUp(hands[0]) == [1, 1, 1, 1, 1] or detector.fingersUp(hands[0]) == [1, 1, 1, 1, 1]:
                #  ===================================Convert Coordinates
                x3 = np.interp(x1, (frameR, wCam - frameR), (0, wScr)) # Converts the width of the window relative to the screen width
                y3 = np.interp(y1, (frameR, hCam - frameR), (0, hScr)) # Converts the height of the window relative to the screen height

                #  ===================================Smoothen Values
                clocX = plocX + (x3 - plocX) / smoothening
                clocY = plocY + (y3 - plocY) / smoothening
                # ===================================== Move Mouse
                pyautogui.moveTo(wScr - clocX, clocY)
                #cv2.circle(img, (x1, y1), 10, (0, 0, 255), cv2.FILLED)
                plocX, plocY = clocX, clocY

            if detector.fingersUp(hands[0]) == [0, 1, 1, 0, 0] or detector.fingersUp(hands[0]) == [0, 1, 1, 0, 0]:

                r, t = 9, 2
                if True:
                    cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), t)
                    cv2.circle(img, (x1, y1), r, (255, 0, 255), cv2.FILLED)
                    cv2.circle(img, (x2, y2), r, (255, 0, 255), cv2.FILLED)
                   # cv2.circle(img, (cx, cy), r, (0, 0, 255), cv2.FILLED)
                    length = math.hypot(x2 - x1, y2 - y1)
                    if length < 40:
                       # cv2.circle(img, (cx, cy), 10, (0, 255, 0), cv2.FILLED)
                        pyautogui.leftClick()
                        cv2.waitKey(1)

            if detector.fingersUp(hands[0]) == [0, 1, 0, 0, 0] or detector.fingersUp(hands[0]) == [0, 1, 0, 0, 0]:

                if True:
                    # cv2.line(img, (x3, y3), (x1, y1), (255, 0, 255), t)
                    # cv2.circle(img, (x1, y1), r, (255, 0, 255), cv2.FILLED)
                    # cv2.circle(img, (x3, y3), r, (255, 0, 255), cv2.FILLED)
                    # cv2.circle(img, (cx3, cy3), r, (0, 0, 255), cv2.FILLED)
                    length = math.hypot(x1, y1)
                    print(length)
                    if length < 350:
                        # cv2.circle(img, (cx3, cy3), 10, (0, 255, 0), cv2.FILLED)
                        keyboard.press(Key.media_volume_up)
                        keyboard.release(Key.media_volume_up)
                        time.sleep(0.1)
                    if length > 350:
                        # cv2.circle(img, (cx3, cy3), 10, (0, 0, 0), cv2.FILLED)
                        keyboard.press(Key.media_volume_down)
                        keyboard.release(Key.media_volume_down)
                        time.sleep(0.1)

            if detector.fingersUp(hands[0]) == [0, 1, 1, 1, 0] or detector.fingersUp(hands[0]) == [0, 1, 1, 1, 0]:
                pyautogui.doubleClick()
                cv2.waitKey(1)

            if detector.fingersUp(hands[0]) == [1, 0, 0, 0, 0] or detector.fingersUp(hands[0]) == [1, 0, 0, 0, 0]:
                pyautogui.rightClick()
                cv2.waitKey(1)

        cv2.imshow("Image", img)
        cv2.waitKey(1)
    return render(request,'index.html')