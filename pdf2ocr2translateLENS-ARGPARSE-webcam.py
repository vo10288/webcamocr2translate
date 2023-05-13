import cv2
import pytesseract
from googletrans import Translator
from PIL import Image
import time
import argparse
from datetime import datetime
from imutils.video import VideoStream
from imutils.video import FPS
import numpy as np
import imutils
import os



filename = datetime.now().strftime("%Y_%m_%d_%H_%M_%S") +'.png'

ap = argparse.ArgumentParser()
#ap.add_argument("-i", "--input", default="immagine.png",
#	help="input file")

ap.add_argument("-v", "--video", default=0, 
	help="name of video")
	
ap.add_argument("-o", "--output", default='tempTranslate.png',#str(filename),
	help="output file save with ocr and translate")
	
ap.add_argument("-l", "--languagetesseract", default='ita',
	help="language input tesseract")
	
ap.add_argument("-d", "--destinationgoogletrans", default='it', 
	help="language destination googletrans")

ap.add_argument("-r", "--resolution", default=400, 
	help="resolution of output video")

args = vars(ap.parse_args())




# Imposta la lingua per l'OCR e la traduzione
pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'
lang = str(args["languagetesseract"])
translator = Translator()


if not os.path.exists('IMAGES'):
	os.makedirs('IMAGES')
					

#################
print("[INFO] starting video stream...")
vs = VideoStream(args["video"]).start()
time.sleep(1.0)
fps = FPS().start()

while True:

	try:
		img = vs.read()
		filename = datetime.now().strftime("%Y_%m_%d_%H_%M_%S") +'.png'

		#img = imutils.resize(frame, width=int(args["resolution"]))


################
# Carica l'immagine da processare
#img = cv2.imread(str(args["input"]))

		# Esegui OCR sull'immagine
		text = pytesseract.image_to_string(img, lang=lang)

		time.sleep(2)

		# Individua lingua
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
		time.sleep(3)
		
		cv2.imwrite('IMAGES/'+filename, new_img)
		time.sleep(3)


		cv2.imshow("OUTPUT-TRANSLATE", new_img)
		#time.sleep(15)
		#cv2.imshow("INPUT-IMAGE", img)
		#time.sleep(15)
		key = cv2.waitKey(1) & 0xFF
 
		if key == ord("q"):
			break
			cv2.destroyAllWindows()
 
		fps.update()
	except: pass

key = cv2.waitKey(1) & 0xFF
 
if key == ord("q"):
	cv2.destroyAllWindows()
	vs.stop()
	
