from math import log
from PyQt5.QtWidgets import QMainWindow, QApplication, QMenu, QStyle, QLabel, QVBoxLayout, QMessageBox, QFrame, QToolButton, QMenuBar, QInputDialog
from PyQt5.QtWidgets import QLineEdit, QPushButton, QAction, QToolBar, QToolTip, QLineEdit, QHBoxLayout, QWidget, QSizePolicy
from PyQt5.QtGui import QIcon, QCursor
from urllib.parse import urlparse
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtCore import QEvent, QObject, QUrl, QPoint, Qt, QTimer, QSize
import sys, os, tarfile, json, subprocess
import logging
from datetime import datetime
from loadConfig import *
from functools import partial
from languge_Translator import Translator

# Custom class for creating menu as our input
class CustomMenu(QWidget):
 # Call inicialization funtion with 3 input paramter
    # 1. == ClassMyBrowser, 2. == number of menu, 3. == number of options per menu
    def __init__(self,parent,num_of_menus, num_of_options_per_menu):
        super(CustomMenu, self).__init__()
        # Get MyBrowser as parent for call navigations
        self.parent = parent
        self.layout = QHBoxLayout(self)
        self.num_of_menus = num_of_menus
        self.num_of_options_per_menu = num_of_options_per_menu
        if num_of_menus == 2 and num_of_options_per_menu == 4:
            self.create_menu()
        else:
            self.parent.close()
        self.hovered_action = None
    
    # Create Menu with input menu name and add their  oftion accroding options list [option name, option number]
    def create_menu(self):
        # Create first Menu
        self.menu1_button = QPushButton(self)
        # Create Home QvBoxLayout
        menu1_news_layout = QVBoxLayout(self.menu1_button)
        menu1_news_icon = self.style().standardIcon(QStyle.SP_FileDialogContentsView)
        menu1_news_label = QLabel(self.menu1_button)
        menu1_news_label.setPixmap(menu1_news_icon.pixmap(QSize(self.parent.buttons_icon_width_info,self.parent.buttons_icon_height_info)))
        menu1_news_layout.addWidget(menu1_news_label)
        self.menu1_news_text_label = QLabel("Menu 1", self.menu1_button)
        menu1_news_layout.addWidget(self.menu1_news_text_label)
        # Align text and icon in the center
        menu1_news_layout.setAlignment(menu1_news_label,Qt.AlignCenter)
        menu1_news_layout.setAlignment(self.menu1_news_text_label,Qt.AlignCenter)
        # Change to hand when click cursor
        self.menu1_button.setCursor(Qt.PointingHandCursor)
        self.menu1 = QMenu(self)
        self.menu1_exit = QAction('Exit', self)
        self.menu1_exit.triggered.connect(partial(self.option_triggered, 1))
        self.menu1_www1 = QAction('WWW 1', self)
        self.menu1_www1.triggered.connect(partial(self.option_triggered, 2))
        self.menu1_www2 = QAction('WWW 2', self)
        self.menu1_www2.triggered.connect(partial(self.option_triggered, 3))
        self.menu1_www3 = QAction('WWW 3', self)
        self.menu1_www3.triggered.connect(partial(self.option_triggered, 4))
        self.menu1.addAction(self.menu1_exit)
        self.menu1.addAction(self.menu1_www1)
        self.menu1.addAction(self.menu1_www2)
        self.menu1.addAction(self.menu1_www3)
        self.menu1_button.setMenu(self.menu1)
        # Add menu to layer
        self.layout.addWidget(self.menu1_button)
        
        # Add a blank space between two buttons
        spacer = QWidget()
        spacer.setFixedSize(15, 1)
        self.layout.addWidget(spacer)
        
        # Create second Menu
        self.menu2_button = QPushButton(self)
        # Create Home QvBoxLayout
        menu2_news_layout = QVBoxLayout(self.menu2_button)
        menu2_news_icon = self.style().standardIcon(QStyle.SP_FileDialogContentsView)
        menu2_news_label = QLabel(self.menu2_button)
        menu2_news_label.setPixmap(menu2_news_icon.pixmap(QSize(self.parent.buttons_icon_width_info,self.parent.buttons_icon_height_info)))
        menu2_news_layout.addWidget(menu2_news_label)
        self.menu2_news_text_label = QLabel("Menu 2", self.menu1_button)
        menu2_news_layout.addWidget(self.menu2_news_text_label)
        # Align text and icon in the center
        menu2_news_layout.setAlignment(menu2_news_label,Qt.AlignCenter)
        menu2_news_layout.setAlignment(self.menu2_news_text_label,Qt.AlignCenter)
        # Change to hand when click cursor
        self.menu2_button.setCursor(Qt.PointingHandCursor)
        self.menu2 = QMenu(self)
        self.menu2_www4 = QAction('WWW 4', self)
        self.menu2_www4.triggered.connect(partial(self.option_triggered, 5))
        self.menu2_www5 = QAction('WWW 5', self)
        self.menu2_www5.triggered.connect(partial(self.option_triggered, 6))
        self.menu2_www6 = QAction('WWW 6', self)
        self.menu2_www6.triggered.connect(partial(self.option_triggered, 7))
        self.menu2_address = QAction('Address', self)
        self.menu2_address.triggered.connect(partial(self.option_triggered, 8))
        self.menu2.addAction(self.menu2_www4)
        self.menu2.addAction(self.menu2_www5)
        self.menu2.addAction(self.menu2_www6)
        self.menu2.addAction(self.menu2_address)
        self.menu2_button.setMenu(self.menu2)
        # Add menu to layer
        self.layout.addWidget(self.menu2_button)
        
        # Add a blank space between two buttons
        spacer = QWidget()
        spacer.setFixedSize(15, 1)
        self.layout.addWidget(spacer)

        # Install event filter on the menu
        # Still not work exactly
        self.menu1.installEventFilter(self)
        self.menu2.installEventFilter(self)

    def options_menu_hover(self,action,hover_time,path_to_sound):
        action.hover_timer = QTimer(self)
        action.hover_timer.setInterval(hover_time)
        action.hover_timer.setSingleShot(True)
        action.hover_timer.timeout.connect(partial(self.play_sound_for_option,path_to_sound))
        action.hovered.connect(action.hover_timer.start)
        
    def play_sound_for_option(self, action):
        sound_file = action
        if os.path.exists(sound_file):
            if sound_file.endswith('.wav'):
                subprocess.run(["aplay", sound_file])
            elif sound_file.endswith('.mp3'):
                subprocess.run(["mpg123", sound_file])
        else:
            print(f"Sound file not found: {sound_file}")

    def eventFilter(self, watched, event):
        if event.type() == QEvent.HoverMove and isinstance(watched, QMenu):
        # Get the hovered action based on global cursor position
            action = watched.actionAt(watched.mapFromGlobal(QCursor.pos()))
            # If we hover a different action or move to an empty area of the menu...
            if action != self.hovered_action:
                # Stop the timer of the previously hovered action (if applicable)
                if self.hovered_action and self.hovered_action.hover_timer.isActive():
                    self.hovered_action.hover_timer.stop()
                # Update the hovered_action attribute
                self.hovered_action = action
                # Start the timer of the newly hovered action (if applicable)
                if action:
                    action.hover_timer.start()
            return True
        elif event.type() == QEvent.Leave and isinstance(watched, QMenu):
            # If the cursor leaves the menu, stop the timer of the hovered action (if applicable)
            if self.hovered_action and self.hovered_action.hover_timer.isActive():
                self.hovered_action.hover_timer.stop()
            self.hovered_action = None
            return True
        return super().eventFilter(watched, event)
    
    # Get definition funtion for each type of options from myMainBrowser
    def option_triggered(self, option_number):
        if option_number == 1:
            self.parent.close()
        elif option_number == 2:
            self.parent.navigate_www1()
        elif option_number == 3:
            self.parent.navigate_www2()
        elif option_number == 4:
            self.parent.navigate_www3()
        elif option_number == 5:
            self.parent.navigate_www4()
        elif option_number == 6:
            self.parent.navigate_www5()
        elif option_number == 7:
            self.parent.navigate_www6()
        else:
            self.parent.toggle_url_toolbar()
            
