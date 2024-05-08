# Coded by Eric Chen / D1172271
# ISTM Purdue
#
# Time Elapsed: 15Hr
# Date: 2023/11/25
# CopyRight: GNU GPLv3
# DESC: RollColling FLASK Server

import logging
from PyQt6.QtWidgets import QApplication, QMainWindow
from Library.GUI import Panel


# DESC: The all in one class that handles everything
class MainWindow(QMainWindow):
	def __init__(self):
		super().__init__()
		self.rollcalling_panel = Panel.RollCalling('0.0.0.0', 8888)
		self.setCentralWidget(self.rollcalling_panel)
		self.setFixedSize(770, 460)


# DESC: The entrypoint
def main():
	# configuring logger for all modules
	logging.basicConfig(level=logging.INFO,
						format='[%(levelname)s] - Logger:%(name)s - %(message)s(%(name)s:%(lineno)d)')

	# start application
	app = QApplication([])
	window = MainWindow()
	window.show()
	app.exec()
	return



if __name__ == "__main__":
	main()