import mongoengine as mge

def default_connection():
	mge.connect("db_cdi", host="127.0.0.1", port=27017)