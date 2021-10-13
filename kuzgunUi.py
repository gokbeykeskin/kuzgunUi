from PyQt5 import QtWidgets, QtCore,QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QPixmap, QTransform
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sys
from dronekit import connect, VehicleMode, LocationGlobalRelative
import time

gorsellerDosyasi = 'gorseller/'

def baglantiyiKes():
	vehicle.close()
	durumBilgisi.setText("Durum: Bağlı Değil")
	durumBilgisi.adjustSize()
	vehicle.remove_attribute_listener('attitude', veriGuncelle)

def armEt():
	vehicle.armed = not vehicle.armed

def veriGuncelle(self, attr_name, value): #dronekit kütüphanesinin attribute listener özelliğini kullanarak uçaktan anlık veri çeker.
	ucusModu.setText("Uçuş modu: " + vehicle.mode.name)
	ucusModu.adjustSize()

	if(vehicle.armed):
		durum = "Arm oldu"
	else:
		durum = "Arm Değil"
	durumBilgisi.setText("Durum: " + durum)
	durumBilgisi.adjustSize()

	donmusDikeyCursorPixmap = dikeyHizCPixmap.transformed(QTransform().rotate(-vehicle.velocity[2]*18),QtCore.Qt.SmoothTransformation)
	#print("dikey hız:" + str(-vehicle.velocity[2]*18)) 
	dikeyHizCursor.setPixmap(donmusDikeyCursorPixmap)
	
	donmusYatisCursor = yatisCPixmap.transformed(QTransform().rotate(vehicle.attitude.roll*57.2957795),QtCore.Qt.SmoothTransformation)
	#print("roll:" + str(vehicle.attitude.roll*57.2957795))
	yatisCursor.setPixmap(donmusYatisCursor)

	donmusPusulaCursor = pusulaCPixmap.transformed(QTransform().rotate(vehicle.heading),QtCore.Qt.SmoothTransformation)
	#print("yön: " + str(vehicle.heading))
	pusulaCursor.setPixmap(donmusPusulaCursor)

	donmusYerHiziCursor = yerHiziCPixmap.transformed(QTransform().rotate(vehicle.groundspeed*6),QtCore.Qt.SmoothTransformation)
	#print("hız: " + str(vehicle.groundspeed))
	yerHiziCursor.setPixmap(donmusYerHiziCursor)


	donmusAttitudePixmap = attitudeCPixmap.transformed(QTransform().rotate(vehicle.attitude.roll*57.2957795),QtCore.Qt.SmoothTransformation)
	attitudeCursor.setPixmap(donmusAttitudePixmap)

	attitudeLabel.setGeometry(300,int(vehicle.attitude.pitch*550-250),900,900)
	donmusYukseklikCursorPixmap = yukseklikCPixmap.transformed(QTransform().rotate(float(vehicle.location.global_relative_frame.alt)*3.6),QtCore.Qt.SmoothTransformation)
	#print("pitch: "  + str(vehicle.location.global_relative_frame.alt))
	yukseklikCursor.setPixmap(donmusYukseklikCursorPixmap)
	#print("speed:"+str(vehicle.groundspeed)+"\naltitude:" + str(vehicle.location.global_relative_frame.alt))
	win.show()


	if(vehicle.armed):
		yaziGuncelle("Disarm Et")
	else:
		yaziGuncelle("Arm Et") 

def yaziGuncelle(yazi):
	armDugmesi.setText(yazi)



print("#Kuzgun'a bağlanılıyor.<<<")

#for USB or telemetry connection(port name might change depending on OS, this is for Linux based OS):
'''
For simulation 127.0.0.1:14550
1 - cd ArduPilot/ArduPlane
2 - ../Tools/autotest/sim_vehicle.py --map --console
Then run
'''
vehicle = connect('127.0.0.1:14550',baud = 57600, wait_ready=False)     #2. parametre olarak baud = 57600 gelecek,1. parametre telemetri com portu olacak
#vehicle.wait_ready('autopilot_version')

app = QApplication(sys.argv)
win = QMainWindow() #ana ekran
win.setGeometry(500,0,900,900)
win.setWindowTitle("KUZGUN UÇUŞ ARAYÜZÜ")

attitudePixmap = QtGui.QPixmap(gorsellerDosyasi+"attitudeArkaplan.png") #attitude cayrosu fotoğrafı

attitudeLabel = QtWidgets.QLabel(win) #durum cayrosu etiketi
attitudeLabel.setPixmap(attitudePixmap)
attitudeLabel.setAlignment(QtCore.Qt.AlignCenter)
attitudeLabel.setGeometry(300,50,1800,1800)

anaArkaplanPixmap = QtGui.QPixmap(gorsellerDosyasi+"anaArkaplan.png") #ana arkaplan fotoğrafı
anaArkaplanLabel = QtWidgets.QLabel(win) #ana arkaplan etiketi
anaArkaplanLabel.setAlignment(QtCore.Qt.AlignCenter)
anaArkaplanLabel.setGeometry(0,0,900,900)
anaArkaplanLabel.setPixmap(anaArkaplanPixmap)


dikeyHizPixmap = QtGui.QPixmap(gorsellerDosyasi+"dikeyHizArkaplan.png") #dikey hız fotoğrafı
dikeyHizLabel = QtWidgets.QLabel(win)
dikeyHizLabel.setPixmap(dikeyHizPixmap)
dikeyHizLabel.setGeometry(0,50,300,300)


dikeyHizCPixmap = QtGui.QPixmap(gorsellerDosyasi+"cursor.png") #dikey hız imleci fotoğrafı
dikeyHizCPixmap = dikeyHizCPixmap.transformed(QTransform().rotate(270),QtCore.Qt.SmoothTransformation) #sıfır noktasından başlaması için dik imleci 270 derece döndür

