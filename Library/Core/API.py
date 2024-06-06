# Coded by Eric Chen / D1172271
# ISTM Purdue
#
# Date: 2023/11/25
# CopyRight: GNU GPLv3
# DESC: RollColling FLASK Server

import os
import logging
import requests
import threading
from flask import Flask, request, render_template, redirect, url_for
from werkzeug.utils import secure_filename

from ..FacialRecognition import FacialRecognition


class WebpageAPI:
    LOGGER = None
    __HALT_SIGNAL = None
    UPLOAD_FOLDER = None
    UPDATE_SIGNAL = None
    TARGET_FOLDER = None
    FACIAL_RECOGNITION = None
    API = Flask(__name__, template_folder=os.path.join(os.path.dirname(__name__), '..', 'Site/Template'), static_folder=os.path.join(os.path.dirname(__name__), '..', 'Site/Static'))

    def __init__(self, interface, port, upload_folder, update_signal, target_folder):
        # initialize some important instance attribute
        self.thread = threading.Thread(target=self.__start_server)
        self.thread.daemon = True # incase the program was fucked up, like immdeiate crash
        self.interface = interface
        self.port = port
        self.ssl = False # future improvement

        # create the folder for saving the attendence data
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)

        # initialize some important class attribute
        WebpageAPI.LOGGER = logging.getLogger(__name__)
        WebpageAPI.__HALT_SIGNAL = threading.Event() # elegent shutdown solution
        WebpageAPI.UPLOAD_FOLDER = upload_folder
        WebpageAPI.UPDATE_SIGNAL = update_signal
        WebpageAPI.TARGET_FOLDER = target_folder

        WebpageAPI.FACIAL_RECOGNITION = FacialRecognition.FacialRecognitionClass(WebpageAPI.TARGET_FOLDER)


    # start the server in a seperate thread to solve the halting GUI problem
    def __start_server(self):
        self.API.run(host=self.interface, port=self.port, debug=True, use_reloader=False, ssl_context=("Cert/server.crt", "Cert/server.key")) # dont touch !!!
        return


    # start the flask server
    def start(self):
        self.thread.start()
        return


    # stop the flask server
    def stop(self):
        WebpageAPI.__HALT_SIGNAL.set()
        requests.get("http://127.0.0.1:" + str(self.port) + '/Server_Immediate_Halt')
        return


    # the default website landing page
    @staticmethod
    @API.get('/')
    def default_landing():
        return render_template('index.html')


    # submission success page
    @staticmethod
    @API.get('/Success')
    def success():
        nid = request.args.get('NID', 'Unknown')
        WebpageAPI.LOGGER.info("Rendering the success landing page for user: {}".format(nid))
        return render_template('success.html', NID=nid)


    # receiving the user submission data
    @staticmethod
    @API.route('/Submit-RollCall', methods=['POST', 'GET'])
    def handle_rollcall():
        if request.method == 'GET': # incase some bastard are fuzzing the path via GET
            return redirect(url_for('default_landing'))

        elif request.method == 'POST':
            NID = request.form.get('NID') # access text data
            snapshot = request.files.get('SnapShot')

            # if either one is submitted with empty data
            if not (NID or snapshot):
                return "RollCall Submission invalid", 400

            # parse the data, save image
            filename = secure_filename(snapshot.filename)
            filename = os.path.join(os.path.dirname(__name__), WebpageAPI.UPLOAD_FOLDER, filename)
            snapshot.save(filename)

            print(WebpageAPI.FACIAL_RECOGNITION.recognizeFace(filename, NID))

            # emit the signal for rerendering the panel
            WebpageAPI.LOGGER.info("Emitting qt signal")
            WebpageAPI.UPDATE_SIGNAL.emit(NID, filename)
            WebpageAPI.LOGGER.info(f"Saving rollcalling entry of NID \'{NID}\' to: \'{filename}\'")
            return "RollCall Submission success", 200


    # the hidden shutdown command triggering path
    @staticmethod
    @API.get('/Server_Immediate_Halt')
    def halt():
        WebpageAPI.LOGGER.warning("Receive an immediate halting signal from controller !")
        if WebpageAPI.__HALT_SIGNAL.is_set():
            WebpageAPI.LOGGER.warning("Shutting down the werkzeug Server !!")
            func = request.environ.get('werkzeug.server.shutdown')

            if func is not None:
                func()
            
            else:
                WebpageAPI.LOGGER.critical("You are not in debug mode !! Force shutting daemon !!")

        return "Server shutting down", 200



if __name__ == "__main__":
    instance = WebpageAPI("0.0.0.0", 8888)
    instance.start_server()
