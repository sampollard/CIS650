import sys, os
from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5 import QtCore, QtGui, QtWidgets, QtGui
from PyQt5.QtCore import *
from PyQt5.QtGui import * #import QIcon, QPixmap
from PyQt5.QtWidgets import *
from PIL import Image
from PIL.ImageQt import ImageQt
import socket
import paho.mqtt.client as paho
import signal
import time
import os
import sys
from datetime import datetime as dt

def control_c_handler(signum, frame):
    sys.exit()
    print('saw control-c')
    mqtt_client.disconnect()
    mqtt_client.loop_stop()  # waits until DISCONNECT message is sent out
    print("Now I am done.")
    sys.exit(0)
signal.signal(signal.SIGINT, control_c_handler)

# Set MQTT stuff
MY_NAME = 'UI model checker'
broker = 'iot.eclipse.org'
topicname = "cis650prs"

# Get your IP address
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
ip_addr = str(s.getsockname()[0])
print('IP address: {}'.format(ip_addr))
s.close()

# Set up mqtt on_* functions that don't change the GUI
def on_disconnect(self, client, userdata, rc):
    print("Disconnected in a normal way")
    #graceful so won't send will
def on_log(self, _userdata, level, buf):
    pass
def on_message(client, userdata, msg):
    print("Received " + ", ".join([msg.topic, msg.payload.decode('utf-8') + "\n"]))

