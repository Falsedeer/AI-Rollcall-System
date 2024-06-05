# Coded by Eric Chen / D1172271
# ISTM Purdue
#
# Date: 2023/11/25
# CopyRight: GNU GPLv3
# DESC: RollColling FLASK Server

import os
import sys
import qrcode
import logging
import datetime
import pandas as pd
from PIL import ImageQt
from PyQt6.uic import loadUi
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QBrush, QPixmap, QImage
from PyQt6.QtWidgets import QWidget, QMessageBox, QSpacerItem, QSizePolicy, QListWidgetItem, QGraphicsScene
from ..Utils import Networking
from ..Core import API


# DESC: The main widget of the Server control panel
class RollCalling(QWidget):
    UPDATE_SIGNAL = pyqtSignal(str, str)

    def __init__(self, interface, port):
        super().__init__()
        loadUi("Library/Design/Panel.ui", self)

        # assigning some critical attributes
        self.interface = interface
        self.port = port
        self.attendence = []
        self.setFixedSize(775, 465)
        self.logger = logging.getLogger(__name__)
        self.datetime = datetime.date.today()
        self.upload_base_folder = os.path.join("Uploads", self.datetime.strftime('%Y-%m-%d'))
        self.target_image_folder = "Targets"

        # signal connecting
        self.Calender.setEnabled(False)
        self.UPDATE_SIGNAL.connect(self.__update_attendence)
        self.StopServer_Button.clicked.connect(self.stop_server)
        self.StartServer_Button.clicked.connect(self.start_server)
        self.ExportJson_Button.clicked.connect(self.export_json)
        self.ExportExcel_Button.clicked.connect(self.export_excel)
        self.ShowAttendence_Button.clicked.connect(lambda: self.StackedWidget.setCurrentIndex(1))
        self.Back_Button.clicked.connect(lambda: self.StackedWidget.setCurrentIndex(0))

        # configure the custom flask instance with qt signal
        self.server = API.WebpageAPI(self.interface, self.port, self.upload_base_folder, self.UPDATE_SIGNAL, self.target_image_folder)

        # try locating the server path
        local_ip = Networking.get_local_ip()
        self.intranet_url = 'https://' + local_ip + ':' + str(self.port) + '/'
        self.loopback_url = 'https://127.0.0.1' + ':' + str(self.port) + '/'
        
        # show qrcode (since we are debugging, so we use local)
        self.__gen_rollcalling_qrcode(self.intranet_url)

        # debug
        self.logger.info("Identified intranet base path as: {}".format(self.intranet_url))
        self.logger.info("Identified loopback base path as: {}".format(self.loopback_url))


    # update the list of attendence
    def __update_attendence(self, NID, snapshot_path):
        self.attendence.append((NID, snapshot_path))

        # update list
        nid_item = QListWidgetItem(NID)
        path_item = QListWidgetItem(snapshot_path)

        nid_item.setFont(QFont("Cantarell", 13))
        path_item.setFont(QFont("Cantarell", 13))
        nid_item.setForeground(QBrush(Qt.GlobalColor.red))
        path_item.setForeground(QBrush(Qt.GlobalColor.red))

        self.AttendenceNID_List.addItem(nid_item)
        self.AttendenceSnapshot_List.addItem(path_item)
        self.logger.info("Current Attendence List: {}".format(str(self.attendence)))
        return


    # generate the qrcode of server, render right after start server
    def __gen_rollcalling_qrcode(self, url):
        # Generate QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(url)
        qr.make(fit=True)
        img = qr.make_image(fill='black', back_color='white')
        
        # Convert the QR code image to a format suitable for QGraphicsView
        qimage = ImageQt.ImageQt(img)
        qr_pixmap = QPixmap.fromImage(qimage)
        scaled_pixmap = qr_pixmap.scaled(self.QRCode_Display.size(), Qt.AspectRatioMode.KeepAspectRatio)
        scene = QGraphicsScene()
        scene.addPixmap(scaled_pixmap)

        # display
        self.QRCode_Display.setScene(scene)
        self.QRCode_Display.show()
        return


    # start the flask server
    def start_server(self):
        self.logger.info("Starting the flask server......")
        self.server.start()
        return


    # halt / stop the flask server
    def stop_server(self):
        self.logger.info("Stopping the flask server......")
        self.server.stop()
        self.pop_messagebox("[WARNING]", "Fask server shutdown elegently !!", "You are now ready to leave ! :)")
        sys.exit(0)
        return


    # export in excel format (default)
    def export_excel(self):
        # conver data to dataframe
        df = pd.DataFrame(self.attendence, columns=['NID', 'Path'])

        # create export filename & save
        filename = os.path.join('Export', self.datetime.strftime('%Y-%m-%d') + "_rollcall.xlsx")
        df.to_excel(filename, index=False)

        # notify user the saved path
        self.pop_messagebox("[INFO]", "Excel Export Succeed !", f"Saved to: {filename}")
        return


    # export in json format (additional)
    def export_json(self):
        self.logger.info("Exporting the attendence in json format......")

        # notify not implemented yet
        self.pop_messagebox("[WARNING]", "Export Type Not Implement !", "Will be added in future update !! :)")
        return


    # Alert messgae box
    def pop_messagebox(self, banner, title, text):
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle(banner)
        msg_box.setText(title)
        msg_box.setInformativeText(text)
        msg_box.setIcon(QMessageBox.Icon.Information)  # Set an icon
        msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)

        # Adjusting the size using QSpacerItem
        spacer = QSpacerItem(200, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        layout = msg_box.layout()
        layout.addItem(spacer, layout.rowCount(), 0, 1, layout.columnCount())
        msg_box.exec()
        return
