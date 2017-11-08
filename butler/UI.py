import sys, os
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
MY_NAME = 'UI_weak_until'
broker = 'iot.eclipse.org'
topicname = "cis650prs"

# Get your IP address
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
ip_addr = str(s.getsockname()[0])
print('IP address: {}'.format(ip_addr))
s.close()

'''
def on_connect(client, userdata, flags, rc):
    print('connected')

def on_message(client, userdata, msg):
    # msg.payload is bytes, msg.topic is string. That's stupid.
    print("Received " + ", ".join([msg.topic, msg.payload.decode('utf-8') + "\n"]))
    myString = str(msg.payload).split("====")
    if "====".join(myString[1:]) == l:
        print("Matched {}".format(l))
        lb = True
    elif "====".join(myString[1:]) == r:
        print("Matched {}".format(r)) # TODO: GUI it
        rb = True
    if lb == True and rb == False:
        print("Assert (!{} W {}) failed".format(l, r)) # TODO: GUI it
        failed = True

def on_disconnect(client, userdata, rc):
    print("Disconnected in a normal way")
    #graceful so won't send will

def on_log(client, userdata, level, buf):
    pass
    # print("log: {}".format(buf)) # only semi-useful IMHO

'''

class mainClass(QWidget):
    from PyQt5.QtCore import QObject, pyqtSignal
    #client_message = QtCore.pyqtSignal(object)
    #client_message = pyqtSignal(object)
    client_message = pyqtSignal()

    def __init__(self, mqtt_client, parent = None):
        super().__init__()
        self._mqtt_client = mqtt_client
        self.startUI()         
   
    def test(self):
        print("hello test")


    def update_label(self):
        pass
    
    def startUI(self, parent = None ):
        #super().__init__()
        
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
        weakUntillAssert= QLabel()
        weakTimeStamp = QLabel()
        weakStatus = QLabel()
    
        lineBreak=QLabel()   
     
        title2 = QLabel()
        progressProperty= QLabel()
        progressPropertyTimeStamp = QLabel()
        progressPropertyStatus = QLabel()
        
        title1.setText("Weak untill Assert")
        weakUntillAssert.setText("! lw W rw ")
        weakTimeStamp.setText("Time Stamp: No updated yet")
        weakStatus.setText("Status: ok/failed")
  
        lineBreak.setText("---------------------------------------------------------------------------")       
 
        title2.setText("Progress property")
        progressProperty.setText("lp -->  rp ")
        progressPropertyTimeStamp.setText("Time Stamp: No updated yet")
        progressPropertyStatus.setText("Status: ok/failed")
	
        title1.setAlignment(Qt.AlignCenter)
        weakUntillAssert.setAlignment(Qt.AlignLeft)
        weakTimeStamp.setAlignment(Qt.AlignLeft)
        weakStatus.setAlignment(Qt.AlignLeft)
       
        lineBreak.setAlignment(Qt.AlignCenter)
 
        title2.setAlignment(Qt.AlignCenter)
        progressProperty.setAlignment(Qt.AlignLeft)
        progressPropertyTimeStamp.setAlignment(Qt.AlignLeft)
        progressPropertyStatus.setAlignment(Qt.AlignLeft)

        layout.addWidget(title1)
        layout.addWidget(weakUntillAssert)
        layout.addWidget(weakTimeStamp)
        layout.addWidget(weakStatus)

        layout.addWidget(lineBreak)
           
        layout.addWidget(title2)
        layout.addWidget(progressProperty)
        layout.addWidget(progressPropertyTimeStamp)
        layout.addWidget(progressPropertyStatus)
        #Add layout and widgets to window , set window size, name window
        self.setLayout(layout)
        
        self.setMinimumSize(600, 800)
        self.setWindowTitle("Model Checker")
      

        #Borrowed  
        self._mqtt_client.on_connect = self.on_connect
        print("Pass connected")
        self._mqtt_client.on_message = self.client_message.emit()
        #self._mqtt_client.on_message = lambda c, d, msg: self.client_message.emit(msg)
        print("got on msg")
        self.client_message.connect(self.on_client_message)   
        print("end main loop") 

    def on_client_message(self,message):
        print("on client msg called")
        print(message)
        title1.setText(message.payload)
        weakUntillAssert.setText(message.payload)
        weakTimeStamp.setText(message.payload)
        weakStatus.setText(message.payload)
        print("Leaving client msg")
        return
 
    def updatePoints(self):
        pass 
   
    def on_connect(self, client, userdata, flags, rc):
        client.subscribe("#")
        print("Connected")

    def on_disconnect(self,client, userdata, rc):
        print("Disconnected in a normal way")
        #graceful so won't send will

    def on_log(self,client, userdata, level, buf):
        pass

def main():
            # Instantiate the MQTT client
    mqtt_client = paho.Client()
    mqtt_topic = topicname + '/' + socket.gethostname()   
    mqtt_client.will_set(mqtt_topic, '______________Will of '+MY_NAME+' _________________\n\n', 0, False)
    mqtt_client.connect(broker, 1883)
    #mqtt_client.subscribe("#")
    mqtt_client.subscribe(topicname + "/#")
    app = QApplication(sys.argv)
    mainWindow = mainClass(app,mqtt_client)
    mainWindow.show()
    
    mqtt_client.loop_start() 
    try:
        sys.exit(app.exec_())
    finally:
        mqtt_client.loop_stop()

	
if __name__ == '__main__':
    main()
