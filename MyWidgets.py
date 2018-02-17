from PyQt5.QtCore import Qt, QSize, QFileInfo
from PyQt5.QtWidgets import (QWidget, QLabel, QTabWidget, QTreeWidget, QTreeWidgetItem, QVBoxLayout, QListWidget,
							 QListWidgetItem, QSizePolicy)
from PyQt5.QtGui import QPixmap, QTransform, QIcon, QImage
from PIL import Image

class MyImageView(QLabel):
	"""
    Custom Widget to show image.

    Attributes:
        parent         reference to parent (Main Window)
        model          reference to an object of class MyModel (the model)
        viewer_list    reference to an object of class ImageFileList (list of images)
        rotation       value of rotation
        rotate         bool
    """
	def __init__(self, parent):
		"""
		Set several parameters and reference to parent
		:param parent:
		"""
		super(MyImageView, self).__init__(parent)
		self.parent = parent
		self.setAlignment(Qt.AlignCenter)
		self.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
		self.setAcceptDrops(True)
		self.rotation = 0
		self.rotate = False

	def set_model(self, model):
		"""
		Set the reference to the model and update the view
		:param model: the model
		:return:
		"""
		self.model = model
		self.update_view()

	def set_viewer_list(self, viewer_list):
		"""
		Set the reference to list of images
		:param viewer_list: list of images
		:return:
		"""
		self.viewer_list = viewer_list

	def update_view(self):
		"""
		Update the view of main image
		:return:
		"""
		if self.model.current_image and not self.rotate:
			self.qpix = QPixmap(self.model.current_image)
			self.setPixmap(self.qpix.scaled(QSize(min(self.size().width(),512), min(self.size().height(), 512)), Qt.KeepAspectRatio, Qt.FastTransformation))
		elif self.model.current_image and self.rotate:
			self.setPixmap(self.qpix.scaled(QSize(min(self.size().width(),512), min(self.size().height(), 512)), Qt.KeepAspectRatio, Qt.FastTransformation))
		elif not self.model.current_image:
			self.qpix = QPixmap()
			self.setPixmap(self.qpix)
			self.parent.extract_info.setEnabled(False)
			self.parent.left_rotate.setEnabled(False)
			self.parent.right_rotate.setEnabled(False)

	def left_rotate(self):
		"""
		Rotate the main image of 90 degrees to the left and update the view
		:return:
		"""
		self.rotate = True
		self.rotation -= 90

		transform = QTransform().rotate(self.rotation)
		self.qpix = self.qpix.transformed(transform, Qt.SmoothTransformation)

		self.update_view()
		self.rotation = 0

	def right_rotate(self):
		"""
		Rotate the main image of 90 degrees to the right and update the view
		:return:
		"""
		self.rotate = True
		self.rotation += 90

		transform = QTransform().rotate(self.rotation)
		self.qpix = self.qpix.transformed(transform, Qt.SmoothTransformation)


		self.update_view()
		self.rotation = 0

	def dragEnterEvent(self, e):
		"""
		Drag files directly onto the widget
		:param e:
		:return:
		"""
		if len(e.mimeData().urls()) > 0 and e.mimeData().urls()[0].isLocalFile():
			qi = QFileInfo(e.mimeData().urls()[0].toLocalFile())
			ext = qi.suffix()
			if ext == 'jpg' or ext == 'jpeg' or ext == 'png' or ext == 'JPG' or ext == 'PNG':
				e.accept()
			else:
				e.ignore()
		else:
			e.ignore()

	def dropEvent(self, e):
		"""
		Drop files directly onto the widget.
		File locations are stored in fname, update the model, fill the list of images,
		enable some buttons and populate the list
		:param e:
		:return:
		"""
		if self.rotate:
			self.rotate = False
		if e.mimeData().hasUrls:
			e.setDropAction(Qt.CopyAction)
			e.accept()

			for url in e.mimeData().urls():
				fname = str(url.toLocalFile())
				self.model.fill_list(fname)

			self.model.update(fname)
			self.set_model(self.model)
			self.parent.extract_info.setEnabled(True)
			self.parent.left_rotate.setEnabled(True)
			self.parent.right_rotate.setEnabled(True)
			self.viewer_list.populate()
		else:
			e.ignore()


