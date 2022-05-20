from statistics import mean
import sys
from PyQt6 import QtWidgets, uic
from pseudoSensor import PseudoSensor
from MainWindow import Ui_MainWindow
import datetime
import multitimer

# Globals
# I decided not to use a database so we will store the values in a list with items of the form [humidity, temperature, datetime]

monitor = False
vals = []
timer_count = 0
hmax = 80
tmax = 40
ps = PseudoSensor()



class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.closeProgram.setCheckable(True)
        self.closeProgram.clicked.connect(self.closeProgram_was_clicked)
        self.read1.setCheckable(True)
        self.read1.clicked.connect(self.read1_was_clicked)
        self.Reset.setCheckable(True)
        self.Reset.clicked.connect(self.reset_was_clicked)
        self.read10.setCheckable(True)
        self.read10.clicked.connect(self.read10_was_clicked)
        self.getStats.setCheckable(True)
        self.getStats.clicked.connect(self.getStats_was_clicked)
        self.Set.setCheckable(True)
        self.Set.clicked.connect(self.Set_was_clicked)

    def Set_was_clicked(self):
        global monitor
        global hmax
        global tmax
        monitor = False
        hmax = int(self.humidityLimit.toPlainText())
        tmax = int(self.temperatureLimit.toPlainText())
        self.displayText.clear()
        self.displayText.append('hmax: ' + str(hmax))
        self.displayText.append('tmax: ' + str(tmax))
        

    # Close the program, we must stop the timer so the program actually finishes
    def closeProgram_was_clicked(self):
        timer.stop()  
        self.close()

    # Make everything start from scratch

    def reset_was_clicked(self):
        global vals
        global monitor
        vals = []
        monitor = False
        self.displayText.clear()

    # Read a single value

    def read1_was_clicked(self):
        
        h,t = ps.generate_values()
        vals.append([h, t, datetime.datetime.now()])
        print(vals)
        if(checkht(h,t)):
            return
        self.displayText.clear()
        self.displayText.append("H " + str(h))
        self.displayText.append("T " + str(t))

    # Enable the monitor flag so that we can gather data every second with the timer
    def read10_was_clicked(self):
        global monitor
        monitor = not monitor

# Function to get the Stats

    def getStats_was_clicked(self):
        global monitor
        monitor = False
        self.displayText.clear()
        h = []
        t = []
        v = []
        print(len(vals))

        # if we have no data, continue
        if len(vals) == 0:
            self.displayText.append("No data")
            return

        # Now we have data, so we must check if we have 10 or fewer
        elif len(vals) < 10:
            for i in range(len(vals)):
                h.append(vals[i][0])
                t.append(vals[i][1])
        else:
            v = vals[-10:]
            for i in range(10):
                h.append(v[i][0])
                t.append(v[i][1])
        # Now we can compute the stats

        self.displayText.append("H max: " + str(max(h)))
        self.displayText.append("H min: " + str(min(h)))
        self.displayText.append("H avg: " + str(mean(h)))
        self.displayText.append("T max: " + str(max(t)))
        self.displayText.append("T min: " + str(min(t)))
        self.displayText.append("T avg: " + str(mean(t)))
                

        

app = QtWidgets.QApplication(sys.argv)

window = MainWindow()

# A timer so that we can do a function every second
def timer_1():
        global timer_count
        timer_count = timer_count + 1
        print(timer_count)
        global monitor
        if monitor:
            for i in range(10):
                h,t = ps.generate_values()
                vals.append([h, t, datetime.datetime.now()])
                #if(checkht(h,t)):
                #    break


            window.displayText.append("Appended 10 values")

#CONFIGURING THE TIMER 
timer = multitimer.MultiTimer(interval=1, function=timer_1, args=None, kwargs=None, count=999999, runonstart=True)
timer.start()

def checkht(h, t):
        global monitor
        global hmax
        global tmax
        if (h < hmax) and (t < tmax):
            return False
        monitor = False
        window.displayText.clear()
        window.displayText.append("Reading out of Range")
        window.displayText.append("H: " + str(h))
        window.displayText.append("T: " + str(t))
        window.displayText.append("Hmax: " + str(hmax))
        window.displayText.append("Tmax: " + str(tmax))
        return True

window.show()
app.exec()



