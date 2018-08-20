# USAGE
# python classify.py --model fashion.model --labelbin mlb.pickle --image examples/example_01.jpg

# import the necessary packages
from keras.preprocessing.image import img_to_array
from keras.models import load_model
import numpy as np
import argparse
import imutils
import pickle
import imageio
import os
from skimage.transform import resize


# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-m", "--model", 
	default="../model_execution/sorting.model",help="path to trained model model")
ap.add_argument("-l", "--labelbin", 
	default="../model_execution/mlb.pickle", help="path to label binarizer")
ap.add_argument("-i", "--image", required=True,
	help="path to input image")
args = vars(ap.parse_args())

print("Parsed arguemtns");

# load the image
image = imageio.imread(args["image"])
output = imutils.resize(image, width=400)

print("Preprocessed image")

# pre-process the image for classification
image = resize(image, (96, 96), anti_aliasing=True)
image = image.astype("float") / 255.0
image = img_to_array(image)
image = np.expand_dims(image, axis=0)

# load the trained convolutional neural network and the multi-label
# binarizer

print("[INFO] loading network...")

model = load_model(args["model"])
mlb = pickle.loads(open(args["labelbin"], "rb").read())

# classify the input image then find the indexes of the two class
# labels with the *largest* probability

print("[INFO] classifying image...")

proba = model.predict(image)[0]



idxs = np.argsort(proba)[::-1][:3]



print("Indices: ", idxs)

# loop over the indexes of the high confidence class labels
for (i, j) in enumerate(idxs):
	# build the label
	label = "{}: {:.2f}%".format(mlb.classes_[j], proba[j] * 100)
	#with open("prediction.txt", "w") as myFile: 
	#	print(mlb.classes_[j], file=myFile)
	print(mlb.classes_[j])

