#pip install opencv-python
import cv2 

webcam = cv2.VideoCapture()

def returnCameraIndexes():
    # checks the first 10 indexes.
    index = 0
    arr = []
    i = 10
    while i > 0:
        cap = cv2.VideoCapture(index)
        if cap.read()[0]:
            arr.append(index)
            cap.release()
        index += 1
        i -= 1
    return arr

print(returnCameraIndexes()[0])

try:
    if webcam.isOpened():
        validacao, frame = webcam.read()
        while validacao:
            validacao, frame = webcam.read()
            cv2.imshow("Video da Webcam", frame)
            key = cv2.waitKey(5)
            if key == 27: #ESC
                break
        cv2.imwrite("testeWebcam.png", frame)
    webcam.release()
    cv2.destroyAllWindows()
except:
    print("Não foi possível abrir a câmera.")