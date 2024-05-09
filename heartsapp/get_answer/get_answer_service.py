from get_answer import get_answer_pb2
from commons.utility import format_logger

import os
import logging
from time import time

import joblib
import numpy as np
import tensorflow as tf
import tensorflow_hub as hub

class GetAnswer:

	def __init__(self, config):

		module_url = config.get('module_url')
		data_path = config.get('data_path')
		emb_path = os.path.join(data_path, 'q_embs_new.pkl')
		dataset_path = os.path.join(data_path, 'final_ds.pkl')
		log_dir_path = os.path.join(data_path, 'logs')
		export_path = os.path.join(data_path, '1')
		self.threshold = config.get('threshold')
		self.top_k = config.get('top_k')
		self.metric = config.get('metric')
		self.input_node = config.get('input_node')
		self.output_node = config.get('output_node')
		self.do_normalize = config.get('normalize')
		self.sess = tf.Session()
		tf.saved_model.loader.load(self.sess, ['serve'], export_path)
		self.graph = tf.get_default_graph()
		self.dataset = joblib.load(dataset_path)
		self.logger = logging.getLogger('GetAnswerLogger')
		self.logger  = format_logger(self.logger, log_dir_path, 'GetAnswer.log')
		self.logger.info('GetAnswer API started !')
		if not os.path.exists(emb_path):
			print('Question embeddings not found, preparing embeddings!')
			st_time = time()
			self.q_embeddings = self.sess.run(self.output_node, feed_dict=\
									{self.input_node:[pair[0] for pair in self.dataset]})
			print('time taken to prepare embeddings -  {}'.format(time()-st_time))
			joblib.dump(self.q_embeddings, emb_path)
		else:
			self.q_embeddings = joblib.load(emb_path)

		if self.do_normalize:
			with self.graph.as_default():
				self.q_embeddings = tf.math.l2_normalize(tf.convert_to_tensor(self.q_embeddings), 0)
		else:
			with self.graph.as_default():
				self.q_embeddings = tf.convert_to_tensor(self.q_embeddings)

	def _cosine(self, x, y):
		with self.graph.as_default():
			y = tf.transpose(y)
			x_y = tf.matmul(x,y) # because norm(y, axis=1) == 1.0 for all rows
			return x_y

	def _select_above_threshold(self, x):
		return np.argwhere(x > self.threshold).squeeze()

	def _k_nearest_idxs(self, x):
		return np.argsort(x)[-1: -self.top_k-1: -1]

	def _nearest_neighbors(self, question):
		# NN graph opt node
		query_st_time = time()
		q_emb = self.graph.get_tensor_by_name(self.output_node)
		if self.metric == 'cosine':
			scores = self._cosine(q_emb, self.q_embeddings)
		else:
			raise NotImplementedError('{} metric not implemented'.format(self.metric))
		st_time = time()
		distances = self.sess.run(scores, feed_dict={self.input_node:[question]})
		distances = distances.reshape((distances.shape[1], ))
		self.logger.info('time taken to get distances -> {}'.format(time() - st_time))
		indexes = self._k_nearest_idxs(distances)
		self.logger.info('query time -> {}'.format(time()-query_st_time))
		return [(self.dataset[idx][0], self.dataset[idx][1], distances[idx]) for idx in indexes]