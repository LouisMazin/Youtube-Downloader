from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from animated_toggle import AnimatedToggle
from qt_material import apply_stylesheet
from os import path
import downloader_music
WidthFenetre = 1750
HeightFenetre = 875
HeightButtons = HeightFenetre/17.5
WidthButtons = WidthFenetre/3

class Interface(QMainWindow):
    def __init__(self,app):
        global dpi
        super().__init__()
        dpi = app.primaryScreen().devicePixelRatio()
        self.gridlayout = QGridLayout()
        self.setWindowTitle("Téléchargement Youtube - par Louis")
        self.setCentralWidget(QWidget())
        self.setFixedSize(int(1200/dpi),int(400/dpi))
        self.setWindowIcon(QIcon("icon.ico"))
        
        self.topLayout = QGridLayout()
        
        self.csvLabel = QLabel("Fichier de chansons :")
        self.csvLineEdit = QLineEdit()
        self.csvLineEdit.setText(path.abspath("chansons.csv"))
        self.csvSearch = QPushButton("Parcourir")
        self.csvSearch.clicked.connect(lambda: self.Parcourir("CSV (*.csv)",self.csvLineEdit))
        
        self.toggleMode = AnimatedToggle()
        self.toggleMode.clicked.connect(self.changeMode)
        self.toggleMode.setChecked(True)
        
        self.lienLabel = QLabel("Lien de la vidéo :")
        self.lienLineEdit = QLineEdit()
        self.lienLineEdit.setPlaceholderText("https://www.youtube.com/watch?v=...")
        
        self.topLayout.addWidget(self.csvLabel,0,0)
        self.topLayout.addWidget(self.csvLineEdit,0,1)
        self.topLayout.addWidget(self.csvSearch,0,2)
        self.topLayout.addWidget(self.toggleMode,0,3)
        self.topLayout.addWidget(self.lienLabel,0,4)
        self.topLayout.addWidget(self.lienLineEdit,0,5)
        
        self.midLayout = QGridLayout()
        
        self.artistLabel = QLabel("Artiste :")
        self.artist = QLineEdit()
        self.titleLabel = QLabel("Titre :")
        self.title = QLineEdit()
        self.albumLabel = QLabel("Album :")
        self.album = QLineEdit()
        self.imageLabel = QLabel("Image :")
        self.imageLineEdit = QLineEdit()
        self.parcourirImage = QPushButton("Parcourir")
        self.parcourirImage.clicked.connect(lambda: self.Parcourir("Images (*.jpg *.jpeg *.png)",self.imageLineEdit))
        self.customTagsLabel = QLabel("Tags personnalisés :")
        self.customTags = AnimatedToggle()
        self.customTags.clicked.connect(self.setCustomTags)
        self.customTags.setChecked(True)
        self.customTags.setFixedWidth(int(HeightButtons/dpi*1.5))
        
        self.midLayout.addWidget(self.customTagsLabel,0,0)
        self.midLayout.addWidget(self.customTags,0,1)
        self.midLayout.addWidget(self.artistLabel,1,0)
        self.midLayout.addWidget(self.artist,1,1)
        self.midLayout.addWidget(self.titleLabel,1,2)
        self.midLayout.addWidget(self.title,1,3)
        self.midLayout.addWidget(self.albumLabel,2,0)
        self.midLayout.addWidget(self.album,2,1)
        self.midLayout.addWidget(self.imageLabel,2,2)
        self.midLayout.addWidget(self.imageLineEdit,2,3)
        self.midLayout.addWidget(self.parcourirImage,2,4)
        
        self.bottomLayout = QGridLayout()
        
        self.callbackLabel = QLabel("")
        self.downloadButton = QPushButton("Télécharger")
        self.downloadButton.clicked.connect(self.download)
        
        self.bottomLayout.addWidget(self.downloadButton,1,0)
        self.bottomLayout.addWidget(self.callbackLabel,0,0)
        
        
        self.gridlayout.addLayout(self.topLayout,0,0)
        self.gridlayout.addLayout(self.bottomLayout,2,0)
        self.gridlayout.addLayout(self.midLayout,1,0)
        
        self.centralWidget().setLayout(self.gridlayout)

        self.lienMode = [self.lienLabel,self.lienLineEdit]
        self.fileMode = [self.csvLabel,self.csvLineEdit,self.csvSearch]

        self.changeMode()
        
    def setCustomTags(self):
        if(self.customTags.isChecked()):
            for i in [self.artistLabel,self.artist,self.titleLabel,self.title,self.albumLabel,self.album,self.imageLabel,self.imageLineEdit,self.parcourirImage,self.customTagsLabel,self.customTags]:
                i.setEnabled(True)
        else:
            for i in [self.artistLabel,self.artist,self.titleLabel,self.title,self.albumLabel,self.album,self.imageLabel,self.imageLineEdit,self.parcourirImage]:
                i.setEnabled(False)
                
    def changeMode(self):
        if(self.toggleMode.isChecked()):
            if(self.customTags.isChecked()):
                self.setCustomTags()
            else:
                self.customTagsLabel.setEnabled(True)
                self.customTags.setEnabled(True)
            for i in self.fileMode:
                i.setEnabled(False)
            for i in self.lienMode:
                i.setEnabled(True)
        else:
            if(self.customTags.isChecked()):
                self.customTags.setChecked(False)
                self.setCustomTags()
                self.customTagsLabel.setEnabled(False)
                self.customTags.setEnabled(False)
                self.customTags.setChecked(True)
            else:
                self.customTagsLabel.setEnabled(False)
                self.customTags.setEnabled(False)
            for i in self.fileMode:
                i.setEnabled(True)
            for i in self.lienMode:
                i.setEnabled(False)
                
    def download(self):
        if(self.toggleMode.isChecked() and self.lienLineEdit.text() == "" and (not self.customTags.isChecked())):
            self.callbackLabel.setText('Lien manquant')
            return
        if(not self.toggleMode.isChecked() and path.isfile(self.csvLineEdit.text()) == False):
            self.callbackLabel.setText('Fichier csv introuvable')
            return
        self.callbackLabel.setText("Téléchargement en cours...")
        self.callbackLabel.repaint()
        if(self.toggleMode.isChecked()):
            if(self.customTags.isChecked()):
                self.callbackLabel.setText(downloader_music.main("link",[self.lienLineEdit.text(),self.artist.text(),self.album.text(),self.title.text(),self.imageLineEdit.text()]))
            else:
                self.callbackLabel.setText(downloader_music.main("link",[self.lienLineEdit.text(),"","","",""]))
        else:
            self.callbackLabel.setText(downloader_music.main("csv",[self.csvLineEdit.text()]))
    def Parcourir(self,filter,lineEdit):
        self.filename = QFileDialog.getOpenFileName(self, 'Open File', 'c:\\', filter)
        lineEdit.setText(self.filename[0])
def run():
    app = QApplication([])
    window = Interface(app)
    apply_stylesheet(app, theme='dark_amber.xml')
    app.setStyleSheet(app.styleSheet()+"""*{background-color: transparent;color: #ffffff;border: none;padding: 0;margin: 0;line-height: 0;font-family: "Segoe UI", sans-serif;}QWidget{color: #ffffff;}QLabel{color: #ffffff;}""")
    window.show()
    app.exec()
