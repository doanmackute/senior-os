from PyQt5.QtWidgets import QMainWindow, QApplication, QMenu, QStyle, QLabel, QVBoxLayout
from PyQt5.QtWidgets import QLineEdit, QPushButton, QAction, QToolBar, QToolTip, QLineEdit, QHBoxLayout, QWidget, QSizePolicy
from PyQt5.QtGui import QIcon
from urllib.parse import urlparse
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtCore import QEvent, QObject, QUrl, QPoint, Qt, QTimer, QSize
import sys
import os

class MyBrowser(QMainWindow):
    # Define the contructor for initialization 
    def __init__(self):
        super(MyBrowser,self).__init__()
        self.initUI()  
        
    # Definuje inicializace pro User Interface Define init for UI
    def initUI(self):
        self.browser = QWebEngineView()
        self.setCentralWidget(self.browser)
        self.showMaximized()
        
        # Disable nativni globalni efektu Tooltip
        QApplication.setEffectEnabled(Qt.UI_FadeTooltip, False)
        QApplication.setEffectEnabled(Qt.UI_AnimateTooltip, False)
        
        # Definuje Home Page pro Web Browser
        # Pouzivanim .html file a os metoda na definici cesty k souboru HTML
        html_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'homepage.html')
        self.browser.setUrl(QUrl.fromLocalFile(html_path))
        
        # Funkce URL bar
        self.browser.urlChanged.connect(self.update_url)
        self.browser.titleChanged.connect(self.update_title)
        
        # Vytvorit toolbar pro ulozeni URL navigace
        url_toolbar = QToolBar("URL Navigation")
        self.addToolBar(url_toolbar)
        self.addToolBarBreak()
        
        #Vytvorit toolbar pro ulozeni Buttons navigace
        buttons_toolbar = QToolBar("Buttons Navigation")
        self.addToolBar(buttons_toolbar)
        
        # Nastavit styl pro button toolbar navigaci
        buttons_toolbar.setStyleSheet("""
             QToolBar {
                background-color: #c2ad99;   /*Svetla modra */
                border: none;               
                spacing: 20px;              /*Mezera mezi toolbar*/
                border-radius: 5px;
            }
            
            /* Nastavit parametry pro button v Toolbar*/
            QPushButton {
                background-color: #350345;
                color: white;              
                padding: 8px 16px;          /* Padding okoli textu */
                border: none;               
                border-radius: 5px;         /* Rounded corners */
                font-size: 30px;            /* Font Velikosti */
                font-weight: bold;
            }
            
            QPushButton:hover {
                background-color: #0267ab; 
            }
            
            QPushButton QLabel {
                font: 30px Arial;            /* Font Velikosti */
                font-weight: bold;
                color: white;
            }
        """)
        
        # Dva mezera pro ulozeni na zacatku a konci Button navigace (Button bude v uprostred)
        first_spacer = QWidget()
        first_spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        second_spacer = QWidget()
        second_spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        # Nastavit maximalni vysku pro Button a URL navigace
        buttons_toolbar.setFixedHeight(168)
        url_toolbar.setMaximumHeight(150)
        
        # Ulozit prvni mezero na Button navigace
        buttons_toolbar.addWidget(first_spacer)
        
        # Pridat Menu tlacitko s icon
        menu_btn = QPushButton(self)
        # Ulozit QvBoxLayout uvnitr Menu tlacitko
        menu_layout = QVBoxLayout(menu_btn)
        # Qlabel pro icon
        menu_icon = self.style().standardIcon(QStyle.SP_FileDialogDetailedView)
        menu_label = QLabel(menu_btn)
        menu_label.setPixmap(menu_icon.pixmap(QSize(75,75)))
        menu_layout.addWidget(menu_label)
        # Qlabel pro text
        menu_text_label = QLabel("Menu",menu_btn)
        menu_layout.addWidget(menu_text_label)
        # Poradat vsechny uprostred
        menu_layout.setAlignment(menu_label,Qt.AlignCenter)
        menu_layout.setAlignment(menu_text_label,Qt.AlignCenter)
        menu_btn.setToolTip("Kliknutím se zobrazit více možnosti")
        menu_btn.setFixedSize(175,150)
        # Vynenit cursor do ruky
        menu_btn.setCursor(Qt.PointingHandCursor)
        # Nastavit hover status na False
        menu_btn.hovered = False  
        # Mouse enter a leave event pro Zobrazeni tooltip
        menu_btn.enterEvent = self.create_show_tooltip_event(menu_btn)
        menu_btn.leaveEvent = self.create_hide_tooltip_event(menu_btn)
        buttons_toolbar.addWidget(menu_btn)
        
        # Vytvorit zobrazeni s vice moznosti
        switch_menu = QMenu(self)
        switch_menu.setStyleSheet("""
        QMenu {
            background-color: #350345;
            color: #FFFFFF;
            border: 2px solid black;
            border-radius: 5px; 
            padding: 5px;
            border-radius: 5px;
        }

        QMenu::item {
            /* Top botton left right*/
            padding: 10px 10px 5px 30px;
            font-family: Arial;
            font-size: 25px;
            font-weight: bold; 
            width: 150px;
            text-align: left;
            border-radius: 5px;
        }

        QMenu::item:selected {
            background-color: #0267ab;
        }
        
        QMenu::separator {
            height: 1px;
            background: white;
            margin-left: 10px;
            margin-right: 5px;
}                              
        
        """)
        option1_menu = switch_menu.addAction("Option 1")
        option1_menu.triggered.connect(self.option1_selected)
        switch_menu.addSeparator()
        option2_menu = switch_menu.addAction("Option 2")
        option2_menu.triggered.connect(self.option2_selected)
        switch_menu.addSeparator()
        option3_menu = switch_menu.addAction("Option 3")
        option3_menu.triggered.connect(self.option3_selected)
        switch_menu.addSeparator()
        option4_menu = switch_menu.addAction("Option 4")
        option4_menu.triggered.connect(self.option4_selected)
        switch_menu.addSeparator()
        option5_menu = switch_menu.addAction("Option 5")
        option5_menu.triggered.connect(self.option5_selected)
        
        menu_btn.setMenu(switch_menu)
        
        # Pridat Mezero mezi dvema button
        spacer = QWidget()
        spacer.setFixedSize(25,1)
        buttons_toolbar.addWidget(spacer)
        
        # Pridat Home tlacitko s icon
        home_btn = QPushButton(self)
        # Ulozit QvBoxLayout
        home_layout = QVBoxLayout(home_btn)
        # Qlabel pro icon
        home_icon = self.style().standardIcon(QStyle.SP_DirHomeIcon)
        home_label = QLabel(home_btn)
        home_label.setPixmap(home_icon.pixmap(QSize(75,75)))
        home_layout.addWidget(home_label)
        # Qlabel pro text
        home_text_label = QLabel("Home", home_btn)
        home_layout.addWidget(home_text_label)
        # Poradat vsechny uprostred
        home_layout.setAlignment(home_label,Qt.AlignCenter)
        home_layout.setAlignment(home_text_label,Qt.AlignCenter)
        home_btn.clicked.connect(self.navigate_home)
        home_btn.setToolTip("Kliknutím se vrátit na domovskou stránku")
        home_btn.setFixedSize(175,150)
        # vynenit cursor do ruky
        home_btn.setCursor(Qt.PointingHandCursor)
        # Nastavit hover status na False
        home_btn.hovered = False  
        # Mouse enter a leave event pro Zobrazeni tooltip
        home_btn.enterEvent = self.create_show_tooltip_event(home_btn)
        home_btn.leaveEvent = self.create_hide_tooltip_event(home_btn)
        buttons_toolbar.addWidget(home_btn)
        
        # Pridat Mezero mezi dvema button
        spacer = QWidget()
        spacer.setFixedSize(25, 1)
        buttons_toolbar.addWidget(spacer)
        
        # Pridat Back tlacitko s icon
        back_btn = QPushButton(self)
        # Ulozit QvBoxLayout unitr Back Button
        back_layout = QVBoxLayout(back_btn)
        # Qlabel pro icon
        back_icon = self.style().standardIcon(QStyle.SP_ArrowBack)
        back_label = QLabel(back_btn)
        back_label.setPixmap(back_icon.pixmap(QSize(75,75)))
        back_layout.addWidget(back_label)
        # Qlabel pro text
        back_text_label = QLabel("Back",back_btn)
        back_layout.addWidget(back_text_label)
        # Poradat vsechny uprestred
        back_layout.setAlignment(back_label,Qt.AlignCenter)
        back_layout.setAlignment(back_text_label,Qt.AlignCenter)
        back_btn.clicked.connect(self.browser.back)
        back_btn.setToolTip("Kliknutím se vrátit zpět")
        back_btn.setFixedSize(175,150)
        # Vynenit cursor do ruky
        back_btn.setCursor(Qt.PointingHandCursor)
        # Nastavit hover status na False
        back_btn.hovered = False  
        # Mouse enter a leave event pro zobrazeni tooltip
        back_btn.enterEvent = self.create_show_tooltip_event(back_btn)
        back_btn.leaveEvent = self.create_hide_tooltip_event(back_btn)
        buttons_toolbar.addWidget(back_btn)
        
        # Pridat Mezero mezi dvema button
        spacer = QWidget()
        spacer.setFixedSize(25, 1)
        buttons_toolbar.addWidget(spacer)

        # Pridat Forward tlacitko s icon
        forward_btn = QPushButton(self)
        # Ulozit QVBoxLayout
        forward_layout = QVBoxLayout(forward_btn)
        # Qlabel pro icon
        forward_icon = self.style().standardIcon(QStyle.SP_ArrowForward)
        forward_label = QLabel(forward_btn)
        forward_label.setPixmap(forward_icon.pixmap(QSize(75,75)))
        forward_layout.addWidget(forward_label)
        # Qlabel pro text
        forward_text_label = QLabel("Forward",forward_btn)
        forward_layout.addWidget(forward_text_label)
        # Poradat vsechny uprestred
        forward_layout.setAlignment(forward_label,Qt.AlignCenter)
        forward_layout.setAlignment(forward_text_label,Qt.AlignCenter)       
        forward_btn.setFixedSize(175,150)
        forward_btn.clicked.connect(self.browser.forward)
        forward_btn.setToolTip("Kliknutím se vrátit vpřed")
        # Vynenit cursor do ruky
        forward_btn.setCursor(Qt.PointingHandCursor)
        # Nastavit hover status na False
        forward_btn.hovered = False
        # Mouse enter a leave event pro Zobrazeni tooltip
        forward_btn.enterEvent = self.create_show_tooltip_event(forward_btn)
        forward_btn.leaveEvent = self.create_hide_tooltip_event(forward_btn)
        buttons_toolbar.addWidget(forward_btn)
        
        # Pridat Mezero mezi dvema button
        spacer = QWidget()
        spacer.setFixedSize(25, 1)
        buttons_toolbar.addWidget(spacer)
        
        # Pridat Reload tlacitko s icon
        reload_btn = QPushButton(self)
        # Ulozit QVBoxLayout
        reload_layout = QVBoxLayout(reload_btn)
        # Qlabel pro icon
        reload_icon = self.style().standardIcon(QStyle.SP_BrowserReload)
        reload_label = QLabel(reload_btn)
        reload_label.setPixmap(reload_icon.pixmap(QSize(80,80)))
        reload_layout.addWidget(reload_label)
        # Qlabel pro text
        reload_text_label = QLabel("Reload",reload_btn)
        reload_layout.addWidget(reload_text_label)
        # Poradat vsechny uprestred
        reload_layout.setAlignment(reload_label,Qt.AlignCenter)
        reload_layout.setAlignment(reload_text_label,Qt.AlignCenter)   
        reload_btn.clicked.connect(self.reload_and_go_to_top)
        reload_btn.setToolTip("Kliknutím znovu načíst a vrátit na vrchol")
        reload_btn.setFixedSize(175,150)
        # vynenit cursor do ruky
        reload_btn.setCursor(Qt.PointingHandCursor)
        # Nastavit hover status na False
        reload_btn.hovered = False 
        # Mouse enter a leave event pro Zobrazeni tooltip
        reload_btn.enterEvent = self.create_show_tooltip_event(reload_btn)
        reload_btn.leaveEvent = self.create_hide_tooltip_event(reload_btn)
        buttons_toolbar.addWidget(reload_btn)
        self.browser.loadFinished.connect(self.scroll_to_top)
        
        # Pridat mezera mezi dvema Button
        spacer = QWidget()
        spacer.setFixedSize(25,1)
        buttons_toolbar.addWidget(spacer)
        
        # Pridat prvni tlacitko pro navigaci zpravy
        new1_btn = QPushButton(self)
        # Ulozit QVBoxLayout
        new1_layout = QVBoxLayout(new1_btn)
        # Qlabel pro icon
        new1_icon = self.style().standardIcon(QStyle.SP_FileDialogContentsView)
        new1_label = QLabel(new1_btn)
        new1_label.setPixmap(new1_icon.pixmap(QSize(50,50)))
        new1_layout.addWidget(new1_label)
        # Qlabel pro text
        new1_text_label = QLabel("New #1",new1_btn)
        new1_layout.addWidget(new1_text_label)
        # Poradat vsechny uprestred
        new1_layout.setAlignment(new1_label,Qt.AlignCenter)
        new1_layout.setAlignment(new1_text_label,Qt.AlignCenter)   
        new1_btn.clicked.connect(self.navigate_new1)
        new1_btn.setToolTip("Kliknutím přesměrovat na seznam.cz")
        new1_btn.setFixedSize(175,150)
        # vynenit cursor do ruky
        new1_btn.setCursor(Qt.PointingHandCursor)
        # Nastavit hover status na False
        new1_btn.hovered = False 
        # Mouse enter a leave event pro Zobrazeni tooltip
        new1_btn.enterEvent = self.create_show_tooltip_event(new1_btn)
        new1_btn.leaveEvent = self.create_hide_tooltip_event(new1_btn)
        buttons_toolbar.addWidget(new1_btn)
        
        # Pridat mezera mezi dvema Button
        spacer = QWidget()
        spacer.setFixedSize(25,1)
        buttons_toolbar.addWidget(spacer)
        
        # Pridat druhe tlacitko pro navigaci zpravy
        new2_btn = QPushButton(self)
        # Ulozit QVBoxLayout
        new2_layout = QVBoxLayout(new2_btn)
        # Qlabel pro icon
        new2_icon = self.style().standardIcon(QStyle.SP_FileDialogContentsView)
        new2_label = QLabel(new2_btn)
        new2_label.setPixmap(new2_icon.pixmap(QSize(50,50)))
        new2_layout.addWidget(new2_label)
        # Qlabel pro text
        new2_text_label = QLabel("New #2",new2_btn)
        new2_layout.addWidget(new2_text_label)
        # Poradat vsechny uprestred
        new2_layout.setAlignment(new2_label,Qt.AlignCenter)
        new2_layout.setAlignment(new2_text_label,Qt.AlignCenter)   
        new2_btn.clicked.connect(self.navigate_new2)
        new2_btn.setToolTip("Kliknutím přesměrovat na ct24.ceskatelevize.cz")
        new2_btn.setFixedSize(175,150)
        # vynenit cursor do ruky
        new2_btn.setCursor(Qt.PointingHandCursor)
        # Nastavit hover status na False
        new2_btn.hovered = False 
        # Mouse enter a leave event pro Zobrazeni tooltip
        new2_btn.enterEvent = self.create_show_tooltip_event(new2_btn)
        new2_btn.leaveEvent = self.create_hide_tooltip_event(new2_btn)
        buttons_toolbar.addWidget(new2_btn)
        
        # Pridat mezera mezi dvema Button
        spacer = QWidget()
        spacer.setFixedSize(25,1)
        buttons_toolbar.addWidget(spacer)
        
        # Pridat treti tlacitko pro navigaci zpravy
        new3_btn = QPushButton(self)
        # Ulozit QVBoxLayout
        new3_layout = QVBoxLayout(new3_btn)
        # Qlabel pro icon
        new3_icon = self.style().standardIcon(QStyle.SP_FileDialogContentsView)
        new3_label = QLabel(new3_btn)
        new3_label.setPixmap(new3_icon.pixmap(QSize(50,50)))
        new3_layout.addWidget(new3_label)
        # Qlabel pro text
        new3_text_label = QLabel("New #3",new3_btn)
        new3_layout.addWidget(new3_text_label)
        # Poradat vsechny uprestred
        new3_layout.setAlignment(new3_label,Qt.AlignCenter)
        new3_layout.setAlignment(new3_text_label,Qt.AlignCenter)   
        new3_btn.clicked.connect(self.navigate_new3)
        new3_btn.setToolTip("Kliknutím přesměrovat na irozhlas.cz")
        new3_btn.setFixedSize(175,150)
        # vynenit cursor do ruky
        new3_btn.setCursor(Qt.PointingHandCursor)
        # Nastavit hover status na False
        new3_btn.hovered = False 
        # Mouse enter a leave event pro Zobrazeni tooltip
        new3_btn.enterEvent = self.create_show_tooltip_event(new3_btn)
        new3_btn.leaveEvent = self.create_hide_tooltip_event(new3_btn)
        buttons_toolbar.addWidget(new3_btn)
        
        # Ulozit druhe mezero na konci Button navigace
        buttons_toolbar.addWidget(second_spacer)
   
        # Pridat URL hledani, URL vymena funkce
        self.url_bar = QLineEdit()
        self.url_bar.setAlignment(Qt.AlignCenter)
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        self.url_bar.setPlaceholderText("Zadejte URL nebo vyhledejte...")
        # Vymenit parametr URL toolbar
        self.url_bar.setStyleSheet("""
        QLineEdit {
            font-family: "Arial";
            font-size: 16px;
            font-weight: bold;
            border: 3px solid #ede9df; 
            border-radius: 5px;
            background-color: white;
            padding: 2px;
            box-shadow: 4px 4px 6px rgba(0, 0, 0, 0.1);            
        }
        
        QLineEdit:hover {
            border: 2px solid #656565;
            padding: 2px;
        }
        
        QLineEdit:focus {
            border: 2px solid #0078d4;
            padding: 3px;
        }                 
        """)
        self.url_bar.setClearButtonEnabled(True)
        self.browser.urlChanged.connect(self.update_url)
        #self.url_bar.security_icon_action = self.url_bar.addAction(QIcon(),QLineEdit.TrailingPosition)
        #self.url_bar.textChanged.connect(self.check_url)
        url_toolbar.addWidget(self.url_bar)
 
 
    #def check_url(self,url):
        #if url.startswith("https://"):
            #self.url_bar.security_icon_action.setIcon(QIcon("home_icon.png"))
        #else:
            #self.url_bar.security_icon_action.setIcon(QIcon("home_icon.png"))
            
    # Metoda pro vraceni Home Page
    def navigate_home(self):
        html_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'homepage.html')
        self.browser.setUrl(QUrl.fromLocalFile(html_path))
        
    # Metoda pro nagivaci prvni button news seznam.cz
    def navigate_new1(self):
        self.browser.setUrl(QUrl("https://seznam.cz"))
        
    # Metoda pro nagivaci druhe button news ct24.ceskatelevize.cz
    def navigate_new2(self):
        self.browser.setUrl(QUrl("https://ct24.ceskatelevize.cz"))
        
    # Metoda pro nagivaci prvni button news irozhlas.cz
    def navigate_new3(self):
        self.browser.setUrl(QUrl("https://irozhlas.cz"))

    # Metoda pro navigaci URL
    def navigate_to_url(self):
        # ziskat URL z uzivatele a vymenit do URL
        url = self.url_bar.text().strip()
        # Jestlite "." neni v hledane bar
        if "." not in url:
            url = "https://www.google.com/search?q=" + url
        else:
            # Top Level Domain neni dostupne
            if not any(url.endswith(tld) for tld in [".com", ".org", ".net", ".gor", ".cz"]):
                url = "https://www.google.com/search?q=" + url
        # V pripade URl je prazdne, vychozi https
        if "://" not in url:
            url = "https://" + url

        self.browser.setUrl(QUrl(url))

    # Metoda navigace Update URL
    def update_url(self, q):
        # Nastavit Text pro URL bar
        self.url_bar.setText(q.toString())
        self.url_bar.setCursorPosition(0)
        
    # Metoda pro Aktualizace title
    def update_title(self):
        title = self.browser.page().title()
        self.setWindowTitle(title)
    
    # Metoda pro Reload stranky
    def reload_and_go_to_top(self):
        self.browser.reload()
    
    # Metoda pro prejit k zacatecku stranku (0,0)
    def scroll_to_top(self,ok):
        if ok:
            self.browser.page().runJavaScript("window.scrollTo(0,0);")
    
    # Metoda pro zobrazeni tooltip
    def create_show_tooltip_event(self, btn):
        def event(e):
            btn.hovered = True
            tooltip_point = e.globalPos()
            # Nastavit tooltip misto bude blizko cursoru
            tooltip_point.setY(tooltip_point.y() + 10)
            # Nastavit zpozdeni a kontroluje, ze tooltip je zobrazeno
            QTimer.singleShot(0, lambda: QToolTip.showText(tooltip_point, btn.toolTip()) if btn.hovered else None)
            QPushButton.enterEvent(btn, e)
        return event

    # Metoda pro hide tooltip
    def create_hide_tooltip_event(self, btn):
        def event(e):
            btn.hovered = False
            QToolTip.hideText()
            QPushButton.leaveEvent(btn, e)
        return event
    
    # Still don't add any event on the menu button
    def option1_selected(self):
        print("") 

    def option2_selected(self):
        print("")
        
    def option3_selected(self):
        print("")
        
    def option4_selected(self):
        print("")
        
    def option5_selected(self):
        print("")
    
# Definuje funkci Main
if __name__ == "__main__":
    qApplication = QApplication(sys.argv)
    qApplication.setApplicationName("Web Browser for senior")
    # Nastavit styl pro vsechny ToolTip (Vymenit styl jako CSS)
    qApplication.setStyleSheet("""
        QToolTip {
            font: 25px 'Arial';
            color: black;
            background-color: #f6f7f8;
            padding: 3px;
            border: 1px solid black; /* zakřivené rohy */
            opacity:200;
            border-radius: 5px;
        }
        
        QToolTip::text{
            color: black;
            margin: -2px;
        }
    """)
    mainWindow = MyBrowser()
    mainWindow.show()
    sys.exit(qApplication.exec_())
