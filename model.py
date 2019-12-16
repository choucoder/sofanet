import numpy as np
import pickle as pk
import datetime

# Parametros
num_input   = 6
n_hidden_1  = 10
n_hidden_2  = 8
num_classes = 2

def loadModel():
	return pk.load(open('model_trained.dat', 'rb'))

def restoreParameters(data):
	weights = {}
	biases = {}

	weights['w1'] = data['w1']
	weights['w2'] = data['w2']
	weights['out'] = data['wout']

	biases['b1'] = data['b1']
	biases['b2'] = data['b2']
	biases['out'] = data['bout']

	return weights, biases

def sigmoid(x):
	return 1 / (1 + np.exp(-x))

def forwardPropagation(x):
	data = loadModel()
	weights, biases = restoreParameters(data)

	layer_1 = np.dot(x, weights['w1']) + biases['b1']
	layer_1 = sigmoid(layer_1)
	layer_2 = np.dot(layer_1, weights['w2']) + biases['b2']
	layer_2 = sigmoid(layer_2)
	layer_out = np.dot(layer_2, weights['out']) + biases['out']

	return sigmoid(layer_out)

def predict(vector):
	resp = forwardPropagation(vector)
	print("resp: {}".format(resp))
	arg_max = np.argmax(resp)

	result = ""
	result2 = ""

	if arg_max == 0:
		result = "No tener diabetes"
		result2 = "Si tener diabetes"
	else:
		result = "Si tener diabetes"
		result2 = "No tener diabetes"

	return resp[arg_max], result, result2, arg_max

def edad(d):

	dif_y = datetime.datetime.now() - d
	return int(dif_y.days / 360)


#if __name__ == '__main__':
#	X = np.random.randn(1, num_input)
#	print("Predicción: {}".format(forwardPropagation(X)))
