#Notes
#TODO Adding three asserts to UI
# Adding three weak untills`
# !leader0 untill election0
# ts ==== DEST (id) ==== leader ==== 0
# So if 0 is the cheater, then 1 would catch it right away
#

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

    #Global car messages to update
    car0 = "????"
    car1 = "????"
    car2 = "????"
    car3 = "????"

    # Start out true, only can turn to False once
    #No weak untills yet
 
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
        self.lineSpace0 = QLabel()
        self.lineBreak0=QLabel()
        self.lineBreak1=QLabel()
        self.lineBreak2=QLabel()
        self.lineBreak3=QLabel()
        self.lineBreak4=QLabel()
        
        self.lineBreak0.setText("---------------------------------------------------------------------------")       
        self.lineBreak1.setText("---------------------------------------------------------------------------")       
        self.lineBreak2.setText("---------------------------------------------------------------------------")       
        self.lineBreak3.setText("---------------------------------------------------------------------------")       
        self.lineBreak4.setText("---------------------------------------------------------------------------")       

        #Add different labels 
        self.title = QLabel()
        
        
        self.car0= QLabel()
        self.car1= QLabel()
        self.car2= QLabel()
        self.car3= QLabel()
        
        self.title.setText("  Car     Start      Instruction       End") 
        self.car0.setText( "   0       Q0          Wait at L0       NA ")
        self.car1.setText( "   1        Q1          Wait at L1        NA ")
        self.car2.setText( "   2       Q2          Wait at L2       NA ")
        self.car3.setText( "   3       Q3          Wait at L3       NA ")
        
     
	
        self.title.setAlignment(Qt.AlignLeft)
        self.car0.setAlignment(Qt.AlignLeft)
        self.car1.setAlignment(Qt.AlignLeft)
        self.car2.setAlignment(Qt.AlignLeft)
        self.car3.setAlignment(Qt.AlignLeft)


        #Add to layout
        layout.addWidget(self.title)
        #layout.addWidget(self.lineBreak1)
        layout.addWidget(self.car0)
        layout.addWidget(self.car1)
        layout.addWidget(self.car2)
        layout.addWidget(self.car3)

        self.setLayout(layout) 
        self.setMinimumSize(600, 800)
        self.setWindowTitle("Leader Model Checker")
        # we need the signal so the event is processed on the GUI thread
        # source: https://github.com/Sensirion/libsensors-python/blob/master/streaming_plot_client.py
        self._mqtt_client.on_message = lambda client, userdata, msg: self.client_handler.emit(msg)
        self.client_handler.connect(self.on_client_message)

    # Handlers for each message
    

    def on_client_message(self, msg):
        print("Received" + ", ".join([msg.topic, msg.payload.decode('utf-8') + "\n"]))
        myString = str(msg.payload.decode('utf-8')).split("$$$$")
        #Check WeakUntill
        #Check 1
        if len(myString) == 4 and myString[1] == "0" and myString[2] == "forward" :
            self.update_label_something(myString[3], myString[0])
        elif len(myString) == 4 and myString[1] == "0" and myString[2] == "right":
            self.update_label_something(myString[3], myString[0])
        elif len(myString) == 4 and myString[1] == "0" and myString[2] == "enter":
            self.update_label_something(myString[3], myString[0])
        elif len(myString) == 4 and myString[1] == "0" and myString[2] == "exit":
            self.update_label_something(myString[3], myString[0])

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