from PyQt5.QtWidgets import (QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QFileDialog, QMessageBox,
							 QDesktopWidget, QListView)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize
from MyWidgets import CustomTab, MyImageView, ImageFileList


class MainWindow(QWidget):
	"""
    Main window controller

    Attributes:
        model         reference to an object of class MyModel (the model)
        viewer        reference to an object of class MyImageView (main image)
        viewer_list   reference to an object of class ImageFileList (list of images)
        ...some graphical elements
    """

	def __init__(self, model):
		super().__init__()

		self.model = model

		self.initUI()
		self.center_on_screen()

	def initUI(self):
		"""Method to initialize the UI: layouts and components"""
		self.setWindowTitle("Exif Reader")

		self.load = QPushButton()
		self.load.setText("Add Photo")
		self.load.clicked.connect(self.load_image_but)

		self.extract_info = QPushButton()
		self.extract_info.setEnabled(False)
		self.extract_info.setText("Get Info")
		self.extract_info.clicked.connect(self.open_info)

		self.empty_list = QPushButton()
		self.empty_list.setEnabled(False)
		self.empty_list.setText("Empty List")

		self.remove_item = QPushButton()
		self.remove_item.setEnabled(False)
		self.remove_item.setText("Remove Item")

		self.left_rotate = QPushButton()
		self.left_rotate.setEnabled(False)
		self.left_rotate.setIcon(QIcon('IconImage/rotate_left.png'))
		self.left_rotate.setIconSize(QSize(24, 24))
		self.left_rotate.clicked.connect(self.fnleft_rotate)

		self.right_rotate = QPushButton()
		self.right_rotate.setEnabled(False)
		self.right_rotate.setIcon(QIcon('IconImage/rotate_right.png'))
		self.right_rotate.setIconSize(QSize(24, 24))
		self.right_rotate.clicked.connect(self.fnright_rotate)

		self.viewer = MyImageView(self)
		self.viewer.resize(800, 600)
		self.viewer.set_model(self.model)

		self.viewer_list = ImageFileList(self.model, self.viewer, self)
		self.viewer_list.setFlow(QListView.LeftToRight)
		self.viewer_list.setMaximumHeight(120)

		self.viewer.set_viewer_list(self.viewer_list)

		top_h_box = QHBoxLayout()
		top_h_box.addWidget(self.load)
		top_h_box.addWidget(self.extract_info)
		top_h_box.addStretch()
		top_h_box.addWidget(self.left_rotate)
		top_h_box.addWidget(self.right_rotate)

		bottom_button_box = QVBoxLayout()
		bottom_button_box.addWidget(self.empty_list)
		bottom_button_box.addWidget(self.remove_item)

		bottom_h_box = QHBoxLayout()
		bottom_h_box.addWidget(self.viewer_list)
		bottom_h_box.addLayout(bottom_button_box)

		layout = QVBoxLayout()
		layout.addLayout(top_h_box)
		layout.addWidget(self.viewer)
		layout.addLayout(bottom_h_box)

		self.setLayout(layout)

		self.setMinimumSize(600, 500)
		self.show()

	def center_on_screen(self):
		"""
		Centers main window
		:return:
		"""
		qt_rectangle = self.frameGeometry()
		center_point = QDesktopWidget().availableGeometry().center()
		qt_rectangle.moveCenter(center_point)
		self.move(qt_rectangle.topLeft())

	def resizeEvent(self, ev):
		"""Slot for window resize event (Override)"""
		self.viewer.update_view()
		super().resizeEvent(ev)

	def open_info(self):
		"""
		Open tab to visualize general info and exif data
		:return:
		"""
		self.model.extract_general_info(self.model.current_image)
		self.model.extract_exif_data(self.model.current_image)
		self.custom_tab = CustomTab(self, self.model)
		self.custom_tab.open_dict()

	def load_image_but(self):
		"""
		Open a File dialog when the button is pressed
		Update the model, fill and populate the list.
		:return:
		"""
		options = QFileDialog.Options()
		options |= QFileDialog.DontUseNativeDialog
		filename, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
												  "Images (*.jpg *.jpeg *.png *.JPG *.PNG)",
												  options=options)

		if filename:
			self.extract_info.setEnabled(True)
			self.left_rotate.setEnabled(True)
			self.right_rotate.setEnabled(True)
			self.empty_list.setEnabled(True)
			self.model.update(filename)
			self.model.fill_list(filename)
			if self.viewer.rotate:
				self.viewer.rotate = False
			self.viewer.set_model(self.model)
			self.viewer_list.populate()
		else:
			QMessageBox.about(self, "File Name Error", "No file name selected")

	def fnleft_rotate(self):
		"""
		Rotate the image to the left 90 degrees
		:return:
		"""
		self.viewer.left_rotate()

	def fnright_rotate(self):
		"""
		Rotate the image to the right 90 degrees
		:return:
		"""
		self.viewer.right_rotate()
