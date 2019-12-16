import tensorflow as tf
import numpy as np
import pandas as pd
import pickle as pk

# Parametros
learning_rate = 0.01
num_steps     = 10000
batch_size    = 128
display_step  = 100


# Parametros de la red
num_input   = 6
n_hidden_1  = 10
n_hidden_2  = 8
num_classes = 2

# Grafo de entrada con Placeholder
X = tf.placeholder("float", [None, num_input])
Y = tf.placeholder("float", [None, num_classes])

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

print(X_train.shape)
print(Y_train.shape)

test = X_train[1].reshape(1, 6)

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

# Crear Modelo
def neural_network(x):

	layer_1 = tf.add(tf.matmul(x, weights['w1']), biases['b1'])
	layer_1 = tf.nn.sigmoid(layer_1)
	layer_2 = tf.add(tf.matmul(layer_1, weights['w2']), biases['b2'])
	layer_2 = tf.nn.sigmoid(layer_2)
	out_layer = tf.add(tf.matmul(layer_2, weights['out']), biases['out'])

	return tf.nn.sigmoid(out_layer)

def saveModel(dic_w, dic_b, session):
    w1 = dic_w['w1'].eval(session)
    w2 = dic_w['w2'].eval(session)
    wout = dic_w['out'].eval(session)

    b1 = dic_b['b1'].eval(session)
    b2 = dic_b['b2'].eval(session)
    bout = dic_b['out'].eval(session)

    data = {}

    data['w1'] = w1
    data['w2'] = w2
    data['wout'] = wout
    data['b1'] = b1
    data['b2'] = b2
    data['bout'] = bout

    pk.dump(data, open('model_trained.dat', 'wb'))

# Construyendo el modelo
logits = neural_network(X)
data = {}

# Definir la funcion de perdida
# y el optimizador a utilizar
loss_op = tf.sqrt(tf.reduce_mean(tf.square(tf.subtract(Y, logits))))
optimizer = tf.train.GradientDescentOptimizer(learning_rate=learning_rate)
train_op  = optimizer.minimize(loss_op)

# Evaluar el modelo
correct_pred = tf.equal(tf.argmax(logits, 1), tf.argmax(Y, 1))
accuracy = tf.reduce_mean(tf.cast(correct_pred, tf.float32))

init = tf.global_variables_initializer()
saver = tf.train.Saver()

# Comenzar el entrenamiento
with tf.Session() as sess:
	sess.run(init)
	# Epocas de entrenamiento
	for step in range(1, num_steps + 1):
		# Leer X_train y Y_train
		batch_x, batch_y = X_train, Y_train
		# Correr el optimizador(backpropagation)
		sess.run(train_op, feed_dict={X: batch_x, Y: batch_y})

		if step % display_step == 0 or step == 1:
			# Calcula la perdida de los lotes y exactitud
			loss, acc = sess.run([loss_op, accuracy], feed_dict={
			X: batch_x, Y: batch_y})

			print("Paso "+ str(step) + ", Minibach Loss= "+\
				"{:.4f}".format(loss) + ", Training Accuracy="+\
				"{:.3f}".format(acc))

	print("Optimizacion Finalizada")
	saveModel(weights, biases, sess)
	saver.save(sess, 'my_net/trained_model.ckpt')


	# Calcular exactitud para test_set
	print("Testeando Accuracy:", \
		sess.run(accuracy, feed_dict={X: X_test, Y: Y_test}))

	print("Tensor: {}".format(sess.run(weights['w1'])))

