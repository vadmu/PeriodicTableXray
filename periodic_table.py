from elements import ELEMENTS
from lines import emission_lines, absorption_lines
import sys
from PyQt4 import Qt, QtGui, QtCore

for el in ELEMENTS:
    el.emission_ka1 = 1000*emission_lines.get(el.number, [0]*8)[0]
    el.emission_ka2 = 1000*emission_lines.get(el.number, [0]*8)[1]
    el.emission_kb1 = 1000*emission_lines.get(el.number, [0]*8)[2]
    el.emission_la1 = 1000*emission_lines.get(el.number, [0]*8)[3]
    el.emission_la2 = 1000*emission_lines.get(el.number, [0]*8)[4]
    el.emission_lb1 = 1000*emission_lines.get(el.number, [0]*8)[5]
    el.emission_lb2 = 1000*emission_lines.get(el.number, [0]*8)[6]
    el.emission_lg1 = 1000*emission_lines.get(el.number, [0]*8)[7]
    
    el.absorption_k   = absorption_lines.get(el.number, [0]*12)[0]
    el.absorption_l1  = absorption_lines.get(el.number, [0]*12)[1]
    el.absorption_l2  = absorption_lines.get(el.number, [0]*12)[2]
    el.absorption_l3  = absorption_lines.get(el.number, [0]*12)[3]

    
def readStyleSheet(fileName) :
    css = ""
    file = Qt.QFile(fileName)
    if file.open(Qt.QIODevice.ReadOnly):
        css = str(file.readAll())
        file.close()
    return css


class Details(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)            
        layout = QtGui.QHBoxLayout()
        self.label1 = QtGui.QLabel()
        self.label2 = QtGui.QLabel()
        self.label3 = QtGui.QLabel()

        layout.addWidget(self.label1)
        layout.addWidget(self.label2)
        layout.addWidget(self.label3)
        self.setLayout(layout)  
        self.currentElement = 0                    
        
    def update(self, el):
        self.currentElement = el
        el = ELEMENTS[el]
        self.label1.setText("<p>" + 
        "<h3><sup>" + str(el.number) + "</sup>" + str(el.symbol) + "</h3>" +
        str(el.mass) + "<br>" +
        # el.eleconfig + "<br>" +
        str(el.name) + "</p>")

        self.label2.setText(
        "<tr><td> K              </td><td align='right'>" + ("%d"%el.absorption_k if el.absorption_k else   "") + "</td></tr>" +
        "<tr><td>L<sub>I</sub>   </td><td align='right'>" + ("%d"%el.absorption_l1 if el.absorption_l1 else "") + "</td></tr>" +
        "<tr><td>L<sub>II</sub>  </td><td align='right'>" + ("%d"%el.absorption_l2 if el.absorption_l2 else "") + "</td></tr>" +
        "<tr><td>L<sub>III</sub> </td><td align='right'>" + ("%d"%el.absorption_l3 if el.absorption_l3 else "") + "</td></tr>")
        
        self.label3.setText(
        "<tr><td>K<sub>&alpha;1</sub>  </td><td align='right'>" + ("%d"%el.emission_ka1 if el.emission_ka1 else "") + "</td></tr>" +
        "<tr><td>K<sub>&alpha;2</sub>  </td><td align='right'>" + ("%d"%el.emission_ka2 if el.emission_ka2 else "") + "</td></tr>" +
        "<tr><td>K<sub>&beta;1</sub>   </td><td align='right'>" + ("%d"%el.emission_kb1 if el.emission_kb1 else "") + "</td></tr>" +
        "<tr><td>L<sub>&alpha;1</sub>  </td><td align='right'>" + ("%d"%el.emission_la1 if el.emission_la1 else "") + "</td></tr>" +
        "<tr><td>L<sub>&alpha;2</sub>  </td><td align='right'>" + ("%d"%el.emission_la2 if el.emission_la2 else "") + "</td></tr>" +
        "<tr><td>L<sub>&beta;1</sub>   </td><td align='right'>" + ("%d"%el.emission_lb1 if el.emission_lb1 else "") + "</td></tr>" +
        "<tr><td>L<sub>&beta;2</sub>   </td><td align='right'>" + ("%d"%el.emission_lb2 if el.emission_lb2 else "") + "</td></tr>" +
        "<tr><td>L<sub>&gamma;1</sub>  </td><td align='right'>" + ("%d"%el.emission_lg1 if el.emission_lg1 else "") + "</td></tr>" )
        
        
        
class MainWidget(QtGui.QWidget):
    def __init__(self, parent=None):

        QtGui.QWidget.__init__(self, parent)
        self.setWindowTitle('Periodic Table Xray')
        self.buttons = []
        layout = QtGui.QGridLayout(self)
        for el in ELEMENTS:
            but = QtGui.QPushButton(str(el.number) + "\n" + str(el.symbol))
            self.buttons.append(but)
            but.setObjectName(el.block)
            but.number = el.number
            but.clicked.connect(self.changeElement)  
            p, g = -1, -1
            if (58 <= el.number <= 71):
                p, g = 1, el.number - 59
            if (90 <= el.number <= 103):  
                p, g = 1, el.number - 91 
            layout.addWidget(but, el.period + p , el.group + g)
            
        self.detailsWidget = Details()
        layout.addWidget(self.detailsWidget, 0, 3, 3, 8)    
        self.setLayout(layout)
        self.setStyleSheet(readStyleSheet('blackstyle.css'))
    
    def changeElement(self):
        s = self.sender()
        for but in self.buttons:
            if but.number == self.detailsWidget.currentElement:
                but.setProperty("selected", False)               
        s.setProperty("selected", True)
        self.setStyleSheet(readStyleSheet('blackstyle.css'))
        self.detailsWidget.update(s.number)
  

def main():
    
    app = QtGui.QApplication(sys.argv)

    w = MainWidget()
    w.setFixedSize(900, 600)
    w.move(100, 100)
    w.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()