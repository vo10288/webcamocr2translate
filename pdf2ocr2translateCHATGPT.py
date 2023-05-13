import cv2
import pytesseract
from googletrans import Translator
from PIL import Image
import time

# Imposta la lingua per l'OCR e la traduzione
pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'
lang = 'ita'
translator = Translator()

# Carica l'immagine da processare
img = cv2.imread('immagine.png')

# Esegui OCR sull'immagine
text = pytesseract.image_to_string(img, lang=lang)

time.sleep(2)

# Traduci il testo
translated_text = translator.translate(text, dest='en').text
print(translated_text)

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
    cv2.putText(new_img, line, (x, y), font, 1, (0, 0, 0), 2, cv2.LINE_AA)
    # Aggiorna la posizione y per la prossima riga di testo
    y += 50

# Salva la nuova immagine
#new_img.save('nuova_immagine.png')
cv2.imwrite('nuova_immagine.png', new_img)
