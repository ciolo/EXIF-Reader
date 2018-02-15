from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
import os
import os.path, time
from hurry.filesize import size


class MyModel:

	def __init__(self, name=None):
		self.name = name

	def update(self, name):
		self.name = name

	def extract_exif(self, img):
		self.exif = {}
		self.image = Image.open(img)
		try:
			info = self.image._get_exif()
			for tag, value in info.items():
				decoded = TAGS.get(tag, tag)
				if decoded is not 'MakerNote':
					self.exif[decoded] = value
		except:
			pass
		return self.exif

	def get_exif_data(self, image):
		"""Returns a dictionary from the exif data of an PIL Image item. Also converts the GPS Tags"""
		self.exif = {}
		img = Image.open(image)
		try:
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
			print('PNG')

		return self.exif

	def get_info_general(self, image):
		self.info = {}
		try:
			img = Image.open(image)
			self.info['File name'] = os.path.basename(img.filename)
			self.info['Document type'] = img.format
			self.info['File size'] = size(os.stat(img.filename).st_size) + " (%5d bytes)" %os.stat(img.filename).st_size
			self.info['Creation date'] = time.ctime(os.path.getctime(img.filename))
			self.info['Modification date'] = time.ctime(os.path.getmtime(img.filename))
			self.info['Image size'] = img.size
			self.info['Color model'] = img.mode
		except AttributeError:
			print('Error with image')

		return self.info