# Model Execution

## First Working Prototype

- For our first working prototype, we took a model which is being used for sorting of car images.
- The model is able to succesfully detect whether the images are of front view of cars or back view of cars or side views.
- We tweaked the classifier in a way that the classifier will receive an image file and returns the label for which it got maximum probability
- The classifier expects name of the image, name of the trained model and the name of the multilabel binarizer.
- Model and the multi label binarizer is being set as default.
- Sample invocation of the script - "python classify.py \--image examples/5.jpg"

## Second Working Prototype
- For our second working type, we received working model test_model.h5.
- Our classifier got the labels and their probabilities from the model
- Sort the probabilities and got the best probability. 
- Choose the label corresponding to the probability
- Take the first string from the label to pass it to the web page.
