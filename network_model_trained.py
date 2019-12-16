import numpy as np
import tensorflow as tf
import pandas as pd

# Parametros de la red
num_input   = 6
n_hidden_1  = 10
n_hidden_2  = 10
num_classes = 2

def one_hot(a, num_classes):
    return np.squeeze(np.eye(num_classes)[a.reshape(-1)])

# Entrada de datos desde archivos xlsx
X_dataset = pd.read_excel('diabetes.xlsx')
Y_dataset = pd.read_excel('diabetes_out.xlsx')

X_dataset = np.array(X_dataset, dtype=np.double)
Y_dataset = np.array(Y_dataset)
Y_dataset = Y_dataset.reshape(Y_dataset.shape[0])

X_train = X_dataset[:500]
Y_train = Y_dataset[:500]
Y_train = one_hot(Y_train, num_classes)

X_test = X_dataset[500:]
Y_test = Y_dataset[500:]
Y_test = one_hot(Y_test, num_classes)

X = tf.placeholder("float", [None, num_input])

weights = {
	'w1' : tf.Variable(tf.random_normal([num_input, n_hidden_1])),
	'w2' : tf.Variable(tf.random_normal([n_hidden_1, n_hidden_2])),
	'out': tf.Variable(tf.random_normal([n_hidden_2, num_classes]))
}
biases  = {
	'b1'  : tf.Variable(tf.random_normal([n_hidden_1])),
	'b2'  : tf.Variable(tf.random_normal([n_hidden_2])),
	'out' : tf.Variable(tf.random_normal([num_classes]))
}

def neural_network(x):

	layer_1 = tf.add(tf.matmul(x, weights['w1']), biases['b1'])
	layer_1 = tf.nn.sigmoid(layer_1)
	layer_2 = tf.add(tf.matmul(layer_1, weights['w2']), biases['b2'])
	layer_2 = tf.nn.sigmoid(layer_2)
	out_layer = tf.add(tf.matmul(layer_2, weights['out']), biases['out'])

	return tf.nn.sigmoid(out_layer)

# Construyendo el modelo
logits = neural_network(X)

test= X_train[1].reshape(1, 6)

init = tf.global_variables_initializer()
saver = tf.train.Saver()

with tf.Session() as sess:
    sess.run(init)
    saver.restore(sess, 'my_net/trained_model.ckpt')
    print("Predict-: {}".format(sess.run(logits, feed_dict={X: test})))

