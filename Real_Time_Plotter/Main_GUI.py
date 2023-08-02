from PyQt5.QtWidgets import (QApplication,QMessageBox,QMainWindow,QVBoxLayout,QAction,QFileDialog)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import serial as sr 
import numpy as np
import pyqtgraph as pg
import pandas as pd




from PyQt5 import QtCore, QtGui, QtWidgets



class Ui_RealTimePlotter(QMainWindow,object):

    

    def setupUi(self, RealTimePlotter):
        RealTimePlotter.setObjectName("RealTimePlotter")
        RealTimePlotter.resize(831, 679)
        self.centralwidget = QtWidgets.QWidget(RealTimePlotter)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")


#global variables

        

        self.data =[]
        self.filename= ['']
        self.dataCsv = []
        self.means=[]
        self.meansCsv = []
        self.Rs = []
        self.RsCsv = []
        self.count = 0
        self.count1 = 0
        self.xChartCL = 0.0
        self.xChartUCL = 0.0
        self.xChartLCL = 0.0
        self.stDevs = []
        self.stDevsCsv = []
        self.rChartCL = 0.0
        self.rChartUCL = 0.0
        self.rChartLCL = 0.0

        self.cond = False
        self.filePlotFlag = False
        self.arduinoPlotFlag = False
        


#set grapgh and timer

        self.timer = QtCore.QTimer()
        self.timer2 = QtCore.QTimer()
        self.timer.setInterval(1000)
        self.timer2.setInterval(200)
        self.timer.timeout.connect(self.plotOnGraph)
        self.timer2.timeout.connect(self.getData)
        self.timer.start()
        self.timer2.start()
        
        self.graph = pg.PlotWidget()
        self.graph2 = pg.PlotWidget()
        self.pen = pg.mkPen(color ="blue")
        self.pen2 = pg.mkPen(color ="red")
        self.pen3 = pg.mkPen(color ="green")
        self.graph.plotItem.setLabel('bottom','Sample')
        self.graph.plotItem.setLabel('left','Sample Mean')
        self.graph2.plotItem.setLabel('bottom','Sample')
        self.graph2.plotItem.setLabel('left','Standard Deviation')
        self.graph.plotItem.setTitle('X_chart')
        self.graph2.plotItem.setTitle('R_chart')

        self.graph.show()
        self.graph2.show()

 #add graph
        self.graph.setStyleSheet("background-color: rgb(0, 0, 0);")
        self.graph.setObjectName("grapgh")
        self.verticalLayout.addWidget(self.graph)


        self.graph2.setStyleSheet("background-color: rgb(0, 0, 0);")
        self.graph2.setObjectName("grapgh2")
        self.verticalLayout.addWidget(self.graph2)

        

       

        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.startButton = QtWidgets.QPushButton(self.centralwidget, clicked=lambda:self.plot_start())
        self.startButton.setStyleSheet("font: 75 10pt \"Times New Roman\";\n"
"background-color: rgb(0, 0, 0);\n"
"\n"
"color: rgb(64, 255, 70);")
        self.startButton.setObjectName("startButton")
        self.horizontalLayout.addWidget(self.startButton)

        
        self.clearButton = QtWidgets.QPushButton(self.centralwidget, clicked=lambda:self.clear())
        self.clearButton.setStyleSheet("font: 75 10pt \"Times New Roman\";\n"
"background-color: rgb(0, 0, 0);\n"
"color: rgb(255, 77, 33);")
        self.clearButton.setObjectName("clearButton")
        

        self.stopButton = QtWidgets.QPushButton(self.centralwidget, clicked=lambda:self.plot_stop())
        self.stopButton.setStyleSheet("font: 75 10pt \"Times New Roman\";\n"
"background-color: rgb(0, 0, 0);\n"
"color: rgb(255, 77, 33);")
        self.stopButton.setObjectName("stopButton")
        self.horizontalLayout.addWidget(self.stopButton)

        self.verticalLayout.addLayout(self.horizontalLayout)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)
        RealTimePlotter.setCentralWidget(self.centralwidget)


        

