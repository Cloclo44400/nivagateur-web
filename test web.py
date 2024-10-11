import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *

class Navigateur(QMainWindow):
    def __init__(self):
        super(Navigateur, self).__init__()
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl("http://www.google.com"))  # Page d'accueil
        self.setCentralWidget(self.browser)

        # Barre de navigation
        self.navigation_bar = QToolBar()
        self.addToolBar(self.navigation_bar)

        # Bouton retour
        self.retour_bouton = QAction("Retour", self)
        self.retour_bouton.triggered.connect(self.browser.back)
        self.navigation_bar.addAction(self.retour_bouton)

        # Bouton suivant
        self.suivant_bouton = QAction("Suivant", self)
        self.suivant_bouton.triggered.connect(self.browser.forward)
        self.navigation_bar.addAction(self.suivant_bouton)

        # Bouton actualiser
        self.actualiser_bouton = QAction("Actualiser", self)
        self.actualiser_bouton.triggered.connect(self.browser.reload)
        self.navigation_bar.addAction(self.actualiser_bouton)

        # Champ de texte pour saisir une URL
        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.naviguer)
        self.navigation_bar.addWidget(self.url_bar)

        # Connecte la modification de l'URL à la méthode de mise à jour de la barre d'adresse
        self.browser.urlChanged.connect(self.mise_a_jour_url_bar)

    # Méthode pour naviguer vers une URL
    def naviguer(self):
        url = self.url_bar.text()
        self.browser.setUrl(QUrl(url))

    # Mise à jour de la barre d'adresse lorsque la page change
    def mise_a_jour_url_bar(self, q):
        self.url_bar.setText(q.toString())

# Exécution de l'application
app = QApplication(sys.argv)
QApplication.setApplicationName("Navigateur Simple")
fenetre = Navigateur()
fenetre.show()
sys.exit(app.exec_())
