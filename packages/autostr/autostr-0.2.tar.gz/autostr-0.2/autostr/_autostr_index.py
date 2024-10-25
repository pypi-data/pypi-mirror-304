def autostr(cls):
	cls_attribute = [item for item in cls.__dict__ if not item.startswith('__')]
	ins_attribute = cls.__init__.__code__.co_names if '__code__' in dir(cls.__init__) else ()

	def print_args(self, *, ins_args, cls_attr):
		result_str = f"""Instance of the class: {self.__class__.__name__}\n\n"""

		if len(cls_attr) > 0:
			result_str += "Class attributes:\n"
			for attr in cls_attr:
				result_str += f'·{attr}: {self.__getattribute__(attr)} \n'
			result_str += '\n'

		if len(ins_args) > 0:
			result_str += "Instance attributes:\n"
			for attr in ins_args:
				result_str += f'·{attr}: {self.__getattribute__(attr)} \n'

		return result_str

	def __str__(self):
		return print_args(
			self,
			ins_args=ins_attribute,
			cls_attr=cls_attribute
		)

	cls.__str__ = __str__
	return cls



