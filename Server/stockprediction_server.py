"""Execute using
export FLASK_APP=stockprediction_server.py
python -m flask run
"""
# Import
import tensorflow as tf
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
from flask import Flask
from flask_cors import CORS
from flask import request, jsonify
import json
app = Flask(__name__)
CORS(app)

# Import data
data = pd.read_csv('data/AmericanAirlines.csv')
print data.head(10)

# Drop date variable
data = data.drop(['DATE'], 1)

# Dimensions of dataset
n = data.shape[0]
p = data.shape[1]

# Make data a np.array
data = data.values

# Training and test data
train_start = 0
train_end = int(np.floor(0.8*n))
test_start = train_end + 1
test_end = n
data_train = data[np.arange(train_start, train_end), :]
data_test = data[np.arange(test_start, test_end), :]

# Scale data
#scaler = MinMaxScaler(feature_range=(-1, 1))
#scaler.fit(data_train)
#data_train = scaler.transform(data_train)
#data_test = scaler.transform(data_test)

# Build X and y
X_train = data_train[:, 1:]
y_train = data_train[:, 0]
X_test = data_test[:, 1:]
y_test = data_test[:, 0]

# Number of stocks in training data
n_stocks = X_train.shape[1]

# Neurons
n_neurons_1 = 1024
n_neurons_2 = 512
n_neurons_3 = 256
n_neurons_4 = 128

# Session
net = tf.InteractiveSession()

# Placeholder
X = tf.placeholder(dtype=tf.float32, shape=[None, n_stocks])
Y = tf.placeholder(dtype=tf.float32, shape=[None])

# Initializers
sigma = 1
weight_initializer = tf.variance_scaling_initializer(mode="fan_avg", distribution="uniform", scale=sigma)
bias_initializer = tf.zeros_initializer()

# Hidden weights
W_hidden_1 = tf.Variable(weight_initializer([n_stocks, n_neurons_1]))
bias_hidden_1 = tf.Variable(bias_initializer([n_neurons_1]))
W_hidden_2 = tf.Variable(weight_initializer([n_neurons_1, n_neurons_2]))
bias_hidden_2 = tf.Variable(bias_initializer([n_neurons_2]))
W_hidden_3 = tf.Variable(weight_initializer([n_neurons_2, n_neurons_3]))
bias_hidden_3 = tf.Variable(bias_initializer([n_neurons_3]))
W_hidden_4 = tf.Variable(weight_initializer([n_neurons_3, n_neurons_4]))
bias_hidden_4 = tf.Variable(bias_initializer([n_neurons_4]))

# Output weights
W_out = tf.Variable(weight_initializer([n_neurons_4, 1]))
bias_out = tf.Variable(bias_initializer([1]))

# Hidden layer
hidden_1 = tf.nn.relu(tf.add(tf.matmul(X, W_hidden_1), bias_hidden_1))
hidden_2 = tf.nn.relu(tf.add(tf.matmul(hidden_1, W_hidden_2), bias_hidden_2))
hidden_3 = tf.nn.relu(tf.add(tf.matmul(hidden_2, W_hidden_3), bias_hidden_3))
hidden_4 = tf.nn.relu(tf.add(tf.matmul(hidden_3, W_hidden_4), bias_hidden_4))

# Output layer (transpose!)
out = tf.transpose(tf.add(tf.matmul(hidden_4, W_out), bias_out))

# Cost function
mse = tf.reduce_mean(tf.squared_difference(out, Y))

# Optimizer
opt = tf.train.AdamOptimizer().minimize(mse)

# Init
net.run(tf.global_variables_initializer())

# Setup plot
plt.ion()
fig = plt.figure()
ax1 = fig.add_subplot(111)
line1, = ax1.plot(y_test)
line2, = ax1.plot(y_test * 0.5)
plt.show()

# Fit neural net
batch_size = 256
mse_train = []
mse_test = []
trend_predict = []	#1 - up, -1 - down
check_trend = []	#1 - correctly predicted, -1 - incorrectly predicted

