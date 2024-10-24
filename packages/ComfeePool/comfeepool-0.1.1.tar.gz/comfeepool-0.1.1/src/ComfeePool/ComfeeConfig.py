from configparser import ConfigParser

class ComfeeConfig():
	"""A class to handle reading configurations from a configuration file."""

	def __init__(self, filename='config.cfg'):
		"""Initialize the configuration parser.

		Args:
		    filename (str): Name of the configuration file to read from.
		"""
		self.parser = ConfigParser(interpolation=None)
		self.filename = filename
		self.parser.read(filename)
		

	def read(self, section='section'):
		"""Read the configuration for a specific section.

		Args:
		    section (str): Section of the configuration to read.

		Returns:
		    dict: Dictionary containing the configuration parameters.

		Raises:
		    Exception: If the section is not found in the configuration file.
		"""
		cfg = {}
		if self.parser.has_section(section):
			params = self.parser.items(section)
			for param in params:
				cfg[param[0]] = param[1]
		else:
			raise Exception('Section {0} not found in the {1} file'.format(section, self.filename))

		return cfg
