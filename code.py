import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QStackedWidget,QLineEdit, QVBoxLayout, QWidget, QLabel,QHBoxLayout
from PyQt5.QtGui import QFont
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from PyQt5 import uic

import matplotlib.pyplot as plt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('C:/interface gestionnaire.ui', self)  # Load the .ui file
        
        # Assuming your QStackedWidget is named 'stackedWidget' in Qt Designer
        self.stacked_widget = self.findChild(QStackedWidget, 'stackedWidget')
        self.stacked_widget.setCurrentIndex(0)
        
        self.lineEdit = self.findChild(QLineEdit, 'lineEdit')
        self.lineEdit_2 = self.findChild(QLineEdit, 'lineEdit_2')
        self.pushButton_6 = self.findChild(QPushButton, 'pushButton_6')
        self.pushButton_6.clicked.connect(self.create_repeated_pages)
        
        self.dynamic_line_edits = []  # List to store references to QLineEdit widgets
        self.user_inputs = []  # List to store user inputs
        
        self.total_repetitions = 0
        
        self.setup_connections()
    
    def setup_connections(self):
        pushButton = self.findChild(QPushButton, 'pushButton')
        pushButton.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))

        pushButton_2 = self.findChild(QPushButton, 'pushButton_2')
        pushButton_2.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(2))

        pushButton_3 = self.findChild(QPushButton, 'pushButton_3')
        pushButton_3.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))

        pushButton_4 = self.findChild(QPushButton, 'pushButton_4')
        pushButton_4.clicked.connect(self.store_value)

        pushButton_5 = self.findChild(QPushButton, 'pushButton_5')
        pushButton_5.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))

        pushButton_6 = self.findChild(QPushButton, 'pushButton_6')
        pushButton_6.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(5))

        pushButton_8 = self.findChild(QPushButton, 'pushButton_8')
        pushButton_8.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))

    def create_repeated_pages(self):
        try:
            self.total_repetitions = int(self.lineEdit_2.text())
        except ValueError:
            print("Please enter a valid number")
            return

        for i in range(self.total_repetitions):
            page = QWidget()
            layout = QVBoxLayout()

            top_label = QLabel("Entrer pour chaque processus :")
            top_label.setFont(QFont("Arial", 18))
            top_label.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
            layout.addWidget(top_label)

            calc_layout = QHBoxLayout()
            calc_label = QLabel("Temps de Calcul")
            calc_label.setFont(QFont("Arial", 16))
            calc_layout.addWidget(calc_label)
            calc_line_edit = QLineEdit()
            calc_line_edit.setFixedWidth(200)
            calc_layout.addWidget(calc_line_edit)
            layout.addLayout(calc_layout)

            read_layout = QHBoxLayout()
            read_label = QLabel("Temps de Lecture Disque")
            read_label.setFont(QFont("Arial", 16))
            read_layout.addWidget(read_label)
            read_line_edit = QLineEdit()
            read_line_edit.setFixedWidth(200)
            read_layout.addWidget(read_line_edit)
            layout.addLayout(read_layout)

            next_button = QPushButton("Next")
            if i < self.total_repetitions - 1:
                next_button.clicked.connect(lambda _, idx=i: self.on_next_button_clicked(idx))
            else:
                next_button.clicked.connect(lambda _, idx=i: self.on_last_next_button_clicked(idx))
            layout.addWidget(next_button, alignment=Qt.AlignHCenter)

            page.setLayout(layout)
            self.stacked_widget.addWidget(page)

            # Store references to the QLineEdit widgets
            self.dynamic_line_edits.append((calc_line_edit, read_line_edit))

            if i == self.total_repetitions-1:
                #self.stacked_widget.setCurrentIndex(4)
                next_button.clicked.connect(self.on_button_clicked2)

        #6self.stacked_widget.setCurrentIndex(4)
    def on_button_clicked2(self):
        self.dynamic_line_edits.append((QLineEdit(), QLineEdit()))
        self.stacked_widget.setCurrentIndex(4)



    def on_next_button_clicked(self, page_index):
        self.store_user_inputs(page_index)
        self.stacked_widget.setCurrentIndex(self.stacked_widget.currentIndex() + 1)

    def on_last_next_button_clicked(self, page_index):
        self.store_user_inputs(page_index)
        self.stacked_widget.setCurrentIndex(self.stacked_widget.count() - 1)
        self.Calculation()
        print("All user inputs:", self.user_inputs)

    def store_user_inputs(self, page_index):
        calc_line_edit, read_line_edit = self.dynamic_line_edits[page_index]
        self.user_inputs.append((calc_line_edit.text(), read_line_edit.text()))
        print("Stored user inputs:", self.user_inputs)

    def store_value(self):
        global valeur # quantum
        entered_value = self.lineEdit.text()
        valeur = int(entered_value)
        print(valeur)
        self.stacked_widget.setCurrentIndex(3)

    def transform_list(self,input_list):
        result = []
        for tup in input_list:
            for num in tup:
                result.append(int(num))
        return result
    def Calculation(self):
        l= self.transform_list(self.user_inputs)
        list1 =[] #burst times
        list2 =[]
        task = []
        task_names =[] #processes
        for adad in range(len(l)):
            if adad%2 == 0:
                list1.append(l[adad])
            if ((adad%1 == 0) and (adad !=0)):
                list2.append(l[adad])
        for i in range(1,int(len(l)//2)+1):
            p=[i,list1[i-1],list2[i-1]]
            task.append(p)
            p=[]
        for kappa in range(1,(len(l)//2 + 1)):
            task_names.append("Task"+str(kappa))
        n = len(task_names)
        remaining_burst_times = list1[:]
        time = 0
        gantt_chart = []

        # Process queue
        while any(remaining_burst_times):
            for i in range(n):
                if remaining_burst_times[i] > 0:
                    start_time = time
                    if remaining_burst_times[i] > valeur:
                        time += valeur
                        remaining_burst_times[i] -= valeur
                    else:
                        time += remaining_burst_times[i]
                        remaining_burst_times[i] = 0
                    end_time = time
                    gantt_chart.append((task_names[i], start_time, end_time))

        # Create the Gantt chart
        fig, gnt = plt.subplots()

         # Set the limits of the x and y axis
        gnt.set_xlim(0, time)
        gnt.set_ylim(0, len(task_names) + 1)

        # Set labels for x and y axis
        gnt.set_xlabel('Time')
        gnt.set_ylabel('Processes')

                    # Set ticks on y-axis
        gnt.set_yticks(range(1, len(task_names) + 1))
        gnt.set_yticklabels(task_names)

        # Plot the tasks
        for i, (process, start, end) in enumerate(gantt_chart):
            gnt.broken_barh([(start, end - start)], (task_names.index(process) + 0.5, 0.9))

        # Save the Gantt chart as an image
        plt.tight_layout()
        plt.savefig('round_robin_gantt_chart.png')
        plt.close()
        pixmap = QPixmap('round_robin_gantt_chart.png')

        # Create a QLabel to display the image
        self.gantt_label = QLabel(self)
        self.gantt_label.setPixmap(pixmap)
        self.gantt_label.setScaledContents(True)

        # Add the QLabel to the specific page of the QStackedWidget
        self.page6_layout = QVBoxLayout(self.page6)  # Assuming page2 is the target page
        self.page6_layout.addWidget(self.gantt_label)
        self.stackedWidget.setCurrentIndex(5)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())