# Call class URL Logger for logging Phishing url to file
# Cisco log: seq no:timestamp: %facility-severity-MNEMONIC:description
class URLLogger:
    def __init__(self, log_file="logPhishing.txt"):
        self.log_file = log_file
        # Ensure the name for log file
        # If the name of file does not exist, create the new file
        # Sequence number initialization
        self.seq_no = 0
        # Ensure that the file is exist
        self._init_txt()

    # Method for creating and opening file .txt
    def _init_txt(self):
        try:
            # Read file with file name
            with open(self.log_file, 'r') as f:
                f.readline()
        except FileNotFoundError:
            # If file does not exist, show use w to create new and write parameter
            with open(self.log_file, 'w') as f:
                f.write("Logging phishing URL from Browser\n")
                
    # Show the the block message to window
    def log_blocked_url(self, url, facility, severity, mnemonic, description):
        logging.warning(f'Blocked URL accessed: {url}. This URL is Phishing')
        self.log_to_txt(url, facility, severity, mnemonic, description)

    # When the URL is blocked from log_blocked_url, save to file .txt
    def log_to_txt(self, url, facility, severity, mnemonic, description):
        self.seq_no += 1
        # Set current time 
        current_time = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
        # seq no:timestamp: %facility-severity-MNEMONIC:description
        log_entry = f"{self.seq_no}\t{current_time}\t{facility}-{severity}-{mnemonic}\t{description}-{url}\n"
        # Write to exising file txt
        with open(self.log_file, 'a') as f:
            f.write(log_entry)
        