# Run
epochs = 2
for e in range(epochs):

    # Shuffle training data
    shuffle_indices = np.random.permutation(np.arange(len(y_train)))
    X_train = X_train[shuffle_indices]
    y_train = y_train[shuffle_indices]

    # Minibatch training
    for i in range(0, len(y_train) // batch_size):
        start = i * batch_size
        batch_x = X_train[start:start + batch_size]
        batch_y = y_train[start:start + batch_size]
        # Run optimizer with batch
        net.run(opt, feed_dict={X: batch_x, Y: batch_y})

        # Show progress
        if np.mod(i, 50) == 0:
	    correct = 0
            # MSE train and test
            mse_train.append(net.run(mse, feed_dict={X: X_train, Y: y_train}))
            mse_test.append(net.run(mse, feed_dict={X: X_test, Y: y_test}))
            print('MSE Train: ', mse_train[-1])
            #print('MSE Test: ', mse_test[-1])
            # Prediction
            #pred = net.run(out, feed_dict={X: X_test})
            #line2.set_ydata(pred)
	    #for i in range(pred.size):
	    #	if(((pred[0][i] > X_test[i][4]) and (y_test[i] > X_test[i][4])) or ((pred[0][i] < X_test[i][4]) and (y_test[i] < X_test[i][4]))):
	    #		correct = correct + 1
	    #print "Correctly trend predicted" + str(correct)
	    #print "Incorrectly trend predicted" + str(pred.size - correct)
            #plt.title('Epoch ' + str(e) + ', Batch ' + str(i))
            #plt.pause(0.01)

@app.route('/getInitial')
def sendInitial():
	initialData = {}
	predictedDataStock1 = []
	actualDataStock1 = []
	predictedDataStock2 = []
	actualDataStock2 = []
	trend = []
	isCorrectlyPredicted = []
	percentChange = []
	pred = net.run(out, feed_dict={X: X_test})
	for i in range(0,501):
		predictedDataStock1.append(str(pred[0][i]))
		actualDataStock1.append(str(y_test[i]))
		predictedDataStock2.append(str(pred[0][i]))
		actualDataStock2.append(str(y_test[i]))
		if(pred[0][i] > X_test[i][4]):
			trend.append(str(1))
		else:
			trend.append(str(-1))
		if((y_test[i] > X_test[i][4] and pred[0][i] > X_test[i][4]) or (y_test[i] < X_test[i][4] and pred[0][i] < X_test[i][4])):
			isCorrectlyPredicted.append(str(1))
		else:
			isCorrectlyPredicted.append(str(-1))
		percentChange.append(str(((pred[0][i - 1] - X_test[i][4])/ X_test[i][4]) * 100))

	initialData['predictedDataStock1'] = predictedDataStock1
	initialData['actualDataStock1'] = actualDataStock1
	initialData['predictedDataStock2'] = predictedDataStock2
	initialData['actualDataStock2'] = actualDataStock2
	initialData['isCorrectlyPredicted'] = isCorrectlyPredicted
	initialData['percentChange'] = percentChange
	response = jsonify(initialData)
	response.headers.add('Access-Control-Allow-Origin', '*')
	return response

@app.route('/getUpdate')
def sendupdate():
	initialData2 = {}
	index = int(request.args.get('i'))
	pred = net.run(out, feed_dict={X: X_test})
	print index
	if(pred[0][index] > X_test[index][4]):
		trend = 1
	else:
		trend = -1
	if((y_test[index] > X_test[index][4] and trend == 1) or (y_test[index] < X_test[index][4] and trend == -1)):
		isCorrectlyPredicted = 1
	else:
		isCorrectlyPredicted = -1
	print	str(pred[0][index])
	#return "Predicted " + str(pred[0][index]) + " Actual " +str(y_test[index]) + "Previous stock value " + str(X_test[index][4]) + " Trend " + str(trend) + " isCorrectlyPredicted " + str(isCorrectlyPredicted)
	initialData2['predictedDataStock1'] = str(pred[0][index])
	initialData2['actualDataStock1'] = str(X_test[index][4])
	initialData2['predictedDataStock2'] = str(pred[0][index])
	initialData2['actualDataStock2'] = str(X_test[index][4])
	initialData2['isCorrectlyPredicted'] = str(isCorrectlyPredicted)
	initialData2['percentChange'] = str(((pred[0][index - 1] - X_test[index][4])/ X_test[index][4]) * 100)
	response = jsonify(initialData2)
	response.headers.add('Access-Control-Allow-Origin', '*')
	return response
app.run(host = '0.0.0.0')
