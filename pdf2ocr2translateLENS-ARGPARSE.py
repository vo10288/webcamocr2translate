import cv2
import pytesseract
from googletrans import Translator
from PIL import Image
import time
import argparse
from datetime import datetime

filename = datetime.now().strftime("%Y_%m_%d_%H_%M_%S") +'.png'

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--input", default="immagine.png",
	help="input file")
	
ap.add_argument("-o", "--output", default=str(filename),
	help="output file save with ocr and translate")
	
ap.add_argument("-l", "--languagetesseract", default='ita',
	help="language input tesseract")
	
ap.add_argument("-d", "--destinationgoogletrans", default='it', 
	help="language destination googletrans")

args = vars(ap.parse_args())




# Imposta la lingua per l'OCR e la traduzione
pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'
lang = str(args["languagetesseract"])
translator = Translator()

# Carica l'immagine da processare
img = cv2.imread(str(args["input"]))

# Esegui OCR sull'immagine
text = pytesseract.image_to_string(img, lang=lang)

time.sleep(2)

detectlanguage = translator.detect(text)
# Traduci il testo
translated_text = translator.translate(text, dest=str(args["destinationgoogletrans"])).text

print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
print('              ')
print(translated_text)
print('              ')
print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
print('              ')
print(detectlanguage)
print('              ')
print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')

time.sleep(4)
# Crea una nuova immagine vuota
h, w, _ = img.shape

#new_img = Image.new('RGB', (w, h), (255, 255, 255))
new_img = img
# Crea un'istanza dell'oggetto Font OpenCV
font = cv2.FONT_HERSHEY_SIMPLEX

# Imposta la posizione iniziale del testo nella nuova immagine
x, y = 10, 50

# Itera attraverso ogni riga di testo e posiziona il testo tradotto nella nuova immagine
for line in translated_text.split('\n'):
    # Scrivi la riga di testo tradotto nella nuova immagine
    cv2.putText(new_img, line, (x, y), font, 1, (255, 0, 0), 2, cv2.LINE_AA)
    # Aggiorna la posizione y per la prossima riga di testo
    y += 50

# Salva la nuova immagine
#new_img.save('nuova_immagine.png')
cv2.imwrite(str(args["output"]), new_img)
time.sleep(12)

cv2.imshow("OUTPUT-TRANSLATE", new_img)
time.sleep(15)
#cv2.imshow("INPUT-IMAGE", img)
#time.sleep(15)
key = cv2.waitKey(1) & 0xFF
 
if key == ord("q"):
	cv2.destroyAllWindows()
