import os
from subprocess import call
from search import Search
from document_canonize import DocumentDB
from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtWidgets import *
from PyQt6.QtGui import QDesktopServices


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle('Document search')
        self.setFixedSize(460, 400)
        self.document_db = DocumentDB()

        self.setup_find_widget_group()


    def setup_find_widget_group(self):
        find_edit = QLineEdit(self)
        find_edit.setPlaceholderText('Input search request and press Enter...')
        find_edit.setFixedWidth(350)
        find_edit.move(5, 10)
        self.find_edit = find_edit

        add_document_button = QPushButton(self)
        add_document_button.setText('Add Document')
        add_document_button.setFixedWidth(100)
        add_document_button.move(355, 10)

        words_list = QListWidget(self)
        words_list.setFixedSize(450, 350)
        words_list.move(5, 45)
        words_list.setSortingEnabled(True)
        self.output_list = words_list

        words_list.itemClicked.connect(self.on_file_click)
        find_edit.returnPressed.connect(self.new_search)
        add_document_button.clicked.connect(self.add_document)


    def on_file_click(self, item):
        file_path = item.text().split(' ')[0]
        if os.path.exists(file_path):
            QDesktopServices.openUrl(QUrl.fromLocalFile(file_path)) # For Windows builds
            #call(["xdg-open", file_path]) # For Linux builds
        else:
            print(f'[Error] File {file_path} was moved or deleted.')
            QMessageBox.warning(self, 'File does not exist', f'File {file_path} was moved or deleted.')

    def new_search(self):
        raw_search = self.find_edit.text()
        self.output_list.clear()
        if raw_search == '':
            return

        search = Search()
        true_search = search.get_efficient_words_from_text(raw_search).keys()
        files = self.document_db.find_relative_documents(true_search, 0)
        for file in files:
            new_item = QListWidgetItem(f'{file[0]}')
            self.output_list.addItem(new_item)


    def add_document(self):
        file_name, _ = QFileDialog().getOpenFileName(self, 'Source Text', '', 'Text files (*.txt)')
        if file_name == '':
            return

        with open(file_name, 'r', encoding="utf8") as text:
            self.document_db.add_document(file_name, text.read())