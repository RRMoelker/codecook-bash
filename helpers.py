# -*- coding: utf-8 -*-

def singleton(cls):
	"""
	singleton class decorator
		overwrites class with function that creates a instance of class.
	"""
	instances = {}
	def getinstance():
		if cls not in instances:
			instances[cls] = cls()
		return instances[cls]
	return getinstance