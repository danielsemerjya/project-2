from .models import User, Listing, Bid, Watch
from django.db.models import Max, F
import os
import cv2
import numpy as np
#from google.colab.patches import cv2_imshow
import imutils
import numpy

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')



def highest_bid(listing_id):
    # return highest bid query for input listing_id
    b = Bid.objects.annotate(
    highest=Max('listing_id__listing__price')
    ).filter(
    price=F('highest'))
    listing = Listing.objects.get(id=listing_id)
    
    for i in b:
        if i.listing_id == listing:
            b = i
    return b

def anonymize_face_pixelate(image, blocks=10):
# divide the input image into NxN blocks
    h, w = image.shape[:2]
    xSteps = np.linspace(0, w, blocks + 1, dtype="int")
    ySteps = np.linspace(0, h, blocks + 1, dtype="int")
    # loop over the blocks in both the x and y direction
    for i in range(1, len(ySteps)):
        for j in range(1, len(xSteps)):
            # compute the starting and ending (x, y)-coordinates
            # for the current block
            startX = xSteps[j - 1]
            startY = ySteps[i - 1]
            endX = xSteps[j]
            endY = ySteps[i]
            # extract the ROI using NumPy array slicing, compute the
            # mean of the ROI, and then draw a rectangle with the
            # mean RGB values over the ROI in the original image
            roi = image[startY:endY, startX:endX]
            (B, G, R) = [int(x) for x in cv2.mean(roi)[:3]]
            cv2.rectangle(image, (startX, startY), (endX, endY),
                (B, G, R), -1)
    # return the pixelated blurred image
    return image

def face_blurr(input):
    # Find face on photo and blurry them
    image_path = 'media/' + str(input)
    directory = r'media/images'

    img = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
    img = imutils.resize(img, width=600)
    #H,W_ = img.shape

    face_coord = face_cascade.detectMultiScale(img,1.2,10,minSize=(50,50))
    print('number of faces: ' + str(face_coord))

    if len(face_coord) == 0:
        pass
    elif len(face_coord) == 1:
        X, Y, w, h = face_coord[0]
        img_cp = img[Y:Y+h,X:X+w].copy()
        dst = anonymize_face_pixelate(img_cp)
        img[Y:Y+h,X:X+w] = dst

    ## If multiple faces are found take the one with largest area
    else:
        for (X, Y, w, h) in face_coord:
            img_cp = img[Y:Y+h,X:X+w].copy()
            dst = anonymize_face_pixelate(img_cp)
            img[Y:Y+h,X:X+w] = dst

    filename = str(input)[7:]
    print(filename)
    cv2.imwrite(os.path.join(directory , filename), img)
    cv2.waitKey(0)

    return img

