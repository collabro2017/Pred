import numpy as np
import tensorflow as tf
import tarfile
import os

def csv_to_numpy_array(filePath, delimiter):
    return np.genfromtxt(filePath, delimiter=delimiter, dtype=None)

def import_data():
    if "data" not in os.listdir(os.getcwd()):
        # Untar directory of data if we haven't already
        tarObject = tarfile.open("data.tar.gz")
        tarObject.extractall()
        tarObject.close()
        print("Extracted tar to current directory")
    else:
        pass

    print("loading training data")
    trainX = csv_to_numpy_array("data/trainX.csv", delimiter="\t")
    trainY = csv_to_numpy_array("data/trainY.csv", delimiter="\t")
    print("loading test data")
    testX = csv_to_numpy_array("data/testX.csv", delimiter="\t")
    testY = csv_to_numpy_array("data/testY.csv", delimiter="\t")
    return trainX,trainY,testX,testY

trainX,trainY,testX,testY = import_data()

# Get our dimensions for our different variables and placeholders:
# numFeatures = the number of words extracted from each email
numFeatures = trainX.shape[1]
# numLabels = number of classes we are predicting (here just 2: ham or spam)
numLabels = trainY.shape[1]

#create a tensorflow session
sess = tf.Session()



X = tf.placeholder(tf.float32, [None, numFeatures])

yGold = tf.placeholder(tf.float32, [None, numLabels])


#all values must be initialized to a value before loading can occur

weights = tf.Variable(tf.zeros([numFeatures,numLabels]))

bias = tf.Variable(tf.zeros([1,numLabels]))


#since we don't have to train the model, the only Ops are the prediction operations

apply_weights_OP = tf.matmul(X, weights, name="apply_weights")
add_bias_OP = tf.add(apply_weights_OP, bias, name="add_bias")
activation_OP = tf.nn.sigmoid(add_bias_OP, name="activation")


correct_predictions_OP = tf.equal(tf.argmax(activation_OP,1),tf.argmax(yGold,1))

# False is 0 and True is 1, what was our average?
accuracy_OP = tf.reduce_mean(tf.cast(correct_predictions_OP, "float"))

# Initializes everything we've defined made above, but doesn't run anything
init_OP = tf.initialize_all_variables()

sess.run(init_OP)       #initialize variables BEFORE loading

#load variables from file
saver = tf.train.Saver()
saver.restore(sess, "trained_variables.ckpt")


#method for converting tensor label to string label
def labelToString(label):
    if np.argmax(label) == 0:
        return "ham"
    else:
        return "spam"

#make prediction on a given test set item
def predict(features, goldLabel):
    #run through graph
    tensor_prediction = sess.run(activation_OP, feed_dict={X: features.reshape(1, len(features)), yGold: goldLabel.reshape(1, len(goldLabel))})     
    prediction = labelToString(tensor_prediction)
    actual = labelToString(goldLabel)
    print("regression predicts email to be %s and is actually %s" %(prediction, actual))

if __name__ == "__main__":

    #show predictions and accuracy of entire test set
    prediction, evaluation = sess.run([activation_OP, accuracy_OP], feed_dict={X: testX, yGold: testY})

    for i in range(len(testX)):
        print("regression predicts email %s to be %s and is actually %s" %(str(i + 1), labelToString(prediction[i]), labelToString(testY[i])))
    print("overall accuracy of dataset: %s percent" %str(evaluation))