from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import (QWidget, QLabel, QTabWidget, QTreeWidget, QTreeWidgetItem, QVBoxLayout, QListWidget, QListWidgetItem, QSizePolicy)
from PyQt5.QtGui import QPixmap, QTransform, QIcon, QImageReader
import os
from os import listdir, walk
from os.path import isfile, join
import glob
from PIL import Image
from PIL.ImageQt import ImageQt

class MyImageView(QLabel):
	def __init__(self):
		super().__init__()
		self.setAlignment(Qt.AlignCenter)
		self.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
		self.V_margin = 0
		self.H_margin = 0
		self.rotation = 0

	def set_model(self, model):
		self.model = model
		self.update_view()

	def update_view(self):
		self.qpix = QPixmap(self.model.name)
		self.setPixmap(self.qpix.scaled(self.size(), Qt.KeepAspectRatio, Qt.FastTransformation))

		self.V_margin = (self.size().height() - self.pixmap().size().height()) / 2
		self.H_margin = (self.size().width() - self.pixmap().size().width()) / 2

	def left_rotate(self):
		self.rotation -= 90

		transform = QTransform().rotate(self.rotation)
		self.qpix = self.qpix.transformed(transform, Qt.SmoothTransformation)

		# ---- update label ----

		self.setPixmap(self.qpix)
		#self.update_view()

	def right_rotate(self):
		self.rotation += 90

		transform = QTransform().rotate(self.rotation)
		self.qpix = self.qpix.transformed(transform, Qt.SmoothTransformation)

		# ---- update label ----

		self.setPixmap(self.qpix)
		#self.update_view()


class CustomTab(QWidget):
	def __init__(self, parent, exif, general):
		super(CustomTab, self).__init__(parent)

		self.tab_widget = QTabWidget()
		self.tab_widget.setWindowTitle("More Info")
		self.tab_widget.setMinimumSize(500, 400)

		self.tab_info = QWidget()
		self.tab_exif = QWidget()

		self.tab_widget.addTab(self.tab_info, "Info")
		self.tab_widget.addTab(self.tab_exif, "Exif")

		self.tab_info_ui(general)
		self.tab_exif_ui(exif)

	def tab_info_ui(self, general):
		self.general_info = general

		layout = QVBoxLayout()

		self.info_dict = QTreeWidget()
		self.info_dict.setHeaderLabel("Data")
		layout.addWidget(self.info_dict)

		self.fill_widget(self.info_dict, self.general_info)

		self.tab_widget.setTabText(0, "General")
		self.tab_info.setLayout(layout)

	def tab_exif_ui(self, exif):
		self.exif = exif

		layout = QVBoxLayout()

		if self.exif:
			self.result_exif = QTreeWidget()
			self.fill_widget(self.result_exif, self.exif)
			self.result_exif.setHeaderLabel("Data")
		else:
			self.result_exif = QLabel()
			self.result_exif.setAlignment(Qt.AlignCenter)
			self.result_exif.setText("No Exif available for this file")

		layout.addWidget(self.result_exif)

		self.tab_widget.setTabText(1, "Exif")
		self.tab_exif.setLayout(layout)

	def open_dict(self):
		self.tab_widget.show()

	def fill_widget(self, widget, value):
		self.widget = widget
		self.widget.clear()
		self.fill_item(self.widget.invisibleRootItem(), value)

	def fill_item(self, item, value):
		item.setExpanded(True)
		if type(value) is dict:
			for key, val in value.items():
				child = QTreeWidgetItem()
				child.setText(0, str(key))
				item.addChild(child)
				self.fill_item(child, val)
		elif type(value) is list:
			for val in value:
				child = QTreeWidgetItem()
				item.addChild(child)
				if type(val) is dict:
					child.setText(0, '[dict]')
					self.fill_item(child, val)
				elif type(val) is list:
					child.setText(0, '[list]')
					self.fill_item(child, val)
				else:
					child.setText(0, str(val))
					child.setExpanded(True)
		else:
			child = QTreeWidgetItem()
			child.setText(0, str(value))
			item.addChild(child)


class ImageFileList(QListWidget):
	''' A specialized QListWidget that displays the
		list of all image files in a given directory. '''

	def __init__(self, dirpath, parent=None):
		QListWidget.__init__(self, parent)
		self.setDirpath(dirpath)
		self.setIconSize(QSize(100, 100))
		self.setAcceptDrops(True)

	def setDirpath(self, dirpath):
		''' Set the current image directory and refresh the list. '''
		self._dirpath = dirpath
		self._populate()

	def _images(self):
		''' Return a list of filenames of all
			supported images in self._dirpath. '''

		# Start with an empty list
		images = ['/Users/albertociolini/Desktop/Test/test2.JPG', '/Users/albertociolini/Desktop/Test/test.png',
				  '/Users/albertociolini/Desktop/Test/puzzle.png', '/Users/albertociolini/Desktop/Test/Modulo.JPG',
				  '/Users/albertociolini/Desktop/Test/IMG_0847.JPG', '/Users/albertociolini/Desktop/Test/fototessera1.JPG',
				  '/Users/albertociolini/Desktop/Test/Modulo1.JPG']

		# Find the matching files for each valid
		# extension and add them to the images list
		"""for extension in QImageReader.supportedImageFormats():
			pattern = os.path.join(self._dirpath, '*.%s' % extension)
			images.extend(glob.glob(pattern))"""
		onlyfiles = [f for f in listdir(self._dirpath) if isfile(join(self._dirpath, f))]
		f = []
		for (dirpath, dirnames, filenames) in walk(self._dirpath):
			f.extend(filenames)
			break
		files = listdir(self._dirpath)
		for name in files:
			print(name)

		return images

	def _populate(self):
		''' Fill the list with images from the
			current directory in self._dirpath. '''

		# In case we're repopulating, clear the list
		self.clear()

		# Create a list item for each image file,
		# setting the text and icon appropriately
		for image in self._images():
			picture = Image.open(image)
			picture.thumbnail((72, 72), Image.ANTIALIAS)
			icon = QIcon(QPixmap.fromImage(ImageQt(picture)))
			#item = QListWidgetItem(os.path.basename(image)[:20] + "...", self.pictureListWidget)
			item = QListWidgetItem(self)
			item.setStatusTip(image)
			#item.setText(image)
			item.setIcon(icon)
