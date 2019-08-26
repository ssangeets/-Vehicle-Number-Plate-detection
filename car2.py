import cv2
import json
import io

from skimage import io
import imutils

import os
os.environ['OPENCV_IO_MAX_IMAGE_PIXELS']=str(2**64)

import pytesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
print("Enter position of image which you want to see ")
b=int(input())

a=[]
with open('plate.json') as f:
    for line in f:
        a.append(json.loads(line))
image = io.imread(a[b]['content'])
image=cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

#RGS 10 Gray scale conversion
gray= cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


gray= cv2.bilateralFilter(gray,11,17,17)



#edges
edged= cv2.Canny(gray,170,200)


#contours
cnts, new =cv2.findContours(edged.copy(),cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)


#create copy
img1=image.copy()
cv2.drawContours(img1,cnts,-1,(0,255,0),3)


cnts=sorted(cnts,key=cv2.contourArea,reverse=True)[:30]
NumberPlateCnt = None #No Number plate


img2 = image.copy()
cv2.drawContours(img2,cnts,-1,(0,255,0),3)


#0op over our contours to find the best possible approximate contour i nter pista
count=0
idx=7
for c in cnts:
    peri= cv2.arcLength (c, True)
    approx = cv2.approxPolyDP(c, 0.02* peri, True)
#" approx-", approx)

    if len(approx)== 4: # Select the contour with 4 Corners
        NumberPlateCnt = approx #This la94E 409EO Nuse Places Contour

    #Crops those concours and store it in Cropped Images older
        x,y,w,h = cv2.boundingRect (c) #Th a ngout CO-OOO
        new_img= image[y:y+ h, x:x+w] #ears, Dekage
        cv2.imwrite('Car4/' + str(idx) +'.png', new_img) #Stere.new amoge
        idx+=1

        break


#Drawing the selected contour on the original image
#print (underPlating
cv2.drawContours(image, [NumberPlateCnt], -1 ,(0,255,0),3)


Cropped_img_loc = 'Car4/7.png'


#Use tesseract to convert image into string
text=''
text = pytesseract.image_to_string(Cropped_img_loc,config = '--psm 6')
print("Number is :",text)

