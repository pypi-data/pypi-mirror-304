class Dict(dict):
	def __init__(self, *args, **kwargs):
		super(Dict, self).__init__(*args, **kwargs)
		self.__dict__ = self