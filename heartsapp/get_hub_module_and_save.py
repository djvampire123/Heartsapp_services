import os
import tensorflow as tf
import tensorflow_hub as hub

import json

with open(os.path.abspath('heartsapp/config.json'), 'r') as f:
    config = json.load(f)

module_url = config.get('module_url')
export_path = os.path.join(config.get('data_path'), '1')

with tf.Graph().as_default():
    embedder = hub.Module(module_url)
    text = tf.placeholder(tf.string, [None])
    embedding = embedder(text)

    init_op = tf.group([tf.global_variables_initializer(), tf.tables_initializer()])
    with tf.Session() as session:
        session.run(init_op)
        tf.saved_model.simple_save(
            session,
            export_path,
            inputs = {"text": text},
            outputs = {"embedding": embedding},
            legacy_init_op = tf.tables_initializer()        
        )