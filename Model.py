from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
import os
import os.path
import time
from hurry.filesize import size


class MyModel:
	"""
	This class contains the program state. (The Model)

	It provides methods to get, set, modify and evolve the state.

	Attributes:
		current_image   current image displayed
		image           list of images
		exif            dict of exif data of current image
		info            dict of general info of current image
	"""

	def __init__(self, name=None):
		"""
		Init method.

		Args:
			current_image    list of images
			image            current image displayed
		"""
		self.current_image = name
		self.images = []

	def update(self, name):
		"""
		Update the Model
		:param name: name of current image
		:return:
		"""
		self.current_image = name

	def fill_list(self, image):
		"""
		Insert image in list
		:param image: image to add to the list
		:return:
		"""
		for i in self.images:
			if i == image:
				return
		self.images.append(image)

	def get_element(self, position):
		"""
		Returns element of list at certain position
		:param position: position of image in list
		:return:
		"""
		current_element = self.images[position]
		self.update(current_element)

	def empty_list(self):
		"""
		Empty the list
		:return:
		"""
		del self.images[:]

	def delete_element(self, position):
		"""
		Delete image from list at certain position
		:param position: position of image in list
		:return:
		"""
		if self.images[position] == self.current_image:
			self.update("")
		self.images = [v for i,v in enumerate(self.images) if i != position]

	def get_list(self):
		"""
		Return the list of images
		:return: list of images
		"""
		return self.images

	def extract_exif_data(self, image):
		"""
		Extract exif data of image
		:param image: current image
		:return:
		"""
		self.exif = {}
		try:
			img = Image.open(image)
			if img.format != 'PNG':
				info = img._getexif()
			else:
				info = img.info
			for tag, value in info.items():
				decoded = TAGS.get(tag, tag)
				if decoded == "GPSInfo":
					gps_data = {}
					for t in value:
						sub_decoded = GPSTAGS.get(t, t)
						gps_data[sub_decoded] = value[t]
					self.exif[decoded] = gps_data
				else:
					self.exif[decoded] = value
		except AttributeError:
			print('Error with type of image')

	def get_exif(self):
		"""
		Return the exif data
		:return: exif data
		"""
		return self.exif

	def extract_general_info(self, image):
		"""
		Extract general info from image
		:param image: current image
		:return:
		"""
		self.info = {}
		try:
			img = Image.open(image)
			self.info['File name'] = os.path.basename(img.filename)
			self.info['Document type'] = img.format
			self.info['File size'] = size(os.stat(img.filename).st_size) + " (%5d bytes)" % os.stat(img.filename).st_size
			self.info['Creation date'] = time.ctime(os.path.getctime(img.filename))
			self.info['Modification date'] = time.ctime(os.path.getmtime(img.filename))
			self.info['Image size'] = img.size
			self.info['Color model'] = img.mode
		except AttributeError:
			print('Error with image')

	def get_general_info(self):
		"""
		Return general info of image
		:return: general info
		"""
		return self.info