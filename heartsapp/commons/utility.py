import os
import logging

def format_logger(logger, log_dir_path, log_file_name):

	f_handler = logging.FileHandler(os.path.join(log_dir_path, log_file_name))
	c_handler = logging.StreamHandler()
	f_format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
	c_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
	f_handler.setFormatter(f_format)
	c_handler.setFormatter(c_format)
	c_handler.setLevel(logging.INFO)
	f_handler.setLevel(logging.INFO)
	logger.setLevel(logging.INFO)
	logger.addHandler(c_handler)
	logger.addHandler(f_handler)
	return logger
