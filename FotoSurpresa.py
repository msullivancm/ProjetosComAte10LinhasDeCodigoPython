#pip install opencv-python
import cv2 

webcam = cv2.VideoCapture(0)

try:
    if webcam.isOpened():
        validacao, frame = webcam.read()
        cv2.imwrite("testeWebcam.png", frame)
    webcam.release()
    cv2.destroyAllWindows()
except:
    print("Não foi possível abrir a câmera.")