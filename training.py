import numpy as np
import activation
import sys

initial_weights_file = input("Initial neural network text file for weights: \n");
training_set_file = input("Training set text file name: \n");
output_file = input("Results of training output file name: \n");
num_epochs = input("Enter the number of epochs: \n");
learning_rate = input("Enter the learning rate: \n");

num_epochs = int(num_epochs);
learning_rate = float(learning_rate);

initial_weights_file_handle = open(initial_weights_file, 'r')

# load in input file, get weights for input to hidden layer and hidden layer to output layer
for i, line in enumerate(initial_weights_file_handle):
    if i == 0:
        ni, nh, no = [ int(x) for x in line.split(' ') ]
        input_weights = np.zeros((nh, ni+1));
        hidden_weights = np.zeros((no, nh+1));
    elif i <= nh:
        #set the input weights to hidden layer
        input_weights[i-1] = [ float(x) for x in line.split(' ') ]
    else:
        #set the hidden layer's weights to output layer
        hidden_weights[i-nh-1] = [ float(x) for x in line.split(' ') ]

initial_weights_file_handle.close();

# load in test set

training_set_handle = open(training_set_file, 'r')

# load in test set, get features and labels
for i, line in enumerate(training_set_handle):
    if i == 0:
        num_test_examples, ni, no = [ int(x) for x in line.split(' ') ]
        features = np.zeros((num_test_examples, ni+1));
        labels = np.zeros((num_test_examples, no));
        temp = np.zeros((1, ni+no));
    else:
        #get features and labels
        temp = [ float(x) for x in line.split(' ') ]
        features[i-1,0] = -1;
        features[i-1,1:] = temp[0:ni];
        labels[i-1,:] = temp[ni:];

training_set_handle.close();

for _ in range(0, num_epochs): #unused variable name
    for i in range(0, features.shape[0]):

        temp1 = np.dot(features[i,:].reshape(1, ni+1),input_weights.T);
        temp2 = activation.sigmoid(temp1);
        temp3 = np.concatenate((np.zeros((temp2.shape[0],1))-1, temp2), axis=1);
        temp4 = np.dot(temp3,hidden_weights.T);
        temp5 = activation.sigmoid(temp4);

        hidden_layer_correction = activation.deriv_sigmoid(temp4)*(labels[i,:] - temp5);

        input_layer_correction = activation.deriv_sigmoid(temp1)*(np.dot(hidden_layer_correction,hidden_weights[:,1:]));

        hidden_weights += learning_rate*np.dot(temp3.T, hidden_layer_correction).T;

        input_weights += learning_rate*np.dot(features[i,:].reshape(1, ni+1).T, input_layer_correction).T;

output_file_handle = open(output_file, 'w')

temp_out = "%d %d %d\n" % (ni, nh, no);
output_file_handle.write(temp_out);

buf = "";
for i in range(nh):
    for j in range(features.shape[1]):
        temp_out = "%.3f " % (input_weights[i,j]);
        buf += temp_out;
    buf += "\n";
    output_file_handle.write(buf);
    buf = "";

for i in range(no):
    for j in range(hidden_weights.shape[1]):
        temp_out = "%.3f " % (hidden_weights[i,j]);
        buf += temp_out;
    buf += "\n";
    output_file_handle.write(buf);
    buf = "";

output_file_handle.close();
