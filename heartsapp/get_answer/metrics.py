import tensorflow as tf
import numpy as np


# UNDER CONSTRUCTION
class TFMetrics:

	def __init__(self,):
		pass

	def _cosine_similarity(self, x, y):
			return tf.math.subtract([1.0] , tf.abs(tf.math.divide(tf.reduce_sum(tf.matmul(x,y), 1),\
													tf.math.multiply(tf.reduce_sum(x),tf.reduce_sum(y)))))

	def _l1_metric(self, x, y):

		return tf.reduce_sum(tf.abs(tf.add(x, tf.transpose(tf.math.negative(y)))), 1)

	def _l2_metric(self, x, y):

		return tf.math.sqrt(tf.reduce_sum(tf.math.square(tf.math.subtract(x, tf.transpose(y))), 1))


def cosine_similarity(x, y):

	return np.dot(x,y)/(np.linalg.norm(x)*np.linalg.norm(y))

def l1_metric(x, y):
	pass

def l2_metric(x, y):
	pass