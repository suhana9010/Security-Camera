import winsound
import cv2, time
import numpy, os

cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)

fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi', fourcc, 20.0, (640, 480))
TIMER = int(40)
prev=time.time()

while (cam.isOpened() and TIMER>=0):
    ret, frame1 = cam.read()
    ret, frame2 = cam.read()
    diff = cv2.absdiff(frame1, frame2)
    gray = cv2.cvtColor(diff, cv2.COLOR_RGB2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
    dilated = cv2.dilate(thresh, None, iterations=3)
    contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    date_time = time.strftime("recording %H-%M -%d %m %y")  # set current time as video name
    t = time.ctime()
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(frame1,t,
                (380, 455), font,
                0.5, (5, 5, 5),
                1)
    cur = time.time()

    if cur - prev >= 1:
        prev = cur
        TIMER = TIMER - 1
    for c in contours:
        if cv2.contourArea(c) < 5000:
            continue
        x, y, w, h = cv2.boundingRect(c)
        cv2.rectangle(frame1, (x, y), (x + w, y + h), (0, 255, 0), 2)
        winsound.PlaySound('alert.wav', winsound.SND_ASYNC)

    if cv2.waitKey(10) == ord('q'):
        break
    cv2.imshow('Shannu Cam', frame1)
    out.write(frame1)
# Release everything if job is finished
cam.release()
out.release()
cv2.destroyAllWindows()