#////////////

        self.toolBar = QtWidgets.QToolBar(RealTimePlotter)
        self.toolBar.setObjectName("toolBar")
        RealTimePlotter.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        
        self.actionAdd_file = QtWidgets.QAction(RealTimePlotter)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icons/image.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionAdd_file.setIcon(icon)
        self.actionAdd_file.setObjectName("actionAdd_file")
        
        self.actionPlot_from_file = QtWidgets.QAction(RealTimePlotter)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("icons/plot1.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionPlot_from_file.setIcon(icon1)
        self.actionPlot_from_file.setObjectName("actionPlot_from_file")
        
        self.actionPlot_from_arduino = QtWidgets.QAction(RealTimePlotter)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("icons/plot2.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionPlot_from_arduino.setIcon(icon2)
        self.actionPlot_from_arduino.setObjectName("actionPlot_from_arduino")
        
        self.toolBar.addAction(self.actionAdd_file)
        self.toolBar.addAction(self.actionPlot_from_file)
        self.toolBar.addAction(self.actionPlot_from_arduino)

        self.actionAdd_file.triggered.connect(self.browseFolder)
        self.actionPlot_from_file.triggered.connect(self.filePlot)
        self.actionPlot_from_arduino.triggered.connect(self.arduinoPlot)

        



        self.retranslateUi(RealTimePlotter)
        QtCore.QMetaObject.connectSlotsByName(RealTimePlotter)


     

    def retranslateUi(self, RealTimePlotter):
        _translate = QtCore.QCoreApplication.translate
        RealTimePlotter.setWindowTitle(_translate("RealTimePlotter", "Real Time Plotter"))
        self.startButton.setText(_translate("RealTimePlotter", "Start"))
        self.clearButton.setText(_translate("RealTimePlotter", "Clear"))
        self.stopButton.setText(_translate("RealTimePlotter", "Stop"))
        
        


    def browseFolder(self):
        
        self.filename = QFileDialog.getOpenFileName(self,"Open","","Csv Files (*.csv);;All Files (*)")
        # print(self.filename)

    def filePlot(self):
        self.filePlotFlag = True
        self.arduinoPlotFlag = False
        self.count = 0
        self.horizontalLayout.addWidget(self.clearButton)

    def arduinoPlot(self):
        self.arduinoPlotFlag = True
        self.filePlotFlag = False
        self.count = 0
        self.horizontalLayout.removeWidget(self.clearButton)


    def clear(self):
        self.dataCsv = []
        self.meansCsv = []
        self.RsCsv = []
        self.stDevsCsv = []
        self.count = 0
        self.count1 = 0



    

    def play_sound(self):
        # sound = pygame.mixer.Sound("Alarm Sound.mp3")
        # pygame.mixer.Sound.play(sound)
        print(f'alarm{self.count1}')

        
    
    

    def getData(self):

        if arduinoDataFlag and self.arduinoPlotFlag:

            self.a = arduinoData.readline()
            self.a.decode()

            self.data =np.append(self.data,float(self.a))
            # print(self.data)
            if len(self.data) > 5 and self.count+5 < len(self.data):
                
                mean = np.sum(self.data[self.count:self.count+5])/5
                R = max(self.data[self.count:self.count+5]) - min(self.data[self.count:self.count+5])
                self.means.append(mean)
                self.Rs.append(R)

                stDev = np.sqrt(np.sum((self.data[self.count:self.count+5]- mean)**2 )/5)
                self.stDevs.append(stDev)

                # print(mean)
                self.count+=5

                self.xChartCL = np.sum(self.means)/len(self.means)
                self.xChartUCL = self.xChartCL + 0.58 * (np.sum(self.Rs)/len(self.Rs))
                self.xChartLCL =  self.xChartCL - 0.58 * (np.sum(self.Rs)/len(self.Rs))

                self.rChartCL = np.sum(self.Rs)/len(self.Rs)
                self.rChartUCL = 2.11 * self.rChartCL
                self.rChartLCL = 0 * self.rChartCL


            # print(self.means)


        elif self.filePlotFlag and self.filename[0] != '':

            df = pd.read_csv(self.filename[0])
            df = df.dropna(axis=0, how='any')
            self.dataCsv = df[df.head(0).columns[1]]
            # print(self.dataCsv)
            if len(self.dataCsv) > 5 and self.count+5 < (len(self.dataCsv) ):

                mean = np.sum(self.dataCsv[self.count:self.count+5])/5
                R = max(self.dataCsv[self.count:self.count+5]) - min(self.dataCsv[self.count:self.count+5])
                self.meansCsv.append(mean)
                self.RsCsv.append(R)


                stDev = np.sqrt(np.sum((self.dataCsv[self.count:self.count+5]- mean)**2 )/5)
                self.stDevsCsv.append(stDev)
                # print(stDev)
                

                

                self.count+=5


                self.xChartCL = np.sum(self.meansCsv)/len(self.meansCsv)
                self.xChartUCL = self.xChartCL + 0.58 * (np.sum(self.RsCsv)/len(self.RsCsv))
                self.xChartLCL =  self.xChartCL - 0.58 * (np.sum(self.RsCsv)/len(self.RsCsv))

                self.rChartCL = np.sum(self.RsCsv)/len(self.RsCsv)
                self.rChartUCL = 2.11 * self.rChartCL
                self.rChartLCL = 0 * self.rChartCL





            # print('cl',self.xChartCL)
            # print('ucl',self.xChartUCL)
            # print('lcl',self.xChartLCL)


        else:
            pass

            






    def plotOnGraph(self):
        
        if self.cond and arduinoDataFlag and self.arduinoPlotFlag:
           
            self.graph.plotItem.clear()
            self.t = range(0,len(self.means),1)
            self.graph.plotItem.plot(self.t,self.means,pen=self.pen)
            self.graph.plotItem.addLine(y=self.xChartCL,pen=self.pen3)
            self.graph.plotItem.addLine(y=self.xChartUCL,pen=self.pen2)
            self.graph.plotItem.addLine(y=self.xChartLCL,pen=self.pen2)

            self.graph2.plotItem.clear()
            self.tR = range(0,len(self.stDevs),1)
            self.graph2.plotItem.plot(self.tR,self.stDevs,pen=self.pen)
            self.graph2.plotItem.addLine(y=self.rChartCL,pen=self.pen3)
            self.graph2.plotItem.addLine(y=self.rChartUCL,pen=self.pen2)
            self.graph2.plotItem.addLine(y=self.rChartLCL,pen=self.pen2)


            if (self.means[self.count1] > self.xChartUCL or self.means[self.count1] < self.xChartLCL):
                self.play_sound()
            
            elif (self.stDevs[self.count1] > self.rChartUCL or self.stDevs[self.count1] < self.rChartLCL):
                self.play_sound()

            self.count1+=1
            
        
        elif self.cond and self.filePlotFlag and self.filename[0] != '':
            
            self.graph.plotItem.clear()
            self.t = range(0,len(self.meansCsv),1)
            self.graph.plotItem.plot(self.t,self.meansCsv,pen=self.pen)
            self.graph.plotItem.addLine(y=self.xChartCL,pen=self.pen3)
            self.graph.plotItem.addLine(y=self.xChartUCL,pen=self.pen2)
            self.graph.plotItem.addLine(y=self.xChartLCL,pen=self.pen2)


            self.graph2.plotItem.clear()
            self.tR = range(0,len(self.stDevsCsv),1)
            self.graph2.plotItem.plot(self.tR,self.stDevsCsv,pen=self.pen)
            self.graph2.plotItem.addLine(y=self.rChartCL,pen=self.pen3)
            self.graph2.plotItem.addLine(y=self.rChartUCL,pen=self.pen2)
            self.graph2.plotItem.addLine(y=self.rChartLCL,pen=self.pen2)



            if (self.meansCsv[self.count1] > self.xChartUCL or self.meansCsv[self.count1] < self.xChartLCL):
                self.play_sound()
            
            elif (self.stDevsCsv[self.count1] > self.rChartUCL or self.stDevsCsv[self.count1] < self.rChartLCL):
                self.play_sound()


            self.count1+=1




            # print(len(self.meansCsv))

        else:
            pass

            

    def plot_start(self):
        self.cond = True
        self.timer.start()

        
        if arduinoDataFlag :
            arduinoData.reset_input_buffer()
            

        
        

    def plot_stop(self):
        self.cond = False
        self.timer.stop()
        

    
        

    



if __name__ == "__main__":
    import sys
    try:
     arduinoData = sr.Serial("COM3",9600)
     arduinoDataFlag = True
    
    except:
        arduinoDataFlag = False

    app = QtWidgets.QApplication(sys.argv)
    RealTimePlotter = QtWidgets.QMainWindow()
    ui = Ui_RealTimePlotter()
    ui.setupUi(RealTimePlotter)
    RealTimePlotter.show()
    
   

    

    sys.exit(app.exec_())