class mainClass(QWidget):
    client_handler = QtCore.pyqtSignal(object)
    wul = "????"
    wur = "????"
    #pl = "????"
    #pr = "????"
    # Start out true, only can turn to False once
    weak_until = True
    progress = True
   
    def __init__(self, mqtt_client):
        super().__init__()
        self._mqtt_client = mqtt_client
        self.initUI()

    def initUI(self): 
        #This is the layout
        layout = QVBoxLayout(self)
        #Add the two layouts for the scroll boxes

        layout.setContentsMargins(10, 0, 10, 600)
        layout.setSpacing(0)
        layout.insertStretch(0,0);
        #Intro message
        self.introductionText = QLabel(" Welcome to our program\n\n")
        self.introductionText.setAlignment(Qt.AlignCenter) 
        #Add text to layout
        layout.addWidget(self.introductionText)

        #Line spce
        lineSpace =  QLabel()
        #Add different labels 
        title1 = QLabel()
        self.weakUntilAssert= QLabel()
        self.weakTimeStamp = QLabel()
        self.weakStatus = QLabel()
    
        lineBreak=QLabel()   
     
        title2 = QLabel()
        self.progressProperty= QLabel()
        self.progressPropertyTimeStamp = QLabel()
        self.progressPropertyStatus = QLabel()
        
        title1.setText("Fluent")
        self.weakUntilAssert.setText("Fluent goes here")
        self.weakTimeStamp.setText("Time Stamp: Not updated yet")
        self.weakStatus.setText("Status: ok/failed")
  
        lineBreak.setText("---------------------------------------------------------------------------")       
 
        title2.setText("Safety property")
        self.progressProperty.setText("Safety Property ")
        self.progressPropertyTimeStamp.setText("Time Stamp: Not updated yet")
        self.progressPropertyStatus.setText("Status: ok/failed")
	
        title1.setAlignment(Qt.AlignCenter)
        self.weakUntilAssert.setAlignment(Qt.AlignLeft)
        self.weakTimeStamp.setAlignment(Qt.AlignLeft)
        self.weakStatus.setAlignment(Qt.AlignLeft)
       
        lineBreak.setAlignment(Qt.AlignCenter)
 
        title2.setAlignment(Qt.AlignCenter)
        self.progressProperty.setAlignment(Qt.AlignLeft)
        self.progressPropertyTimeStamp.setAlignment(Qt.AlignLeft)
        self.progressPropertyStatus.setAlignment(Qt.AlignLeft)

        layout.addWidget(title1)
        layout.addWidget(self.weakUntilAssert)
        layout.addWidget(self.weakTimeStamp)
        layout.addWidget(self.weakStatus)

        layout.addWidget(lineBreak)
           
        layout.addWidget(title2)
        layout.addWidget(self.progressProperty)
        layout.addWidget(self.progressPropertyTimeStamp)
        layout.addWidget(self.progressPropertyStatus)
        #Add layout and widgets to window , set window size, name window
        self.setLayout(layout) 
        self.setMinimumSize(600, 800)
        self.setWindowTitle("Leader Model Checker")
        # we need the signal so the event is processed on the GUI thread
        # source: https://github.com/Sensirion/libsensors-python/blob/master/streaming_plot_client.py
        self._mqtt_client.on_message = lambda client, userdata, msg: self.client_handler.emit(msg)
        self.client_handler.connect(self.on_client_message)

    # Handlers for each message
    def update_label_weak_until_left(self, l, ts):
        print("update_label_weak_until_left called")
        self.wul = l
        self.weakUntilAssert.setText("!({} W {})".format(self.wul, self.wur))
        self.weakTimeStamp.setText("Timestamp: {}".format(ts))
    def update_label_weak_until_right(self, r, ts):
        print("update_label_weak_until_right called")
        self.wur = r
        self.weakUntilAssert.setText("!({} W {})".format(self.wul, self.wur))
        self.weakTimeStamp.setText("Timestamp: {}".format(ts))
    #def update_label_progress_left(self, l, ts):
    #    print("update_label_progress_left called")
    #    self.pl = l
    #    self.progressProperty.setText("{} --> {}".format(self.pl, self.pr))
    #    self.progressPropertyTimeStamp.setText("Timestamp: {}".format(ts))
    
    #def update_label_progress_right(self, r, ts):
    #    print("update_label_progress_right called")
    #    self.pr = r
    #    self.progressProperty.setText("{} --> {}".format(self.pl, self.pr))
    #    self.progressPropertyTimeStamp.setText("Timestamp: {}".format(ts))
    
    #def update_label_weak_until_status(self, status, ts):
    #    print("update_label_weak_until_status called")
    #    if self.weak_until == False:
    #        return
    #    elif status == "Failed":
    #        self.weak_until = False
    #    self.weakStatus.setText("Status: {}".format(status))
    #    self.weakTimeStamp.setText("Timestamp: {}".format(ts))
    
    def update_label_progress_status(self, status, ts):
        print("update_label_progress_status called")
        if self.progress == False:
            return
        if status == "Failed":
            self.progress = False
        self.progressPropertyStatus.setText("Status: {}".format(status))
        self.progressPropertyTimeStamp.setText("Timestamp: {}".format(ts))

    def on_client_message(self, msg):
        print("Received" + ", ".join([msg.topic, msg.payload.decode('utf-8') + "\n"]))
        myString = str(msg.payload.decode('utf-8')).split("$$$$")
        #Check WeakUntill
        if len(myString) == 3 and myString[1] == "lw":
            self.update_label_weak_until_left(myString[2], myString[0])
        elif len(myString) == 3 and myString[1] == "rw":
            self.update_label_weak_until_right(myString[2], myString[0])
        elif len(myString) == 3 and myString[1] == "W":
            self.update_label_weak_until_status(myString[2], myString[0])
        #Check progross
        #elif len(myString) == 3 and myString[1] == "lp":
        #    self.update_label_progress_left(myString[2], myString[0])
        #elif len(myString) == 3 and myString[1] == "rp":
        #    self.update_label_progress_right(myString[2], myString[0])
        #elif len(myString) == 3 and myString[1] == "P":
        #    self.update_label_progress_status(myString[2], myString[0])

def main():
    # Instantiate the MQTT client
    mqtt_client = paho.Client()
    mqtt_topic = topicname + '/' + socket.gethostname()
    mqtt_client.will_set(mqtt_topic, '______________Will of '+MY_NAME+' _________________\n\n', 0, False)
    mqtt_client.connect(broker, 1883, keepalive=600) # UI is only a listener
    mqtt_client.subscribe(topicname + "/#")
    app = QApplication(sys.argv)
    mainWindow = mainClass(mqtt_client)
    mainWindow.show()
    mqtt_client.loop_start()
    # Start the GUI
    try:
        sys.exit(app.exec_())
    finally:
        mqtt_client.loop_stop()	
if __name__ == '__main__':
    main()
