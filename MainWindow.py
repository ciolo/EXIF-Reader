from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtWidgets import (QSlider, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QFileDialog, QMessageBox,
							 QCheckBox, QGroupBox, QDesktopWidget, QLineEdit, QListWidget, QListView)
from PyQt5.QtGui import (QPixmap, QTransform, QIcon)
from PyQt5.QtCore import QFile, QFileInfo, QSize

from MyWidgets import CustomTab, MyImageView, ImageFileList


class MainWindow(QWidget):
	"""
	Main window controller
	Attributes:
		
	"""

	def __init__(self, model):
		super().__init__()

		self.model = model
		self.rotation = 0

		self.initUI()
		self.center_on_screen()

	def initUI(self):
		self.setWindowTitle("Exif Reader")

		self.load = QPushButton()
		self.load.setText("Add Photo")
		self.load.clicked.connect(self.load_image_but)

		self.extract_info = QPushButton()
		self.extract_info.setEnabled(False)
		self.extract_info.setText("Get Info")
		self.extract_info.clicked.connect(self.open_info)

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

		self.viewer = MyImageView()
		self.viewer.resize(800, 600)
		#self.viewer.setMaximumSize(QSize(512, 512))
		self.viewer.set_model(self.model)

		self.viewer_list = ImageFileList("/Users/albertociolini/Desktop/test/", self)
		self.viewer_list.setFlow(QListView.LeftToRight)
		self.viewer_list.setMaximumHeight(100)

		top_h_box = QHBoxLayout()
		top_h_box.addWidget(self.load)
		top_h_box.addWidget(self.extract_info)
		top_h_box.addStretch()
		top_h_box.addWidget(self.left_rotate)
		top_h_box.addWidget(self.right_rotate)

		bottom_h_box = QHBoxLayout()
		bottom_h_box.addWidget(self.viewer_list)

		layout = QVBoxLayout()
		layout.addLayout(top_h_box)
		layout.addWidget(self.viewer)
		layout.addLayout(bottom_h_box)

		self.setLayout(layout)

		self.setAcceptDrops(True)

		self.setMinimumSize(600, 500)
		#self.viewer.updateView()
		self.show()

	def center_on_screen(self):
		qt_rectangle = self.frameGeometry()
		center_point = QDesktopWidget().availableGeometry().center()
		qt_rectangle.moveCenter(center_point)
		self.move(qt_rectangle.topLeft())

	def resizeEvent(self, ev):
		"""Slot for window resize event (Override)"""
		self.viewer.update_view()
		super().resizeEvent(ev)

	def open_info(self):
		general = self.model.get_info_general(self.model.name)
		exif = self.model.get_exif_data(self.model.name)
		self.custom_tab = CustomTab(self, exif, general)
		self.custom_tab.open_dict()

	def load_image_but(self):
		"""
		Open a File dialog when the button is pressed
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
			self.model.update(filename)
			self.viewer.set_model(self.model)
			self.viewer.update_view()
		else:
			QMessageBox.about(self, "File Name Error", "No file name selected")
		self.viewer.update_view()

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

	def dragEnterEvent(self, e):

		if len(e.mimeData().urls()) > 0 and e.mimeData().urls()[0].isLocalFile():
			qi = QFileInfo(e.mimeData().urls()[0].toLocalFile())
			ext = qi.suffix()
			if ext == 'jpg' or ext == 'jpeg' or ext == 'png' or ext == 'JPG' or ext == 'PNG':
				e.accept()
				self.model.name = qi.filePath()
				self.extract_info.setEnabled(True)
				self.left_rotate.setEnabled(True)
				self.right_rotate.setEnabled(True)
			else:
				e.ignore()
		else:
			e.ignore()

	def dropEvent(self, e):
		"""
		Drop files directly onto the widget
		File locations are stored in fname
		:param e:
		:return:
		"""
		if e.mimeData().hasUrls:
			e.setDropAction(Qt.CopyAction)
			e.accept()
			# Workaround for OSx dragging and dropping
			for url in e.mimeData().urls():
				fname = str(url.toLocalFile())

			self.model.update(fname)
			self.viewer.set_model(self.model)
			self.viewer.update_view()
		else:
			e.ignore()
