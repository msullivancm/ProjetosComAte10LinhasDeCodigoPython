#pip install pytesseract tesseract
#pip install opencv-python
import pytesseract 
import cv2 

imagem = cv2.imread("imagemASerLida.jpg")

caminho = r"c:\Users\Python\AppData\Local\Programs\Tesseract-OCR"

pytesseract.pytesseract.tesseract_cmd = caminho + r"\tesseract.exe"
texto = pytesseract.image_to_string(imagem, lang="por")

print(texto)