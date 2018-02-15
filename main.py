import sys
from Model import MyModel
from MainWindow import MainWindow
from PyQt5.QtWidgets import QApplication


qdark_present = True
try:
	import qdarkstyle  
except ImportError:
	qdark_present = False


if __name__ == '__main__':

	# The model
	model = MyModel()

	app = QApplication(sys.argv)

	if qdark_present:
		app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
	
	window = MainWindow(model)  # The view controller / view (GUI)

	sys.exit(app.exec_())