dikeyHizCursor = QtWidgets.QLabel(win) #dikey hız imleci etiketi
dikeyHizCursor.setAlignment(QtCore.Qt.AlignCenter)
dikeyHizCursor.setGeometry(0,50,300,300)

yatisCPixmap = QtGui.QPixmap(gorsellerDosyasi+"ucakCursor.png") #yatış göstergesinde kullanılıyor

yatisPixmap = QtGui.QPixmap(gorsellerDosyasi+"yatisArkaplan.png") #yatış göstergesi arkaplanı
yatisLabel = QtWidgets.QLabel(win) #yatış göstergesi etiketi
yatisLabel.setPixmap(yatisPixmap)
yatisLabel.setGeometry(0,350,300,300)

yatisCursor = QtWidgets.QLabel(win)
yatisCursor.setAlignment(QtCore.Qt.AlignCenter)
yatisCursor.setGeometry(0,350,300,300)

pusulaCPixmap = QtGui.QPixmap(gorsellerDosyasi+"pusulaCursor.png") #pusula imleci fotoğrafı

pusulaPixmap = QtGui.QPixmap(gorsellerDosyasi+"pusulaArkaplan.png") #pusula arkaplanı arkaplan fotoğrafı
pusulaLabel = QtWidgets.QLabel(win) #pusula arkaplanı
pusulaLabel.setPixmap(pusulaPixmap)
pusulaLabel.setGeometry(600,50,300,300)
pusulaLabel.setText("")

pusulaCursor = QtWidgets.QLabel(win) #pusula imleci
pusulaCursor.setAlignment(QtCore.Qt.AlignCenter)
pusulaCursor.setGeometry(600,50,300,300)
pusulaCursor.setPixmap(pusulaCPixmap)

yerHiziCPixmap = QtGui.QPixmap(gorsellerDosyasi+"cursor.png") #standart kırmızı imleç fotoğrafı
yerHiziCPixmap = yerHiziCPixmap.transformed(QTransform().rotate(270),QtCore.Qt.SmoothTransformation)

yerHiziPixmap = QtGui.QPixmap(gorsellerDosyasi+"yerHiziArkaplan.png") #yer hızı arkaplan fotoğrafı
yerHiziLabel = QtWidgets.QLabel(win) #yer hızı göstergesi
yerHiziLabel.setPixmap(yerHiziPixmap)
yerHiziLabel.setGeometry(300,350,300,150)
yerHiziLabel.setAlignment(QtCore.Qt.AlignBottom)
yerHiziLabel.setText("")

yerHiziCursor = QtWidgets.QLabel(win) #yer hızı imleci
yerHiziCursor.setAlignment(QtCore.Qt.AlignCenter)
yerHiziCursor.setGeometry(300,360,300,300)


attitudeCPixmap = QtGui.QPixmap(gorsellerDosyasi+"attitudeCursor.png") #durum cayrosu imleci fotoğrafı

attitudeCursor = QtWidgets.QLabel(win) #durum cayrosu imleci
attitudeCursor.setAlignment(QtCore.Qt.AlignCenter)
attitudeCursor.setGeometry(300,50,300,300)
attitudeCursor.setPixmap(attitudeCPixmap)

yukseklikCPixmap = QtGui.QPixmap(gorsellerDosyasi+"cursor.png") #yükseklik göstergesi imleci fotoğrafı

yukseklikPixmap = QtGui.QPixmap(gorsellerDosyasi+"yukseklikArkaplan.png") #yükseklik göstergesi arkaplan fotoğrafı
yukseklikLabel = QtWidgets.QLabel(win)
yukseklikLabel.setPixmap(yukseklikPixmap) #yükseklik göstergesi arkaplanı
yukseklikLabel.setGeometry(600,350,300,300)

yukseklikCursor = QtWidgets.QLabel(win) #yükseklik göstergesi imleci
yukseklikCursor.setAlignment(QtCore.Qt.AlignCenter)
yukseklikCursor.setGeometry(600,350,300,300)


ucusModu = QtWidgets.QLabel(win) #uçuş modu göstergesi
ucusModu.move(10,10)
ucusModu.setStyleSheet("QLabel{background-color: yellow;}") #uçuş modu göstergesi arkaplanı

durumBilgisi = QtWidgets.QLabel(win)  #durum bilgisi göstergesi
durumBilgisi.move(10,25)
durumBilgisi.setStyleSheet("QLabel{background-color: yellow;}") #durum bilgisi göstergesi


baglantiyiKesDugmesi = QtWidgets.QPushButton(win) #bağlantıyı kes butonu
baglantiyiKesDugmesi.setText("Bağlantıyı Kes")
baglantiyiKesDugmesi.clicked.connect(baglantiyiKes)
baglantiyiKesDugmesi.move(470,10)

armDugmesi = QtWidgets.QPushButton(win)
armDugmesi.setText("Arm Et")
armDugmesi.clicked.connect(armEt)
armDugmesi.move(320,10)

logoPixmap = QtGui.QPixmap(gorsellerDosyasi+"logo.png") #kuzgun logosu fotoğrafı

logoLabel = QtWidgets.QLabel(win) #kuzgun logosu
logoLabel.setPixmap(logoPixmap)
logoLabel.setGeometry(300,550,300,300)

vehicle.add_attribute_listener('attitude', veriGuncelle) #uçaktan anlık veri alarak veriGuncelle fonksiyonunda kullan

status = app.exec_()
sys.exit(status)
