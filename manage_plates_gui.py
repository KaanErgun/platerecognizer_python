import sys
import json
import os
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit, QMessageBox

PLATES_FILE = 'plates.json'

def load_plates():
    if os.path.exists(PLATES_FILE):
        with open(PLATES_FILE, 'r') as file:
            return json.load(file)
    return []

def save_plates(plates):
    with open(PLATES_FILE, 'w') as file:
        json.dump(plates, file, indent=4)

class PlateManager(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle('Plate Manager')
        
        self.layout = QVBoxLayout()
        
        self.plate_input = QLineEdit(self)
        self.plate_input.setPlaceholderText('Plate')
        self.layout.addWidget(self.plate_input)
        
        self.color_input = QLineEdit(self)
        self.color_input.setPlaceholderText('Color')
        self.layout.addWidget(self.color_input)
        
        self.owner_name_input = QLineEdit(self)
        self.owner_name_input.setPlaceholderText('Owner Name')
        self.layout.addWidget(self.owner_name_input)
        
        self.owner_surname_input = QLineEdit(self)
        self.owner_surname_input.setPlaceholderText('Owner Surname')
        self.layout.addWidget(self.owner_surname_input)
        
        self.phone_number_input = QLineEdit(self)
        self.phone_number_input.setPlaceholderText('Phone Number')
        self.layout.addWidget(self.phone_number_input)
        
        self.apartment_number_input = QLineEdit(self)
        self.apartment_number_input.setPlaceholderText('Apartment Number')
        self.layout.addWidget(self.apartment_number_input)
        
        self.add_button = QPushButton('Add Plate', self)
        self.add_button.clicked.connect(self.add_plate)
        self.layout.addWidget(self.add_button)
        
        self.remove_button = QPushButton('Remove Plate', self)
        self.remove_button.clicked.connect(self.remove_plate)
        self.layout.addWidget(self.remove_button)
        
        self.list_button = QPushButton('List Plates', self)
        self.list_button.clicked.connect(self.list_plates)
        self.layout.addWidget(self.list_button)
        
        self.plates_list = QTextEdit(self)
        self.plates_list.setReadOnly(True)
        self.layout.addWidget(self.plates_list)
        
        self.setLayout(self.layout)
    
    def add_plate(self):
        plate = self.plate_input.text().strip()
        color = self.color_input.text().strip() or None
        owner_name = self.owner_name_input.text().strip() or None
        owner_surname = self.owner_surname_input.text().strip() or None
        phone_number = self.phone_number_input.text().strip() or None
        apartment_number = self.apartment_number_input.text().strip() or None
        
        if not plate:
            QMessageBox.warning(self, 'Error', 'Plate cannot be empty.')
            return
        
        plates = load_plates()
        for p in plates:
            if p['plate'] == plate:
                QMessageBox.warning(self, 'Error', f"Plate {plate} already exists.")
                return
        
        new_plate = {
            'plate': plate,
            'color': color,
            'owner_name': owner_name,
            'owner_surname': owner_surname,
            'phone_number': phone_number,
            'apartment_number': apartment_number
        }
        plates.append(new_plate)
        save_plates(plates)
        QMessageBox.information(self, 'Success', f"Plate {plate} added successfully.")
        self.clear_inputs()
        
    def remove_plate(self):
        plate = self.plate_input.text().strip()
        
        if not plate:
            QMessageBox.warning(self, 'Error', 'Plate cannot be empty.')
            return
        
        plates = load_plates()
        plates = [p for p in plates if p['plate'] != plate]
        save_plates(plates)
        QMessageBox.information(self, 'Success', f"Plate {plate} removed successfully.")
        self.clear_inputs()
    
    def list_plates(self):
        plates = load_plates()
        self.plates_list.clear()
        for p in plates:
            self.plates_list.append(json.dumps(p, indent=4))
    
    def clear_inputs(self):
        self.plate_input.clear()
        self.color_input.clear()
        self.owner_name_input.clear()
        self.owner_surname_input.clear()
        self.phone_number_input.clear()
        self.apartment_number_input.clear()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = PlateManager()
    ex.show()
    sys.exit(app.exec_())