class CustomTab(QWidget):
	"""
    Custom Widget to show info on image.

    Attributes:
        model          reference to an object of class MyModel (the model)
    """
	def __init__(self, parent, model):
		"""
		Set several parameters and reference to parent
		:param parent:
		:param model:
		"""
		super(CustomTab, self).__init__(parent)

		self.tab_widget = QTabWidget()
		self.tab_widget.setWindowTitle("More Info")
		self.tab_widget.setMinimumSize(500, 400)

		self.tab_info = QWidget()
		self.tab_exif = QWidget()

		self.tab_widget.addTab(self.tab_info, "Info")
		self.tab_widget.addTab(self.tab_exif, "Exif")

		self.tab_info_ui(model)
		self.tab_exif_ui(model)

	def tab_info_ui(self, model):
		"""
		Set the reference to model and set general info into widget
		:param model:
		:return:
		"""
		self.model = model
		general_info = self.model.get_general_info()

		layout = QVBoxLayout()
		if general_info:
			result_info = QTreeWidget()
			self.fill_widget(result_info, general_info)
			result_info.setHeaderLabel("Data")
		else: # if general info on current image is empty
			result_info = QLabel()
			result_info.setAlignment(Qt.AlignCenter)
			result_info.setText("No Info available for this file")

		layout.addWidget(result_info)

		self.tab_widget.setTabText(0, "General")
		self.tab_info.setLayout(layout)

	def tab_exif_ui(self, model):
		"""
		Set the reference to model and set exif data into widget
		:param model:
		:return:
		"""
		self.model = model
		exif = self.model.get_exif()

		layout = QVBoxLayout()

		if exif:
			result_exif = QTreeWidget()
			self.fill_widget(result_exif, exif)
			result_exif.setHeaderLabel("Data")
		else: # if general info on current image is empty
			result_exif = QLabel()
			result_exif.setAlignment(Qt.AlignCenter)
			result_exif.setText("No Exif available for this file")

		layout.addWidget(result_exif)

		self.tab_widget.setTabText(1, "Exif")
		self.tab_exif.setLayout(layout)

	def open_dict(self):
		"""
		Open tab widget to visualize info and exif on image
		:return:
		"""
		self.tab_widget.setWindowModality(True)
		self.tab_widget.show()

	def fill_widget(self, widget, value):
		"""
		Call function to fill the widget
		:param widget:
		:param value:
		:return:
		"""
		self.widget = widget
		self.widget.clear()
		self.fill_item(self.widget.invisibleRootItem(), value)

	def fill_item(self, item, value):
		"""
		Fill the widget with value (info or exif)
		:param widget:
		:param value:
		:return:
		"""
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
	"""
    Custom Widget to list of images.

    Attributes:
        parent         reference to parent (Main Window)
        model          reference to an object of class MyModel (the model)
        viewer         reference to an object of class MyImageView (main image)
    """
	def __init__(self, model, viewer, parent=None):
		"""
		Set several parameters and reference to parent, model and viewer
		:param model:
		:param viewer:
		:param parent:
		"""
		QListWidget.__init__(self, parent)
		self.setIconSize(QSize(100, 100))
		self.itemDoubleClicked.connect(self.upload_image)
		self.itemClicked.connect(self.activate_button_delete)
		self.setAcceptDrops(True)
		self.parent = parent
		self.model = model
		self.viewer = viewer
		self.parent.empty_list.clicked.connect(self.empty_list)
		self.parent.remove_item.clicked.connect(self.delete_item)

	def populate(self):
		"""
		Fill the list of images and set itself to viewer
		:return:
		"""

		# In case we're repopulating, clear the list
		self.clear()

		# Create a list item for each image file,
		# setting the text and icon appropriately
		for image in self.model.get_list():
			picture = Image.open(image)
			picture.thumbnail((72, 72), Image.ANTIALIAS)
			icon = QIcon(QPixmap.fromImage(QImage(picture.filename)))
			item = QListWidgetItem(self) # Insert the image in list
			item.setToolTip(image)
			item.setIcon(icon)

		if not self.parent.empty_list.isEnabled():
			self.parent.empty_list.setEnabled(True) # Enable buttons to empty the list
		self.viewer.set_viewer_list(self)

	def upload_image(self):
		"""
		If double click on image in list the image will displayed in main viewer. Update the view
		:return:
		"""
		if self.viewer.rotate:
			self.viewer.rotate = False
		self.current_item = self.currentRow()
		self.model.get_element(self.current_item) # Get image from model
		self.viewer.update_view()
		if not self.parent.extract_info.isEnabled():
			self.parent.extract_info.setEnabled(True)
			self.parent.left_rotate.setEnabled(True)
			self.parent.right_rotate.setEnabled(True)

	def empty_list(self):
		"""
		Empty the list and update model and view
		:return:
		"""
		self.model.empty_list()
		self.model.update("")
		self.clear()
		self.viewer.update_view()
		self.disable_button()

	def disable_button(self):
		"""
		Disable some buttons
		:return:
		"""
		self.parent.extract_info.setEnabled(False)
		self.parent.left_rotate.setEnabled(False)
		self.parent.right_rotate.setEnabled(False)
		self.parent.empty_list.setEnabled(False)
		self.parent.remove_item.setEnabled(False)

	def activate_button_delete(self):
		"""
		Activate button to remove an image from list and set the current image clicked in list
		:return:
		"""
		self.parent.remove_item.setEnabled(True)
		self.current_item = self.currentRow()

	def delete_item(self):
		"""
		Delete image from list and call model to delete image. Update the view
		:return:
		"""
		self.model.delete_element(self.current_item)
		self.takeItem(self.current_item)
		if self.current_item == 0 and not self.model.images:
			self.model.update("")
			self.disable_button()
		elif self.current_item != 0:
			self.current_item = self.current_item - 1
			self.setCurrentRow(self.current_item)

		self.viewer.update_view()

	def dragEnterEvent(self, e):
		"""
		Drag files directly onto the widget
		:param e:
		:return:
		"""
		if len(e.mimeData().urls()) > 0 and e.mimeData().urls()[0].isLocalFile():
			qi = QFileInfo(e.mimeData().urls()[0].toLocalFile())
			ext = qi.suffix()
			if ext == 'jpg' or ext == 'jpeg' or ext == 'png' or ext == 'JPG' or ext == 'PNG':
				e.accept()
			else:
				e.ignore()
		else:
			e.ignore()

	def dragMoveEvent(self, e):
		"""
		Necessary to activate drag and drop in this widget
		:param e:
		:return:
		"""
		if e.mimeData().hasUrls():
			e.setDropAction(Qt.CopyAction)
			e.accept()
		else:
			e.ignore()

	def dropEvent(self, e):
		"""
		Drop files directly onto the widget
		File locations are stored in fname. Fill the list and populate it. Call model to update it
		:param e:
		:return:
		"""
		if e.mimeData().hasUrls:
			e.setDropAction(Qt.CopyAction)
			e.accept()

			for url in e.mimeData().urls():
				fname = str(url.toLocalFile())
				self.model.fill_list(fname)
			self.populate()
		else:
			e.ignore()