# Class for blocking Phishing URL. Using tarfile to extract from file .tar.gz
# Go through all domain in the file
# If the domain is match, take a blocking
class URLBlocker:
    def __init__(self, paths_to_db):
        self.blocked_urls = set()
        # Load file from file path
        for filepath in paths_to_db:
            self.load_urls_from_tar_gz(filepath)
        
    # Read all member in that Domain file
    def load_urls_from_tar_gz(self,path):
        with tarfile.open(path, "r:gz") as tar:
            for member in tar.getmembers():
                # Real all member from the file until the file is None
                url_file = tar.extractfile(member)
                if url_file is not None:
                    content  = url_file.read().decode('utf-8')
                    urls = content.strip().split('\n')
                    self.blocked_urls.update(urls)

    # Control that if the url is Block
    def is_url_blocked(self, url):
        return url in self.blocked_urls

# My main browser contains all GUI in this class (Toolbar, Buttons, URLbar)
class MyBrowser(QMainWindow):
    # Define the contructor for initialization 
    def __init__(self,config_data,my_config_data):
        super(MyBrowser,self).__init__()
        self.browser = QWebEngineView()
        self.setCentralWidget(self.browser)
        self.showMaximized()
        self.lang_translator = Translator()
        
        # Disable all native parameter for Tooltip to set my own type
        QApplication.setEffectEnabled(Qt.UI_FadeTooltip, False)
        QApplication.setEffectEnabled(Qt.UI_AnimateTooltip, False)
        
        # Define the Home Page for the Web Browser
        # !!! using .html but still don't have good Home Page
        html_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'homepage.html')
        self.browser.setUrl(QUrl.fromLocalFile(html_path))
        
        # Get parameter from file sconf/config.json
        font_info = config_data["font_info"]["font"]
        # Cut to get each value of font
        font_family_info, font_size_info, font_weight_info = font_info.split()
        color_info_menu = config_data["colors_info"]["menu_frame"]
        color_info_app = config_data["colors_info"]["app_frame"]
        color_info_button_unselected = config_data["colors_info"]["buttons_unselected"]
        color_info_button_selected = config_data["colors_info"]["buttons_selected"]
        button_value_padd_info = config_data["buttons_info"]["padx_value"]
        
        # Get my parametr from file myadditionalstyle.json
        buttons_width_info = my_config_data["sweb_buttons_add_info"]["sweb_button_width"]
        buttons_height_info = my_config_data["sweb_buttons_add_info"]["sweb_button_height"]
        self.buttons_icon_width_info = my_config_data["sweb_buttons_add_info"]["sweb_button_icon_width"]
        self.buttons_icon_height_info = my_config_data["sweb_buttons_add_info"]["sweb_button_icon_height"]
        buttons_space_width_info = my_config_data["sweb_buttons_add_info"]["sweb_button_space_width"]
        buttons_space_height_info = my_config_data["sweb_buttons_add_info"]["sweb_button_space_height"]
        border_radius_info = my_config_data["sweb_border_info"]["sweb_border_radius_info"]
        toolbar_bar_height_info = my_config_data["sweb_tool_bar_info"]["sweb_toolbar_height"]
        self.time_hover_button = my_config_data["hover_timer"]["time_to_play_sound"]
        self.path_to_image_https = my_config_data["image"]["sweb_image_https"]
        self.path_to_image_http = my_config_data["image"]["sweb_image_http"]

        # Function for URL bar
        self.browser.urlChanged.connect(self.update_url)
        self.browser.titleChanged.connect(self.update_title)
        
        # Create toolbar for saving URL
        self.url_toolbar = QToolBar("URL Navigation")
        self.addToolBar(self.url_toolbar)
        self.addToolBarBreak()
        
        # Create a toolbar for saving menu and buttons
        self.buttons_toolbar = QToolBar("Buttons Navigation")
        self.addToolBar(self.buttons_toolbar)
        
        # Set a style for button toolbar
        self.buttons_toolbar.setStyleSheet(f"""
             QToolBar {{
                background-color: {color_info_app};            
                spacing: {buttons_space_width_info}px;
                border-radius: {border_radius_info}px;
            }}
            
            /* Changes parameters for button in Toolbar*/
            QPushButton {{
                background-color: {color_info_button_unselected};            
                padding: {button_value_padd_info}px;        
                border-radius: {border_radius_info}px;
                font-size: {font_size_info}px;
                font-weight: {font_weight_info};
                font-family: {font_family_info};
                width: {buttons_width_info}px;
                height: {buttons_height_info}px;
                icon-size: {self.buttons_icon_width_info}px {self.buttons_icon_height_info}px;
            }}
            
            QPushButton:hover {{
                background-color: {color_info_button_selected}; 
            }}
            
            QPushButton QLabel {{
                font-size: {font_size_info}px;
                font-weight: {font_weight_info};
                font-family: {font_family_info};
            }}
            
            QMenu {{
                background-color: {color_info_menu};
                font-size: {font_size_info}px;
                font-weight: {font_weight_info};
                font-family: {font_family_info};
                width: 225px;
            }}
            QMenu::item {{
                height: {font_size_info}px;
            }}
            QMenu::item:selected {{
                background-color: {color_info_button_selected}
            }}
        """)
        
        # Add two spacer for let all button in the midde
        # Fist will be leaved in the beginning and the second will be leaved at the end
        first_spacer = QWidget()
        first_spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        second_spacer = QWidget()
        second_spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # Leave the first spacer in the beginning
        self.buttons_toolbar.addWidget(first_spacer)

        # Set fixed height for the button toolbar
        self.buttons_toolbar.setFixedHeight(toolbar_bar_height_info)
        # Set maximum height for the url toolbar
        self.url_toolbar.setMaximumHeight(toolbar_bar_height_info)
        
        # Get number of menu and number of options in the menu from sconf/config.json
        num_menu_buttons = config_data['buttons_info']['num_of_menu_buttons']
        num_of_opt_on_menu = config_data['buttons_info']['num_of_opt_on_frame']

        # Create an instance of CustomMenu with the specified number of menus and options per menu
        self.custom_menu = CustomMenu(self,num_menu_buttons, num_of_opt_on_menu)
        self.buttons_toolbar.addWidget(self.custom_menu)
        
        # Add Home button for come back to Home Page
        self.home_btn = QPushButton(self)
        # Create Home QvBoxLayout
        home_layout = QVBoxLayout(self.home_btn)
        # QStyle.SP_DirHomeIcon for Home Icon
        home_icon = self.style().standardIcon(QStyle.SP_DirHomeIcon)
        home_label = QLabel(self.home_btn)
        home_label.setPixmap(home_icon.pixmap(QSize(self.buttons_icon_width_info,self.buttons_icon_height_info)))
        home_layout.addWidget(home_label)
        self.home_text_label = QLabel("Home", self.home_btn)
        home_layout.addWidget(self.home_text_label)
        # Align text and icon in the center
        home_layout.setAlignment(home_label,Qt.AlignCenter)
        home_layout.setAlignment(self.home_text_label,Qt.AlignCenter)
        self.home_btn.clicked.connect(self.navigate_home)
        self.home_btn.setCursor(Qt.PointingHandCursor)
        self.buttons_toolbar.addWidget(self.home_btn)
        
        # Add blank space between two buttons
        spacer = QWidget()
        spacer.setFixedSize(buttons_space_width_info, buttons_space_height_info)
        self.buttons_toolbar.addWidget(spacer)
        
        # Add back button to go back to the previous page
        self.back_btn = QPushButton(self)
        back_layout = QVBoxLayout(self.back_btn)
        # QStyle.SP_ArrowBack to setting icon for back button
        back_icon = self.style().standardIcon(QStyle.SP_ArrowBack)
        back_label = QLabel(self.back_btn)
        back_label.setPixmap(back_icon.pixmap(QSize(self.buttons_icon_width_info,self.buttons_icon_height_info)))
        back_layout.addWidget(back_label)
        # Set text for back_btn
        self.back_text_label = QLabel("Back",self.back_btn)
        back_layout.addWidget(self.back_text_label)
        # Align text and icon in the center
        back_layout.setAlignment(back_label,Qt.AlignCenter)
        back_layout.setAlignment(self.back_text_label,Qt.AlignCenter)
        self.back_btn.clicked.connect(self.browser.back)
        self.back_btn.setCursor(Qt.PointingHandCursor) 
        self.buttons_toolbar.addWidget(self.back_btn)
        
        # Add a blank space between two buttons
        spacer = QWidget()
        spacer.setFixedSize(buttons_space_width_info, buttons_space_height_info)
        self.buttons_toolbar.addWidget(spacer)

        # Add Forward button with Icon
        self.forward_btn = QPushButton(self)
        forward_layout = QVBoxLayout(self.forward_btn)
        # QStyle.SP_ArrowForward for icon
        forward_icon = self.style().standardIcon(QStyle.SP_ArrowForward)
        forward_label = QLabel(self.forward_btn)
        forward_label.setPixmap(forward_icon.pixmap(QSize(self.buttons_icon_width_info,self.buttons_icon_height_info)))
        forward_layout.addWidget(forward_label)
        # Qlabel for text
        self.forward_text_label = QLabel("Forward",self.forward_btn)
        forward_layout.addWidget(self.forward_text_label)
        # Align icon and text in the center
        forward_layout.setAlignment(forward_label,Qt.AlignCenter)
        forward_layout.setAlignment(self.forward_text_label,Qt.AlignCenter)       
        self.forward_btn.clicked.connect(self.browser.forward)
        # Change the censor to Hand while hover
        self.forward_btn.setCursor(Qt.PointingHandCursor)
        self.buttons_toolbar.addWidget(self.forward_btn)
        
        # Add a blank space between two buttons
        spacer = QWidget()
        spacer.setFixedSize(buttons_space_width_info, buttons_space_height_info)
        self.buttons_toolbar.addWidget(spacer)
        
        # Add Reload button with icon
        self.reload_btn = QPushButton(self)
        reload_layout = QVBoxLayout(self.reload_btn)
        # SP_BrowserReload for Reload icon
        reload_icon = self.style().standardIcon(QStyle.SP_BrowserReload)
        reload_label = QLabel(self.reload_btn)
        reload_label.setPixmap(reload_icon.pixmap(QSize(self.buttons_icon_width_info,self.buttons_icon_height_info)))
        reload_layout.addWidget(reload_label)
        # Text fo reload button
        self.reload_text_label = QLabel("Reload",self.reload_btn)
        reload_layout.addWidget(self.reload_text_label)
        # Align text and icon in the center
        reload_layout.setAlignment(reload_label,Qt.AlignCenter)
        reload_layout.setAlignment(self.reload_text_label,Qt.AlignCenter)   
        self.reload_btn.clicked.connect(self.reload_and_go_to_top)
        self.reload_btn.setCursor(Qt.PointingHandCursor)
        self.buttons_toolbar.addWidget(self.reload_btn)
        
        # Add a blank space between two buttons
        spacer = QWidget()
        spacer.setFixedSize(buttons_space_width_info, buttons_space_height_info)
        self.buttons_toolbar.addWidget(spacer)
        
        # Add Reload button with icon
        self.translate_btn = QPushButton(self)
        translate_layout = QVBoxLayout(self.translate_btn)
        # SP_BrowserReload for Reload icon
        translate_icon = self.style().standardIcon(QStyle.SP_BrowserReload)
        translate_label = QLabel(self.translate_btn)
        translate_label.setPixmap(translate_icon.pixmap(QSize(self.buttons_icon_width_info,self.buttons_icon_height_info)))
        translate_layout.addWidget(translate_label)
        # Text fo reload button
        translate_text_label = QLabel("EN/CZ/DE",self.translate_btn)
        translate_layout.addWidget(translate_text_label)
        # Change to hand when click cursor
        self.translate_btn.setCursor(Qt.PointingHandCursor)
        # Align text and icon in the center
        translate_layout.setAlignment(translate_label,Qt.AlignCenter)
        translate_layout.setAlignment(translate_text_label,Qt.AlignCenter)
        self.translate_btn.clicked.connect(self.toggle_language)   
        self.buttons_toolbar.addWidget(self.translate_btn)
        
        # Add second space to last of toolbar for lay button in the center
        self.buttons_toolbar.addWidget(second_spacer)
   
        # Create a URL bar
        self.url_bar = QLineEdit()
        self.url_bar.setAlignment(Qt.AlignCenter)
        # Change the parameter of URL bar
        self.url_bar.setStyleSheet(f"""
        QLineEdit {{
            font-family: {font_family_info};
            font-size: {font_size_info}px;
            font-weight: {font_weight_info};
            border-radius: {border_radius_info}px;
            background-color: {color_info_app};         
        }}
        
        QLineEdit:hover {{
            padding: {button_value_padd_info}px;
        }}
        
        QLineEdit:focus {{
            padding: {button_value_padd_info}px;
        }}                 
        """)
        self.url_bar.setClearButtonEnabled(True)
        # Load URL blocker and logger
        filepaths = ["Phishing.Database-master/ALL-phishing-domains.tar.gz","Phishing.Database-master/ALL-phishing-links.tar.gz"]
        self.url_blocker = URLBlocker(filepaths)
        self.logger = URLLogger()
        # Navitigate URL when press enter
        # When text of URL is changed, check for URL Phishing
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        self.url_bar.textChanged.connect(self.check_url)
        # Update URL address to URL bar
        self.browser.urlChanged.connect(self.update_url)
        # Green when connect with https, red for connection with http
        self.url_bar.security_icon_action = self.url_bar.addAction(QIcon(),QLineEdit.TrailingPosition)
        self.url_toolbar.addWidget(self.url_bar)
        
        # Initially make URL toolbar visible
        # This method is used for Address option -> hide and show url bar
        self.url_toolbar.setVisible(False)

        # Configure audio and for hovering buttons, menus and options
        # Run this methods for the set Current language in Translator
        self.update_ui_text()
        self.update_ui_audio() 
    
    # Method for get current language and update default language in app
    # If translate button is clicked, change to other language and audio
    def toggle_language(self):
        self.lang_translator.toggle_language()
        self.update_ui_text()
        self.update_ui_audio()
    
    # Function for updating text on Browser when user clicked to button Translate
    # Default value is "en" -> "cz" -> "de"
    def update_ui_text(self):
        self.home_text_label.setText(self.lang_translator.get_text("homeButton"))
        self.back_text_label.setText(self.lang_translator.get_text("backButton"))
        self.forward_text_label.setText(self.lang_translator.get_text("forwardButton"))
        self.reload_text_label.setText(self.lang_translator.get_text("reloadButton"))
        self.custom_menu.menu1_news_text_label.setText(self.lang_translator.get_text("menu1"))
        self.custom_menu.menu2_news_text_label.setText(self.lang_translator.get_text("menu2"))
        self.custom_menu.menu1_exit.setText(self.lang_translator.get_text("menu1Exit"))
        self.custom_menu.menu1_www1.setText(self.lang_translator.get_text("menu1WWW1"))
        self.custom_menu.menu1_www2.setText(self.lang_translator.get_text("menu1WWW2"))
        self.custom_menu.menu1_www3.setText(self.lang_translator.get_text("menu1WWW3"))
        self.custom_menu.menu2_www4.setText(self.lang_translator.get_text("menu2WWW4"))
        self.custom_menu.menu2_www5.setText(self.lang_translator.get_text("menu2WWW5"))
        self.custom_menu.menu2_www6.setText(self.lang_translator.get_text("menu2WWW6"))
        self.custom_menu.menu2_address.setText(self.lang_translator.get_text("menu2Address"))

    # Function for updating audio on Browser when user clicked to button Translate
    # Default value is "en" -> "cz" -> "de"
    def update_ui_audio(self):
        self.setup_hover_sound(self.home_btn,self.time_hover_button,self.lang_translator.get_audio("homeButton"))
        self.setup_hover_sound(self.back_btn,self.time_hover_button,self.lang_translator.get_audio("backButton"))
        self.setup_hover_sound(self.forward_btn,self.time_hover_button,self.lang_translator.get_audio("forwardButton"))
        self.setup_hover_sound(self.reload_btn,self.time_hover_button,self.lang_translator.get_audio("reloadButton"))
        self.setup_hover_sound(self.translate_btn,self.time_hover_button,self.lang_translator.get_audio("translateButton"))
        self.setup_hover_sound(self.custom_menu.menu1_button,self.time_hover_button,self.lang_translator.get_audio("menu1"))
        self.setup_hover_sound(self.custom_menu.menu2_button,self.time_hover_button,self.lang_translator.get_audio("menu2"))
        # Options
        #self.custom_menu.options_menu_hover(self.custom_menu.menu1_exit,self.time_hover_button,self.lang_translator.get_audio("Audio"))
        #self.custom_menu.options_menu_hover(self.custom_menu.menu1_www1,self.time_hover_button,self.lang_translator.get_audio("Audio1"))
        #self.custom_menu.options_menu_hover(self.custom_menu.menu1_www2,self.time_hover_button,self.lang_translator.get_audio("Audio2"))
        #self.custom_menu.options_menu_hover(self.custom_menu.menu1_www3,self.time_hover_button,self.lang_translator.get_audio("Audio3"))
        #self.custom_menu.menu1_exit.hovered.connect(self.on_menu_hover(self.lang_translator.get_audio("menu1Exit")))
        #self.setup_hover_sound(self.custom_menu.menu1_www1,self.time_hover_button,self.lang_translator.get_audio("menu1WWW1"))
        #self.setup_hover_sound(self.custom_menu.menu1_www2,self.time_hover_button,self.lang_translator.get_audio("menu1WWW2"))
        #self.setup_hover_sound(self.custom_menu.menu1_www3,self.time_hover_button,self.lang_translator.get_audio("menu1WWW3"))
        #self.setup_hover_sound(self.custom_menu.menu2_www4,self.time_hover_button,self.lang_translator.get_audio("menu2WWW4"))
        #self.setup_hover_sound(self.custom_menu.menu2_www5,self.time_hover_button,self.lang_translator.get_audio("menu2WWW5"))
        #self.setup_hover_sound(self.custom_menu.menu2_www6,self.time_hover_button,self.lang_translator.get_audio("menu2WWW6"))
        #self.setup_hover_sound(self.custom_menu.menu1_exit,self.time_hover_button,self.lang_translator.get_audio("menu2Address"))

    # QpushButton can be set HoverLeave and HoverEnter event with "widget"
    def setup_hover_sound(self, widget, hover_time,path_to_sound):
        # Using Qtimer to set clock
        widget.hover_timer = QTimer()
        widget.hover_timer.setInterval(hover_time)
        # Run only one times when hover
        widget.hover_timer.setSingleShot(True)
        widget.hover_timer.timeout.connect(lambda: self.play_sound(path_to_sound))
        # Install event to widget -> Event is comefrom eventFilter
        widget.installEventFilter(self)
    
    # Set event for leave and enter button -> Using only with QpushButton
    def eventFilter(self, watched, event):
        if event.type() == QEvent.HoverEnter:
            watched.hover_timer.start()
        elif event.type() == QEvent.HoverLeave:
            watched.hover_timer.stop()
        return super().eventFilter(watched, event)
    
    # Play a sound, which is stored on SWEB_config.json
    def play_sound(self, path_to_sound):
        # Ensure the file exists before trying to play it.
        if os.path.exists(path_to_sound):
            if path_to_sound.endswith('.wav'):
                subprocess.run(["aplay", path_to_sound])
            elif path_to_sound.endswith('.mp3'):
                subprocess.run(["mpg123", path_to_sound])
        else:
            print(f"Sound file not found in: {path_to_sound}")

    # This method is set for visible and invisible URL bar
    def toggle_url_toolbar(self):
        # Toggle visibility of the URL toolbar
        self.url_toolbar.setVisible(not self.url_toolbar.isVisible())

    # This method is used for navigation URL bar
    def navigate_to_url(self):
        # Get url from URL toobal
        url_in_bar = self.url_bar.text().strip()
        # Check that if URL is from URL
        if self.url_blocker.is_url_blocked(url_in_bar):
            self.show_blocked_message(url_in_bar)
            self.logger.log_blocked_url(url_in_bar,'BROWSER', 'LOG_EMERG', 'CONN', 'Phishing connection refused')
            return
        # If "." is not contained in URL
        if "." not in url_in_bar:
            url_in_bar = "https://www.google.com/search?q=" + url_in_bar
        else:
            # Top Level Domain is not available
            if not any(url_in_bar.endswith(tld) for tld in [".com", ".org", ".net", ".gor", ".cz"]):
                url_in_bar = "https://www.google.com/search?q=" + url_in_bar
        # If in URl not http or https, connect with HTTPS
        if "://" not in url_in_bar:
            url_in_bar = "https://" + url_in_bar

        self.browser.setUrl(QUrl(url_in_bar))
    
    # This method is first security in Browser
    # Check if connection is under HTTP or HTTPS
    def check_url(self,url):
        if url.startswith("https://"):
            self.url_bar.security_icon_action.setIcon(QIcon(self.path_to_image_https))
        else:
            self.url_bar.security_icon_action.setIcon(QIcon(self.path_to_image_http))
            
    # Method for running home page - Add to event of Home Button
    def navigate_home(self):
        html_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'homepage.html')
        self.browser.setUrl(QUrl.fromLocalFile(html_path))
        
    # Show block message when User connect to web from Phishing list
    def show_blocked_message(self, url):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setText(f"Blocked Phishing URL: {url}")
        msg.setWindowTitle("Blocked URL Warning")
        msg.exec_()

    # Method for updating URL
    def update_url(self, inputURL):
        # Change text in url Bar
        self.url_bar.setText(inputURL.toString())
        self.url_bar.setCursorPosition(0)
        
    # Method for updating title
    def update_title(self):
        title = self.browser.page().title()
        self.setWindowTitle(title)
    
    # Method for reload page in browser
    def reload_and_go_to_top(self):
        self.browser.reload()
    
    # Method for connect to the first www1 seznam.cz
    def navigate_www1(self):
        self.browser.setUrl(QUrl("https://seznam.cz"))
        
    # Method for connect to the second www2 ct24.ceskatelevize.cz
    def navigate_www2(self):
        self.browser.setUrl(QUrl("https://ct24.ceskatelevize.cz"))
        
    # Method for connect to the third irozhlas.cz
    def navigate_www3(self):
        self.browser.setUrl(QUrl("https://irozhlas.cz"))

    # Method for connect to the fourth idnes.cz
    def navigate_www4(self):
        self.browser.setUrl(QUrl("https://www.idnes.cz"))

    # Method for connect to the fifth aktualne.cz
    def navigate_www5(self):
        self.browser.setUrl(QUrl("https://www.aktualne.cz"))

    # Method for connect to the sixth denik.cz
    def navigate_www6(self):
        self.browser.setUrl(QUrl("https://www.denik.cz"))
    
# Definuje funkci Main
if __name__ == "__main__":
    qApplication = QApplication(sys.argv)
    qApplication.setApplicationName("Web Browser for senior")
    sweb_config = load_sweb_config_json()
    # Nastavit styl pro vsechny ToolTip (Vymenit styl jako CSS)
    qApplication.setStyleSheet("""
    """)
    # Load config data from JSON file
    config = load_config_json()
    mainWindow = MyBrowser(config,sweb_config)
    mainWindow.show()
    sys.exit(qApplication.exec_())
