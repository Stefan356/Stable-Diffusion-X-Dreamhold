import cv2
import pytesseract
import pyscreenshot as ImageGrab

pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

#grab part of the screen
im = ImageGrab.grab(bbox=(300,300,1600,1600))
im.show()

#store in a file
im.save('screen.png')

#what image should be read
img = cv2.imread('screen.png')

#image to string
text = pytesseract.image_to_string(img)

print(text)
