# USAGE
#python classifier.py \--image 5.jpg
#Need to install keras, tensorflow, imutils, numpy, imageio

# import the necessary packages
from keras.preprocessing.image import img_to_array
from keras.models import load_model
from skimage.transform import resize
from keras import utils as np_utils
import numpy as np
import argparse
import imutils
import pickle
import imageio
import os

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-m", "--model", required=False,
	help="path to trained model model")
ap.add_argument("-l", "--labelbin", required=False,
	help="path to label binarizer")
ap.add_argument("-i", "--image", required=True,
	help="path to input image")
args = vars(ap.parse_args())

# load the image
image = imageio.imread(args["image"])
output = imutils.resize(image, width=400)

# pre-process the image for classification

image = resize(image, (224, 224), anti_aliasing=True)
image = image.astype("float") / 255.0
image = img_to_array(image)
image = np.expand_dims(image, axis=0)

# load the trained convolutional neural network and the multi-label
# binarizer
print("[INFO] loading network...")

#Load the model, the python file should be in the same directory as model, else specify the directory of model.
model = load_model("/mnt/efs/carspotting/classifier/test_model.h5")

#Load the class mapping, the python file should be in the same directory as class mapping, else specify the directory of class mapping.
mlb = pickle.loads(open("/mnt/efs/carspotting/classifier/class_mapping.txt", "rb").read())
#print(mlb)

# classify the input image then find the indexes of the two class
# labels with the *largest* probability
print("[INFO] classifying image...")
proba = model.predict(image)[0]
#print(proba)

idxs = np.argsort(proba)[::-1][:3]
#print(idxs)

for (i,j) in enumerate(idxs):
	label = "{}: {:.2f}%".format(mlb[j], proba[j] * 100)
	#print(label)
	a = mlb[j][1]
	head, sep, tail = a.partition(' ')
	print(head)
