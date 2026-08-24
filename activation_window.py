# -*- coding: utf-8 -*-
import sys
import json
import os

# إضافة المسارات للمكتبات المستخرجة والملفات الديناميكية (.dll و .pyd)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
EXTRACTED_DIR = r"C:\Users\mosta\.gemini\antigravity-ide\brain\c324b4b1-2eec-456b-ba79-d613b00ede16\scratch\SE BOT.exe_extracted"
PYZ_DIR = os.path.join(EXTRACTED_DIR, "PYZ.pyz_extracted")

for p in [EXTRACTED_DIR, PYZ_DIR, os.path.join(EXTRACTED_DIR, "PyQt5", "Qt5", "bin"), os.path.join(EXTRACTED_DIR, "nacl")]:
    if os.path.exists(p):
        if p not in sys.path:
            sys.path.insert(0, p)
        if p not in os.environ.get('PATH', ''):
            os.environ['PATH'] = p + ';' + os.environ.get('PATH', '')

from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QMessageBox, QFormLayout
)
from PyQt5.QtGui import QIntValidator
from PyQt5.QtCore import Qt

from main_window import TradingBotUI

# ==============================================================================
# 🔑 كلمة المرور الثابتة لنظام التفعيل (يمكنك تغييرها إلى أي كلمة تختارها)
# ==============================================================================
STATIC_PASSWORD = "123456"

APP_NAME = "S_E2t1's Application"
APP_VERSION = "1.0"

def get_app_path():
    '''
    تعيد المسار الصحيح للملف سواء كنا في VS Code أو في ملف EXE
    '''
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))


class ActivationWindow(QWidget):
    
    def __init__(self=None):
        super().__init__()
        self.main_bot_window = None
        self.init_ui()
        self.load_activation_data()

    def init_ui(self):
        self.setWindowTitle('ℵ S_E ℵ MT5 Bot Activation')
        self.setGeometry(600, 300, 450, 220)
        self.setStyleSheet('background-color: #1c1c1c; color: white; font-family: Arial;')
        
        layout = QVBoxLayout()
        form_layout = QFormLayout()
        
        self.key_label = QLabel('🔑 Activation Key / Password:')
        self.key_input = QLineEdit()
        self.key_input.setEchoMode(QLineEdit.Password)
        self.key_input.setPlaceholderText('Enter Password')
        
        self.account_label = QLabel('💳 MT5 Account Number:')
        self.account_input = QLineEdit()
        self.account_input.setPlaceholderText('e.g. 12345678')
        
        self.onlyInt = QIntValidator()
        self.account_input.setValidator(self.onlyInt)
        
        for field in (self.key_input, self.account_input):
            field.setStyleSheet('background-color: #333; color: white; padding: 8px; border-radius: 4px;')
            field.setAlignment(Qt.AlignCenter)
            
        form_layout.addRow(self.key_label, self.key_input)
        form_layout.addRow(self.account_label, self.account_input)
        
        self.button = QPushButton('Activate & Launch Bot')
        self.button.setStyleSheet('background-color: #00cc66; color: white; font-weight: bold; padding: 10px; border-radius: 5px;')
        self.button.clicked.connect(self.activate_key)
        
        layout.addLayout(form_layout)
        layout.addWidget(self.button)
        self.setLayout(layout)

    def save_activation_data(self, account_id, license_key):
        data = {
            'saved_account_id': account_id,
            'saved_license_key': license_key
        }
        file_path = os.path.join(get_app_path(), 'license_config.json')
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            print(f'Error saving license data: {e}')

    def load_activation_data(self):
        file_path = os.path.join(get_app_path(), 'license_config.json')
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                saved_acc = data.get('saved_account_id', '')
                saved_key = data.get('saved_license_key', '')
                if saved_key:
                    self.key_input.setText(str(saved_key))
                if saved_acc:
                    self.account_input.setText(str(saved_acc))
            except Exception as e:
                print(f'Error loading license data: {e}')

    def activate_key(self):
        key = self.key_input.text().strip()
        mt5_account_number = self.account_input.text().strip()
        
        if not key or not mt5_account_number:
            QMessageBox.critical(self, 'Error', 'Please enter both the key/password and the MT5 account number.')
            return
            
        if not mt5_account_number.isdigit():
            QMessageBox.critical(self, 'Input Error', 'Account Number must contain digits only!')
            return

        # 🔒 التحقق من كلمة المرور الثابتة المحلية
        if key != STATIC_PASSWORD:
            QMessageBox.critical(self, 'Activation Failed', 'Invalid activation key or password!')
            return

        # حفظ التفعيل وافتتاح البوت
        self.save_activation_data(mt5_account_number, key)
        QMessageBox.information(self, 'Success', 'Activation successful! The bot will now open.')
        self.open_main_window(mt5_account_number)

    def open_main_window(self, activated_account_id):
        self.hide()
        self.main_bot_window = TradingBotUI(activated_account_id=activated_account_id)
        self.main_bot_window.show()


def main():
    app = QApplication(sys.argv)
    window = ActivationWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
