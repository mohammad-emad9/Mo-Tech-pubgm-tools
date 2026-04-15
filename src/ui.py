# -*- coding: utf-8 -*-
# QFont\(\)\s+font\d+\.setFamily\(u"Agency FB"\)  to QFont(font_family)


from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from . import resource_path
from .ui_images import resources_rc


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1310, 739)
        MainWindow.setMinimumSize(QSize(1310, 739))
        MainWindow.setMaximumSize(QSize(1310, 739))
        font_id = QFontDatabase.addApplicationFont(resource_path(r"assets\fonts\AGENCYR.TTF"))
        font_families = QFontDatabase.applicationFontFamilies(font_id)
        font_family = font_families[0] if font_families else "Segoe UI"
        font = QFont(font_family)
        font.setBold(True)
        font.setWeight(75)
        MainWindow.setFont(font)
        icon = QIcon()
        icon.addFile(resource_path(r"assets\icons\logo.ico"), QSize(), QIcon.Normal, QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setStyleSheet("")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.appbackground = QLabel(self.centralwidget)
        self.appbackground.setObjectName(u"appbackground")
        self.appbackground.setEnabled(True)
        self.appbackground.setGeometry(QRect(0, 0, 1311, 741))
        self.appbackground.setStyleSheet(u"border-image: url(:/Graphics/bg.png);")
        self.stackedWidget = QStackedWidget(self.centralwidget)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.stackedWidget.setGeometry(QRect(29, 80, 1081, 651))
        self.stackedWidget.setStyleSheet(u"QStackedWidget { background-color: #f5f5f5; }")
        self.gfx_page = QWidget()
        self.gfx_page.setObjectName(u"gfx_page")
        self.gfx_page_background = QLabel(self.gfx_page)
        self.gfx_page_background.setObjectName(u"gfx_page_background")
        self.gfx_page_background.setEnabled(True)
        self.gfx_page_background.setGeometry(QRect(-30, -80, 1311, 741))
        self.gfx_page_background.setStyleSheet(u"border-image: url(:/Graphics/bg.png);")
        self.submit_gfx_btn = QPushButton(self.gfx_page)
        self.submit_gfx_btn.setObjectName(u"submit_gfx_btn")
        self.submit_gfx_btn.setGeometry(QRect(910, 580, 150, 55))
        font1 = QFont(font_family)
        font1.setPointSize(20)
        font1.setBold(True)
        font1.setItalic(False)
        font1.setUnderline(False)
        font1.setWeight(75)
        self.submit_gfx_btn.setFont(font1)
        font2 = QFont(font_family)
        font2.setPointSize(18)
        font2.setBold(True)
        font2.setWeight(75)
        self.submit_gfx_btn.setStyleSheet(u"QPushButton {\n"
                                          "                                background-color: #f7d620;\n"
                                          "                                border: 1px solid black;\n"
                                          "                                border-radius: 10px;\n"
                                          "                                color: rgb(0, 0, 0);\n"
                                          "                                font-weight: bold;\n"
                                          "                                }\n"
                                          "                                QPushButton:hover {\n"
                                          "                                background-color: #ffeb3b;\n"
                                          "                                }\n"
                                          "                                QPushButton:pressed {\n"
                                          "                                background-color: #cddc39;\n"
                                          "                                }\n"
                                          "                            ")
        self.connect_gameloop_btn = QPushButton(self.gfx_page)
        self.connect_gameloop_btn.setObjectName(u"connect_gameloop_btn")
        self.connect_gameloop_btn.setEnabled(True)
        self.connect_gameloop_btn.setGeometry(QRect(590, 580, 311, 55))
        self.connect_gameloop_btn.setFont(font2)
        self.connect_gameloop_btn.setStyleSheet(u"QPushButton {\n"
                                                "                                background-color: rgba(49, 50, 68, 120);\n"
                                                "                                border: 2px solid #45475a;\n"
                                                "                                border-radius: 10px;\n"
                                                "                                color: #969696;\n"
                                                "                                }\n"
                                                "                                QPushButton:hover {\n"
                                                "                                border: 2px solid #f7d620;\n"
                                                "                                color: white;\n"
                                                "                                background-color: rgba(247, 214, 32, 30);\n"
                                                "                                }\n"
                                                "                                QPushButton:checked {\n"
                                                "                                background-color: rgba(247, 214, 32, 60);\n"
                                                "                                color: #f7d620;\n"
                                                "                                border: 2px solid #f7d620;\n"
                                                "                                font-weight: bold;\n"
                                                "                                }\n"
                                                "                                QPushButton:disabled {\n"
                                                "                                color: #4d4d4d;\n"
                                                "                                }\n"
                                                "                            ")
        self.connect_gameloop_btn.setCheckable(True)
        self.PubgchooseFrame = QFrame(self.gfx_page)
        self.PubgchooseFrame.setObjectName(u"PubgchooseFrame")
        self.PubgchooseFrame.setGeometry(QRect(20, 575, 261, 90))
        self.PubgchooseFrame.setFrameShape(QFrame.NoFrame)
        self.pubgchoose_btn = QPushButton(self.PubgchooseFrame)
        self.pubgchoose_btn.setObjectName(u"pubgchoose_btn")
        self.pubgchoose_btn.setGeometry(QRect(180, 10, 71, 51))
        sizePolicy = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pubgchoose_btn.sizePolicy().hasHeightForWidth())
        self.pubgchoose_btn.setSizePolicy(sizePolicy)
        font3 = QFont(font_family)
        font3.setPointSize(20)
        font3.setBold(True)
        font3.setWeight(75)
        font3.setStyleStrategy(QFont.PreferAntialias)
        self.pubgchoose_btn.setFont(font3)
        self.pubgchoose_btn.setStyleSheet(u"")
        self.pubgchoose_btn.setFlat(True)
        self.pubgchoose_dropdown = QComboBox(self.PubgchooseFrame)
        self.pubgchoose_dropdown.setObjectName(u"pubgchoose_dropdown")
        self.pubgchoose_dropdown.setGeometry(QRect(0, 10, 171, 51))
        font4 = QFont(font_family)
        font4.setPointSize(13)
        font4.setBold(True)
        font4.setWeight(75)
        self.pubgchoose_dropdown.setFont(font4)
        self.pubgchoose_dropdown.setStyleSheet(u"")
        self.pubgchoose_label = QLabel(self.PubgchooseFrame)
        self.pubgchoose_label.setObjectName(u"pubgchoose_label")
        self.pubgchoose_label.setGeometry(QRect(0, 59, 251, 21))
        font5 = QFont(font_family)
        font5.setPointSize(10)
        font5.setBold(True)
        font5.setWeight(75)
        self.pubgchoose_label.setFont(font5)
        self.pubgchoose_label.setStyleSheet(u"color: #f7d620;\n"
                                            "                                    font-weight: bold;\n"
                                            "                                ")
        self.frame = QFrame(self.gfx_page)
        self.frame.setObjectName(u"frame")
        self.frame.setGeometry(QRect(0, 0, 1081, 581))
        self.frame.setMinimumSize(QSize(1081, 581))
        self.frame.setMaximumSize(QSize(1081, 581))
        self.frame.setFrameShape(QFrame.NoFrame)
        self.gridLayout = QGridLayout(self.frame)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.GraphicsFrame = QFrame(self.frame)
        self.GraphicsFrame.setObjectName(u"GraphicsFrame")
        self.GraphicsFrame.setMinimumSize(QSize(1, 1))
        self.GraphicsFrame.setMaximumSize(QSize(99999, 999999))
        self.GraphicsFrame.setStyleSheet(u"")
        self.graphics_label = QLabel(self.GraphicsFrame)
        self.graphics_label.setObjectName(u"graphics_label")
        self.graphics_label.setGeometry(QRect(11, 0, 136, 37))
        font6 = QFont(font_family)
        font6.setPointSize(23)
        font6.setBold(True)
        font6.setWeight(75)
        self.graphics_label.setFont(font6)
        self.graphics_label.setStyleSheet(u"\n"
                                          "\n"
                                          "                                    color: #fff;\n"
                                          "                                ")
        self.layoutWidget = QWidget(self.GraphicsFrame)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(11, 50, 1050, 50))
        self.GraphicsLayout = QHBoxLayout(self.layoutWidget)
        self.GraphicsLayout.setSpacing(10)
        self.GraphicsLayout.setObjectName(u"GraphicsLayout")
        self.GraphicsLayout.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.GraphicsLayout.setContentsMargins(5, 5, 5, 5)
        self.supersmooth_graphics_btn = QPushButton(self.layoutWidget)
        self.supersmooth_graphics_btn.setObjectName(u"supersmooth_graphics_btn")
        sizePolicy.setHeightForWidth(self.supersmooth_graphics_btn.sizePolicy().hasHeightForWidth())
        self.supersmooth_graphics_btn.setSizePolicy(sizePolicy)
        self.supersmooth_graphics_btn.setMinimumSize(QSize(140, 45))
        self.supersmooth_graphics_btn.setMaximumSize(QSize(140, 45))
        self.supersmooth_graphics_btn.setFont(font3)
        self.supersmooth_graphics_btn.setStyleSheet(u"")
        self.supersmooth_graphics_btn.setCheckable(True)
        self.supersmooth_graphics_btn.setFlat(True)

        self.GraphicsLayout.addWidget(self.supersmooth_graphics_btn)

        self.smooth_graphics_btn = QPushButton(self.layoutWidget)
        self.smooth_graphics_btn.setObjectName(u"smooth_graphics_btn")
        sizePolicy.setHeightForWidth(self.smooth_graphics_btn.sizePolicy().hasHeightForWidth())
        self.smooth_graphics_btn.setSizePolicy(sizePolicy)
        self.smooth_graphics_btn.setMinimumSize(QSize(140, 45))
        self.smooth_graphics_btn.setMaximumSize(QSize(140, 45))
        self.smooth_graphics_btn.setFont(font3)
        self.smooth_graphics_btn.setStyleSheet(u"")
        self.smooth_graphics_btn.setCheckable(True)
        self.smooth_graphics_btn.setFlat(True)

        self.GraphicsLayout.addWidget(self.smooth_graphics_btn)

        self.balanced_graphics_btn = QPushButton(self.layoutWidget)
        self.balanced_graphics_btn.setObjectName(u"balanced_graphics_btn")
        sizePolicy.setHeightForWidth(self.balanced_graphics_btn.sizePolicy().hasHeightForWidth())
        self.balanced_graphics_btn.setSizePolicy(sizePolicy)
        self.balanced_graphics_btn.setMinimumSize(QSize(140, 45))
        self.balanced_graphics_btn.setMaximumSize(QSize(140, 45))
        self.balanced_graphics_btn.setFont(font3)
        self.balanced_graphics_btn.setStyleSheet(u"")
        self.balanced_graphics_btn.setCheckable(True)
        self.balanced_graphics_btn.setFlat(True)

        self.GraphicsLayout.addWidget(self.balanced_graphics_btn)

        self.hd_graphics_btn = QPushButton(self.layoutWidget)
        self.hd_graphics_btn.setObjectName(u"hd_graphics_btn")
        sizePolicy.setHeightForWidth(self.hd_graphics_btn.sizePolicy().hasHeightForWidth())
        self.hd_graphics_btn.setSizePolicy(sizePolicy)
        self.hd_graphics_btn.setMinimumSize(QSize(140, 45))
        self.hd_graphics_btn.setMaximumSize(QSize(140, 45))
        self.hd_graphics_btn.setFont(font3)
        self.hd_graphics_btn.setStyleSheet(u"")
        self.hd_graphics_btn.setCheckable(True)
        self.hd_graphics_btn.setFlat(True)

        self.GraphicsLayout.addWidget(self.hd_graphics_btn)

        self.hdr_graphics_btn = QPushButton(self.layoutWidget)
        self.hdr_graphics_btn.setObjectName(u"hdr_graphics_btn")
        sizePolicy.setHeightForWidth(self.hdr_graphics_btn.sizePolicy().hasHeightForWidth())
        self.hdr_graphics_btn.setSizePolicy(sizePolicy)
        self.hdr_graphics_btn.setMinimumSize(QSize(140, 45))
        self.hdr_graphics_btn.setMaximumSize(QSize(140, 45))
        self.hdr_graphics_btn.setFont(font3)
        self.hdr_graphics_btn.setStyleSheet(u"")
        self.hdr_graphics_btn.setCheckable(True)
        self.hdr_graphics_btn.setFlat(True)

        self.GraphicsLayout.addWidget(self.hdr_graphics_btn)

        self.ultrahd_graphics_btn = QPushButton(self.layoutWidget)
        self.ultrahd_graphics_btn.setObjectName(u"ultrahd_graphics_btn")
        sizePolicy.setHeightForWidth(self.ultrahd_graphics_btn.sizePolicy().hasHeightForWidth())
        self.ultrahd_graphics_btn.setSizePolicy(sizePolicy)
        self.ultrahd_graphics_btn.setMinimumSize(QSize(140, 45))
        self.ultrahd_graphics_btn.setMaximumSize(QSize(140, 45))
        self.ultrahd_graphics_btn.setFont(font3)
        self.ultrahd_graphics_btn.setStyleSheet(u"")
        self.ultrahd_graphics_btn.setCheckable(True)
        self.ultrahd_graphics_btn.setFlat(True)

        self.GraphicsLayout.addWidget(self.ultrahd_graphics_btn)

        self.uhd_graphics_btn = QPushButton(self.layoutWidget)
        self.uhd_graphics_btn.setObjectName(u"uhd_graphics_btn")
        sizePolicy.setHeightForWidth(self.uhd_graphics_btn.sizePolicy().hasHeightForWidth())
        self.uhd_graphics_btn.setSizePolicy(sizePolicy)
        self.uhd_graphics_btn.setMinimumSize(QSize(140, 45))
        self.uhd_graphics_btn.setMaximumSize(QSize(140, 45))
        self.uhd_graphics_btn.setFont(font3)
        self.uhd_graphics_btn.setStyleSheet(u"")
        self.uhd_graphics_btn.setCheckable(True)
        self.uhd_graphics_btn.setFlat(True)

        self.GraphicsLayout.addWidget(self.uhd_graphics_btn)

        self.gridLayout.addWidget(self.GraphicsFrame, 0, 0, 1, 2)

        self.FramerateFrame = QFrame(self.frame)
        self.FramerateFrame.setObjectName(u"FramerateFrame")
        self.FramerateFrame.setMinimumSize(QSize(821, 117))
        self.FramerateFrame.setMaximumSize(QSize(9999, 9999))
        self.FramerateFrame.setStyleSheet(u"")
        self.fps_label = QLabel(self.FramerateFrame)
        self.fps_label.setObjectName(u"fps_label")
        self.fps_label.setGeometry(QRect(10, 10, 180, 37))
        self.fps_label.setFont(font6)
        self.fps_label.setStyleSheet(u"color: #ffffff;")
        self.layoutWidget1 = QWidget(self.FramerateFrame)
        self.layoutWidget1.setObjectName(u"layoutWidget1")
        self.layoutWidget1.setGeometry(QRect(10, 61, 1070, 50))
        self.FramerateLayout = QHBoxLayout(self.layoutWidget1)
        self.FramerateLayout.setSpacing(10)
        self.FramerateLayout.setObjectName(u"FramerateLayout")
        self.FramerateLayout.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.FramerateLayout.setContentsMargins(5, 5, 5, 5)
        self.low_fps_btn = QPushButton(self.layoutWidget1)
        self.low_fps_btn.setObjectName(u"low_fps_btn")
        sizePolicy.setHeightForWidth(self.low_fps_btn.sizePolicy().hasHeightForWidth())
        self.low_fps_btn.setSizePolicy(sizePolicy)
        self.low_fps_btn.setMinimumSize(QSize(125, 45))
        self.low_fps_btn.setMaximumSize(QSize(125, 45))
        self.low_fps_btn.setFont(font3)
        self.low_fps_btn.setStyleSheet(u"")
        self.low_fps_btn.setCheckable(True)
        self.low_fps_btn.setFlat(True)

        self.FramerateLayout.addWidget(self.low_fps_btn)

        self.medium_fps_btn = QPushButton(self.layoutWidget1)
        self.medium_fps_btn.setObjectName(u"medium_fps_btn")
        sizePolicy.setHeightForWidth(self.medium_fps_btn.sizePolicy().hasHeightForWidth())
        self.medium_fps_btn.setSizePolicy(sizePolicy)
        self.medium_fps_btn.setMinimumSize(QSize(145, 45))
        self.medium_fps_btn.setMaximumSize(QSize(145, 45))
        self.medium_fps_btn.setFont(font3)
        self.medium_fps_btn.setStyleSheet(u"")
        self.medium_fps_btn.setCheckable(True)
        self.medium_fps_btn.setFlat(True)

        self.FramerateLayout.addWidget(self.medium_fps_btn)

        self.high_fps_btn = QPushButton(self.layoutWidget1)
        self.high_fps_btn.setObjectName(u"high_fps_btn")
        sizePolicy.setHeightForWidth(self.high_fps_btn.sizePolicy().hasHeightForWidth())
        self.high_fps_btn.setSizePolicy(sizePolicy)
        self.high_fps_btn.setMinimumSize(QSize(125, 45))
        self.high_fps_btn.setMaximumSize(QSize(125, 45))
        self.high_fps_btn.setFont(font3)
        self.high_fps_btn.setStyleSheet(u"")
        self.high_fps_btn.setCheckable(True)
        self.high_fps_btn.setFlat(True)

        self.FramerateLayout.addWidget(self.high_fps_btn)

        self.ultra_fps_btn = QPushButton(self.layoutWidget1)
        self.ultra_fps_btn.setObjectName(u"ultra_fps_btn")
        sizePolicy.setHeightForWidth(self.ultra_fps_btn.sizePolicy().hasHeightForWidth())
        self.ultra_fps_btn.setSizePolicy(sizePolicy)
        self.ultra_fps_btn.setMinimumSize(QSize(125, 45))
        self.ultra_fps_btn.setMaximumSize(QSize(125, 45))
        self.ultra_fps_btn.setFont(font3)
        self.ultra_fps_btn.setStyleSheet(u"")
        self.ultra_fps_btn.setCheckable(True)
        self.ultra_fps_btn.setFlat(True)

        self.FramerateLayout.addWidget(self.ultra_fps_btn)

        self.extreme_fps_btn = QPushButton(self.layoutWidget1)
        self.extreme_fps_btn.setObjectName(u"extreme_fps_btn")
        sizePolicy.setHeightForWidth(self.extreme_fps_btn.sizePolicy().hasHeightForWidth())
        self.extreme_fps_btn.setSizePolicy(sizePolicy)
        self.extreme_fps_btn.setMinimumSize(QSize(145, 45))
        self.extreme_fps_btn.setMaximumSize(QSize(145, 45))
        self.extreme_fps_btn.setFont(font3)
        self.extreme_fps_btn.setStyleSheet(u"")
        self.extreme_fps_btn.setCheckable(True)
        self.extreme_fps_btn.setFlat(True)

        self.FramerateLayout.addWidget(self.extreme_fps_btn)

        self.fps90_fps_btn = QPushButton(self.layoutWidget1)
        self.fps90_fps_btn.setObjectName(u"fps90_fps_btn")
        sizePolicy.setHeightForWidth(self.fps90_fps_btn.sizePolicy().hasHeightForWidth())
        self.fps90_fps_btn.setSizePolicy(sizePolicy)
        self.fps90_fps_btn.setMinimumSize(QSize(155, 45))
        self.fps90_fps_btn.setMaximumSize(QSize(155, 45))
        self.fps90_fps_btn.setFont(font3)
        self.fps90_fps_btn.setStyleSheet(u"")
        self.fps90_fps_btn.setCheckable(True)
        self.fps90_fps_btn.setFlat(True)

        self.FramerateLayout.addWidget(self.fps90_fps_btn)

        self.fps120_fps_btn = QPushButton(self.layoutWidget1)
        self.fps120_fps_btn.setObjectName(u"fps120_fps_btn")
        sizePolicy.setHeightForWidth(self.fps120_fps_btn.sizePolicy().hasHeightForWidth())
        self.fps120_fps_btn.setSizePolicy(sizePolicy)
        self.fps120_fps_btn.setMinimumSize(QSize(205, 45))
        self.fps120_fps_btn.setMaximumSize(QSize(205, 45))
        self.fps120_fps_btn.setFont(font3)
        self.fps120_fps_btn.setStyleSheet(u"")
        self.fps120_fps_btn.setCheckable(True)
        self.fps120_fps_btn.setFlat(True)

        self.FramerateLayout.addWidget(self.fps120_fps_btn)

        self.gridLayout.addWidget(self.FramerateFrame, 1, 0, 1, 2)

        self.StyleFrame = QFrame(self.frame)
        self.StyleFrame.setObjectName(u"StyleFrame")
        self.StyleFrame.setEnabled(True)
        self.StyleFrame.setMinimumSize(QSize(820, 231))
        self.StyleFrame.setMaximumSize(QSize(9999, 9999))
        self.StyleFrame.setStyleSheet(u"QPushButton {\n"
                                      "                                border: none;\n"
                                      "                                border-image: none;\n"
                                      "                                background: transparent;\n"
                                      "                                icon-size: 100%;\n"
                                      "                                qproperty-iconSize: 150px; /* set the size of the button icon */\n"
                                      "                                qproperty-text: \"\"; /* set the text displayed on the button */\n"
                                      "                                qproperty-flat: true; /* remove the default button border */\n"
                                      "                                padding: 0; /* remove any padding */\n"
                                      "                                }\n"
                                      "\n"
                                      "                                QPushButton:checked {\n"
                                      "                                border-width: 5px; /* set the width of the border */\n"
                                      "                                border-image: url(:/Graphics/checked.png);\n"
                                      "                                }\n"
                                      "                            ")
        self.style_label = QLabel(self.StyleFrame)
        self.style_label.setObjectName(u"style_label")
        self.style_label.setGeometry(QRect(10, 10, 78, 37))
        self.style_label.setFont(font6)
        self.style_label.setStyleSheet(u"color: #ffffff;")
        self.layoutWidget2 = QWidget(self.StyleFrame)
        self.layoutWidget2.setObjectName(u"layoutWidget2")
        self.layoutWidget2.setGeometry(QRect(10, 60, 851, 167))
        self.StyleLayout = QHBoxLayout(self.layoutWidget2)
        self.StyleLayout.setObjectName(u"StyleLayout")
        self.StyleLayout.setContentsMargins(0, 0, 0, 0)
        self.classic_style_btn = QPushButton(self.layoutWidget2)
        self.classic_style_btn.setObjectName(u"classic_style_btn")
        sizePolicy.setHeightForWidth(self.classic_style_btn.sizePolicy().hasHeightForWidth())
        self.classic_style_btn.setSizePolicy(sizePolicy)
        self.classic_style_btn.setMinimumSize(QSize(165, 165))
        self.classic_style_btn.setMaximumSize(QSize(165, 165))
        self.classic_style_btn.setStyleSheet(u"QPushButton {\n"
                                             "                                                qproperty-icon: url(:/Graphics/Classic.png); /* set the button icon */\n"
                                             "                                                }\n"
                                             "                                            ")
        self.classic_style_btn.setCheckable(True)

        self.StyleLayout.addWidget(self.classic_style_btn)

        self.colorful_style_btn = QPushButton(self.layoutWidget2)
        self.colorful_style_btn.setObjectName(u"colorful_style_btn")
        sizePolicy.setHeightForWidth(self.colorful_style_btn.sizePolicy().hasHeightForWidth())
        self.colorful_style_btn.setSizePolicy(sizePolicy)
        self.colorful_style_btn.setMinimumSize(QSize(165, 165))
        self.colorful_style_btn.setMaximumSize(QSize(165, 165))
        self.colorful_style_btn.setStyleSheet(u"QPushButton {\n"
                                              "                                                qproperty-icon: url(:/Graphics/Colorful.png); /* set the button icon */\n"
                                              "                                                }\n"
                                              "\n"
                                              "                                            ")
        self.colorful_style_btn.setCheckable(True)

        self.StyleLayout.addWidget(self.colorful_style_btn)

        self.realistic_style_btn = QPushButton(self.layoutWidget2)
        self.realistic_style_btn.setObjectName(u"realistic_style_btn")
        sizePolicy.setHeightForWidth(self.realistic_style_btn.sizePolicy().hasHeightForWidth())
        self.realistic_style_btn.setSizePolicy(sizePolicy)
        self.realistic_style_btn.setMinimumSize(QSize(165, 165))
        self.realistic_style_btn.setMaximumSize(QSize(165, 165))
        self.realistic_style_btn.setStyleSheet(u"QPushButton {\n"
                                               "                                                qproperty-icon: url(:/Graphics/Realistic.png); /* set the button icon */\n"
                                               "                                                }\n"
                                               "\n"
                                               "                                            ")
        self.realistic_style_btn.setCheckable(True)

        self.StyleLayout.addWidget(self.realistic_style_btn)

        self.soft_style_btn = QPushButton(self.layoutWidget2)
        self.soft_style_btn.setObjectName(u"soft_style_btn")
        sizePolicy.setHeightForWidth(self.soft_style_btn.sizePolicy().hasHeightForWidth())
        self.soft_style_btn.setSizePolicy(sizePolicy)
        self.soft_style_btn.setMinimumSize(QSize(165, 165))
        self.soft_style_btn.setMaximumSize(QSize(165, 165))
        self.soft_style_btn.setStyleSheet(u"QPushButton {\n"
                                          "                                                qproperty-icon: url(:/Graphics/Soft.png); /* set the button icon */\n"
                                          "                                                }\n"
                                          "                                            ")
        self.soft_style_btn.setCheckable(True)

        self.StyleLayout.addWidget(self.soft_style_btn)

        self.movie_style_btn = QPushButton(self.layoutWidget2)
        self.movie_style_btn.setObjectName(u"movie_style_btn")
        sizePolicy.setHeightForWidth(self.movie_style_btn.sizePolicy().hasHeightForWidth())
        self.movie_style_btn.setSizePolicy(sizePolicy)
        self.movie_style_btn.setMinimumSize(QSize(165, 165))
        self.movie_style_btn.setMaximumSize(QSize(165, 165))
        self.movie_style_btn.setStyleSheet(u"QPushButton {\n"
                                           "                                                qproperty-icon: url(:/Graphics/Movie.png); /* set the button icon */\n"
                                           "                                                }\n"
                                           "                                            ")
        self.movie_style_btn.setCheckable(True)

        self.StyleLayout.addWidget(self.movie_style_btn)

        self.gridLayout.addWidget(self.StyleFrame, 2, 0, 1, 2)

        self.ShadowFrame = QFrame(self.frame)
        self.ShadowFrame.setObjectName(u"ShadowFrame")
        self.ShadowFrame.setMinimumSize(QSize(1, 1))
        self.ShadowFrame.setMaximumSize(QSize(9999, 9999))
        self.ShadowFrame.setStyleSheet(u"")
        self.shadow_label = QLabel(self.ShadowFrame)
        self.shadow_label.setObjectName(u"shadow_label")
        self.shadow_label.setGeometry(QRect(10, 10, 126, 37))
        self.shadow_label.setFont(font6)
        self.shadow_label.setStyleSheet(u"color: #ffffff;")
        self.layoutWidget_2 = QWidget(self.ShadowFrame)
        self.layoutWidget_2.setObjectName(u"layoutWidget_2")
        self.layoutWidget_2.setGeometry(QRect(10, 60, 320, 50))
        self.ShadowLayout = QHBoxLayout(self.layoutWidget_2)
        self.ShadowLayout.setSpacing(10)
        self.ShadowLayout.setObjectName(u"ShadowLayout")
        self.ShadowLayout.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.ShadowLayout.setContentsMargins(5, 5, 5, 5)
        self.disable_shadow_btn = QPushButton(self.layoutWidget_2)
        self.disable_shadow_btn.setObjectName(u"disable_shadow_btn")
        self.disable_shadow_btn.setEnabled(False)
        sizePolicy.setHeightForWidth(self.disable_shadow_btn.sizePolicy().hasHeightForWidth())
        self.disable_shadow_btn.setSizePolicy(sizePolicy)
        self.disable_shadow_btn.setMinimumSize(QSize(150, 45))
        self.disable_shadow_btn.setMaximumSize(QSize(150, 45))
        self.disable_shadow_btn.setFont(font3)
        self.disable_shadow_btn.setStyleSheet(u"")
        self.disable_shadow_btn.setCheckable(True)
        self.disable_shadow_btn.setFlat(True)

        self.ShadowLayout.addWidget(self.disable_shadow_btn)

        self.enable_shadow_btn = QPushButton(self.layoutWidget_2)
        self.enable_shadow_btn.setObjectName(u"enable_shadow_btn")
        self.enable_shadow_btn.setEnabled(False)
        sizePolicy.setHeightForWidth(self.enable_shadow_btn.sizePolicy().hasHeightForWidth())
        self.enable_shadow_btn.setSizePolicy(sizePolicy)
        self.enable_shadow_btn.setMinimumSize(QSize(150, 45))
        self.enable_shadow_btn.setMaximumSize(QSize(150, 45))
        self.enable_shadow_btn.setFont(font3)
        self.enable_shadow_btn.setStyleSheet(u"")
        self.enable_shadow_btn.setCheckable(True)
        self.enable_shadow_btn.setFlat(True)

        self.ShadowLayout.addWidget(self.enable_shadow_btn)

        self.gridLayout.addWidget(self.ShadowFrame, 3, 0, 1, 1)

        self.ResolutionkrFrame = QFrame(self.frame)
        self.ResolutionkrFrame.setObjectName(u"ResolutionkrFrame")
        self.ResolutionkrFrame.setMinimumSize(QSize(1, 1))
        self.ResolutionkrFrame.setMaximumSize(QSize(9999, 9999))
        self.resolution_label = QLabel(self.ResolutionkrFrame)
        self.resolution_label.setObjectName(u"resolution_label")
        self.resolution_label.setGeometry(QRect(10, 10, 299, 35))
        font7 = QFont(font_family)
        font7.setPointSize(22)
        font7.setBold(True)
        font7.setWeight(75)
        self.resolution_label.setFont(font7)
        self.resolution_label.setStyleSheet(u"color: #ffffff;")
        self.resolution_btn = QPushButton(self.ResolutionkrFrame)
        self.resolution_btn.setObjectName(u"resolution_btn")
        self.resolution_btn.setGeometry(QRect(10, 60, 150, 45))
        sizePolicy.setHeightForWidth(self.resolution_btn.sizePolicy().hasHeightForWidth())
        self.resolution_btn.setSizePolicy(sizePolicy)
        self.resolution_btn.setMinimumSize(QSize(150, 45))
        self.resolution_btn.setMaximumSize(QSize(150, 45))
        self.resolution_btn.setFont(font3)
        self.resolution_btn.setStyleSheet(u"")
        self.resolution_btn.setCheckable(True)
        self.resolution_btn.setFlat(True)

        self.gridLayout.addWidget(self.ResolutionkrFrame, 3, 1, 1, 1)

        self.stackedWidget.addWidget(self.gfx_page)
        self.other_page = QWidget()
        self.other_page.setObjectName(u"other_page")
        self.other_page_background = QLabel(self.other_page)
        self.other_page_background.setObjectName(u"other_page_background")
        self.other_page_background.setGeometry(QRect(-30, -80, 1311, 741))
        self.other_page_background.setStyleSheet(u"border-image: url(:/Graphics/bg.png);")
        self.tempcleaner_other_btn = QPushButton(self.other_page)
        self.tempcleaner_other_btn.setObjectName(u"tempcleaner_other_btn")
        self.tempcleaner_other_btn.setGeometry(QRect(50, 120, 411, 51))
        self.tempcleaner_other_btn.setMinimumSize(QSize(141, 1))
        self.tempcleaner_other_btn.setMaximumSize(QSize(999, 999))
        font8 = QFont(font_family)
        font8.setPointSize(20)
        font8.setBold(True)
        font8.setWeight(75)
        font8.setKerning(False)
        self.tempcleaner_other_btn.setFont(font8)
        self.tempcleaner_other_btn.setStyleSheet(u"")
        self.tempcleaner_other_btn.setCheckable(False)
        self.gloptimizer_other_btn = QPushButton(self.other_page)
        self.gloptimizer_other_btn.setObjectName(u"gloptimizer_other_btn")
        self.gloptimizer_other_btn.setGeometry(QRect(50, 190, 411, 51))
        self.gloptimizer_other_btn.setMinimumSize(QSize(141, 1))
        self.gloptimizer_other_btn.setMaximumSize(QSize(999, 999))
        self.gloptimizer_other_btn.setFont(font8)
        self.gloptimizer_other_btn.setStyleSheet(u"")
        self.gloptimizer_other_btn.setCheckable(False)
        self.all_other_btn = QPushButton(self.other_page)
        self.all_other_btn.setObjectName(u"all_other_btn")
        self.all_other_btn.setGeometry(QRect(50, 260, 411, 51))
        self.all_other_btn.setMinimumSize(QSize(141, 1))
        self.all_other_btn.setMaximumSize(QSize(999, 999))
        self.all_other_btn.setFont(font8)
        self.all_other_btn.setStyleSheet(u"")
        self.all_other_btn.setCheckable(False)
        self.forceclosegl_other_btn = QPushButton(self.other_page)
        self.forceclosegl_other_btn.setObjectName(u"forceclosegl_other_btn")
        self.forceclosegl_other_btn.setGeometry(QRect(50, 420, 201, 51))
        self.forceclosegl_other_btn.setMinimumSize(QSize(141, 1))
        self.forceclosegl_other_btn.setMaximumSize(QSize(999, 999))
        self.forceclosegl_other_btn.setFont(font8)
        self.forceclosegl_other_btn.setStyleSheet(u"QPushButton {\n"
                                                  "                                background-color: rgba(255, 0, 4, 50);\n"
                                                  "                                border-radius: 8px;\n"
                                                  "                                border: 1px solid #ff0004;\n"
                                                  "                                color: #ffcccc;\n"
                                                  "                                }\n"
                                                  "                                QPushButton:hover {\n"
                                                  "                                background-color: rgba(255, 0, 4, 90);\n"
                                                  "                                }\n"
                                                  "                            ")
        self.forceclosegl_other_btn.setCheckable(False)

        self.uninstallgl_other_btn = QPushButton(self.other_page)
        self.uninstallgl_other_btn.setObjectName(u"uninstallgl_other_btn")
        self.uninstallgl_other_btn.setGeometry(QRect(255, 420, 206, 51))
        self.uninstallgl_other_btn.setMinimumSize(QSize(141, 1))
        self.uninstallgl_other_btn.setMaximumSize(QSize(999, 999))
        self.uninstallgl_other_btn.setFont(font8)
        self.uninstallgl_other_btn.setStyleSheet(u"QPushButton {\n"
                                                  "                                background-color: rgba(255, 50, 50, 60);\n"
                                                  "                                color: #ffcccc;\n"
                                                  "                                border: 1px solid #ff4444;\n"
                                                  "                                border-radius: 8px;\n"
                                                  "                                }\n"
                                                  "                                QPushButton:hover {\n"
                                                  "                                background-color: rgba(255, 0, 0, 90);\n"
                                                  "                                }\n"
                                                  "                            ")
        self.uninstallgl_other_btn.setCheckable(False)

        self.gameloopsuper_other_btn = QPushButton(self.other_page)
        self.gameloopsuper_other_btn.setObjectName(u"gameloopsuper_other_btn")
        self.gameloopsuper_other_btn.setGeometry(QRect(50, 490, 411, 51))
        self.gameloopsuper_other_btn.setMinimumSize(QSize(141, 1))
        self.gameloopsuper_other_btn.setMaximumSize(QSize(999, 999))
        self.gameloopsuper_other_btn.setFont(font8)
        self.gameloopsuper_other_btn.setStyleSheet(u"QPushButton {\n"
                                                  "                                background-color: rgba(255, 215, 0, 50);\n"
                                                  "                                color: #FFD700;\n"
                                                  "                                border: 1px solid #FFD700;\n"
                                                  "                                }\n"
                                                  "                                QPushButton:hover {\n"
                                                  "                                background-color: rgba(255, 215, 0, 80);\n"
                                                  "                                }\n")
        self.gameloopsuper_other_btn.setCheckable(False)

        # GPU Force Button
        self.gpuforce_other_btn = QPushButton(self.other_page)
        self.gpuforce_other_btn.setObjectName(u"gpuforce_other_btn")
        self.gpuforce_other_btn.setGeometry(QRect(50, 560, 411, 51))
        self.gpuforce_other_btn.setMinimumSize(QSize(141, 1))
        self.gpuforce_other_btn.setMaximumSize(QSize(999, 999))
        self.gpuforce_other_btn.setFont(font8)
        self.gpuforce_other_btn.setStyleSheet(u"QPushButton {\n"
                                              "                                background-color: rgba(0, 150, 255, 50);\n"
                                              "                                color: #0096FF;\n"
                                              "                                border: 2px solid #0096FF;\n"
                                              "                                border-radius: 10px;\n"
                                              "                                }\n"
                                              "                                QPushButton:hover {\n"
                                              "                                background-color: rgba(0, 150, 255, 80);\n"
                                              "                                color: white;\n"
                                              "                                }\n"
                                              "                                QPushButton:pressed {\n"
                                              "                                background-color: #0096FF;\n"
                                              "                                color: black;\n"
                                              "                                }")
        self.gpuforce_other_btn.setCheckable(False)
        self.gpuforce_other_btn.setText("Force GPU & Optimize CPU")

        # Essential Drivers Button
        self.drivers_other_btn = QPushButton(self.other_page)
        self.drivers_other_btn.setObjectName(u"drivers_other_btn")
        self.drivers_other_btn.setGeometry(QRect(50, 340, 411, 51))
        self.drivers_other_btn.setMinimumSize(QSize(141, 1))
        self.drivers_other_btn.setMaximumSize(QSize(999, 999))
        self.drivers_other_btn.setFont(font8)
        self.drivers_other_btn.setStyleSheet(u"QPushButton {\n"
                                              "                                background-color: rgba(0, 200, 150, 50);\n"
                                              "                                color: #00C896;\n"
                                              "                                border: 2px solid #00C896;\n"
                                              "                                border-radius: 10px;\n"
                                              "                                }\n"
                                              "                                QPushButton:hover {\n"
                                              "                                background-color: rgba(0, 200, 150, 80);\n"
                                              "                                color: white;\n"
                                              "                                }\n"
                                              "                                QPushButton:pressed {\n"
                                              "                                background-color: #00C896;\n"
                                              "                                color: black;\n"
                                              "                                }")
        self.drivers_other_btn.setCheckable(False)
        self.drivers_other_btn.setText("Essential Drivers \U0001f527")

        self.dns_dropdown = QComboBox(self.other_page)
        self.dns_dropdown.addItem("")
        self.dns_dropdown.addItem("")
        self.dns_dropdown.addItem("")
        self.dns_dropdown.addItem("")
        self.dns_dropdown.addItem("")
        self.dns_dropdown.setObjectName(u"dns_dropdown")
        self.dns_dropdown.setGeometry(QRect(540, 215, 270, 45))
        self.dns_dropdown.setFont(font2)
        self.dns_dropdown.setStyleSheet(u"")
        self.shortcut_dropdown = QComboBox(self.other_page)
        self.shortcut_dropdown.addItem("")
        self.shortcut_dropdown.addItem("")
        self.shortcut_dropdown.addItem("")
        self.shortcut_dropdown.addItem("")
        self.shortcut_dropdown.addItem("")
        self.shortcut_dropdown.setObjectName(u"shortcut_dropdown")
        self.shortcut_dropdown.setGeometry(QRect(540, 85, 270, 45))
        self.shortcut_dropdown.setFont(font2)
        self.shortcut_dropdown.setStyleSheet(u"")
        self.optimizer_label = QLabel(self.other_page)
        self.optimizer_label.setObjectName(u"optimizer_label")
        self.optimizer_label.setGeometry(QRect(30, 50, 351, 51))
        font9 = QFont(font_family)
        font9.setPointSize(28)
        font9.setBold(True)
        font9.setWeight(75)
        self.optimizer_label.setFont(font9)
        self.optimizer_label.setStyleSheet(u"text-align: center;\n"
                                           "                                border: none;\n"
                                           "                                color: rgb(255, 255, 255);\n"
                                           "                            ")
        self.shortcut_other_btn = QPushButton(self.other_page)
        self.shortcut_other_btn.setObjectName(u"shortcut_other_btn")
        self.shortcut_other_btn.setGeometry(QRect(820, 85, 240, 45))
        self.shortcut_other_btn.setFont(font8)
        self.shortcut_other_btn.setStyleSheet(u"")
        self.shortcut_other_btn.setCheckable(False)
        self.line = QFrame(self.other_page)
        self.line.setObjectName(u"line")
        self.line.setGeometry(QRect(480, 110, 20, 361))
        self.line.setFrameShape(QFrame.VLine)
        self.line.setFrameShadow(QFrame.Sunken)
        self.shortcut_label = QLabel(self.other_page)
        self.shortcut_label.setObjectName(u"shortcut_label")
        self.shortcut_label.setGeometry(QRect(540, 40, 350, 40))
        self.shortcut_label.setFont(font8)
        self.shortcut_label.setStyleSheet(u"text-align: center;\n"
                                          "                                border: none;\n"
                                           "                                background: transparent;\n"
                                          "                                color: rgb(255, 255, 255);\n"
                                          "                            ")
        self.dns_label = QLabel(self.other_page)
        self.dns_label.setObjectName(u"dns_label")
        self.dns_label.setGeometry(QRect(540, 170, 350, 40))
        self.dns_label.setFont(font8)
        self.dns_label.setStyleSheet(u"text-align: center;\n"
                                     "                                border: none;\n"
                                      "                                background: transparent;\n"
                                     "                                color: rgb(255, 255, 255);\n"
                                     "                            ")
        self.dns_other_btn = QPushButton(self.other_page)
        self.dns_other_btn.setObjectName(u"dns_other_btn")
        self.dns_other_btn.setGeometry(QRect(820, 215, 240, 45))
        self.dns_other_btn.setFont(font8)
        self.dns_other_btn.setStyleSheet(u"")
        self.dns_other_btn.setCheckable(False)
        self.dns_status_label = QLabel(self.other_page)
        self.dns_status_label.setObjectName(u"dns_status_label")
        self.dns_status_label.setGeometry(QRect(550, 265, 300, 25))
        self.dns_status_label.setFont(font4)
        self.dns_status_label.setStyleSheet(u"color: #969696; background: transparent;")
        self.ipad_label = QLabel(self.other_page)
        self.ipad_label.setObjectName(u"ipad_label")
        self.ipad_label.setGeometry(QRect(540, 330, 350, 40))
        self.ipad_label.setFont(font8)
        self.ipad_label.setStyleSheet(u"text-align: center;\n"
                                      "                                border: none;\n"
                                       "                                background: transparent;\n"
                                      "                                color: rgb(255, 255, 255);\n"
                                      "                            ")
        self.ipad_other_btn = QPushButton(self.other_page)
        self.ipad_other_btn.setObjectName(u"ipad_other_btn")
        self.ipad_other_btn.setGeometry(QRect(820, 375, 240, 45))
        self.ipad_other_btn.setFont(font8)
        self.ipad_other_btn.setStyleSheet(u"")
        self.ipad_other_btn.setCheckable(False)
        self.ipad_dropdown = QComboBox(self.other_page)
        self.ipad_dropdown.addItem("")
        self.ipad_dropdown.addItem("")
        self.ipad_dropdown.addItem("")
        self.ipad_dropdown.addItem("")
        self.ipad_dropdown.setObjectName(u"ipad_dropdown")
        self.ipad_dropdown.setGeometry(QRect(540, 375, 270, 45))
        self.ipad_dropdown.setFont(font2)
        self.ipad_dropdown.setStyleSheet(u"")
        self.ipad_code = QLineEdit(self.other_page)
        self.ipad_code.setObjectName(u"ipad_code")
        self.ipad_code.setGeometry(QRect(540, 435, 270, 35))
        font10 = QFont(font_family)
        font10.setPointSize(17)
        font10.setBold(True)
        font10.setWeight(75)
        self.ipad_code.setFont(font10)
        self.ipad_code.setStyleSheet(u"border-image: url(:/Graphics/fps.png);\n"
                                     "                                text-align: center;\n"
                                     "                                color: #969696;\n"
                                     "\n"
                                     "                            ")
        self.ipad_code.setReadOnly(True)
        self.ipad_code_label = QLabel(self.other_page)
        self.ipad_code_label.setObjectName(u"ipad_code_label")
        self.ipad_code_label.setGeometry(QRect(550, 470, 251, 21))
        font11 = QFont(font_family)
        font11.setPointSize(12)
        font11.setBold(True)
        font11.setWeight(75)
        self.ipad_code_label.setFont(font11)
        self.ipad_code_label.setStyleSheet(u"color: #969696; background: transparent;")
        self.ipad_rest_btn = QPushButton(self.other_page)
        self.ipad_rest_btn.setObjectName(u"ipad_rest_btn")
        self.ipad_rest_btn.setGeometry(QRect(820, 435, 240, 35))
        font12 = QFont(font_family)
        font12.setPointSize(15)
        font12.setBold(True)
        font12.setWeight(75)
        self.ipad_rest_btn.setFont(font12)
        self.ipad_rest_btn.setStyleSheet(u"")
        self.ipad_rest_btn.setCheckable(False)
        self.stackedWidget.addWidget(self.other_page)

        
        # --- gameloop_page ---
        self.gameloop_page = QWidget()
        self.gameloop_page.setObjectName(u"gameloop_page")
        self.gameloop_page_background = QLabel(self.gameloop_page)
        self.gameloop_page_background.setObjectName(u"gameloop_page_background")
        self.gameloop_page_background.setGeometry(QRect(0, 0, 712, 645))
        self.gameloop_page_background.setPixmap(QPixmap(resource_path(u"assets/Pages.png")))
        self.gameloop_page_background.setScaledContents(True)

        self.gl_settings_label = QLabel(self.gameloop_page)
        self.gl_settings_label.setObjectName(u"gl_settings_label")
        self.gl_settings_label.setGeometry(QRect(30, 15, 351, 51))
        self.gl_settings_label.setFont(font9)
        self.gl_settings_label.setStyleSheet(u"text-align: center;\n"
                                             "                                border: none;\n"
                                             "                                color: rgb(255, 255, 255);\n"
                                             "                            ")
        self.gl_render_label = QLabel(self.gameloop_page)
        self.gl_render_label.setObjectName(u"gl_render_label")
        self.gl_render_label.setGeometry(QRect(30, 60, 351, 31))
        self.gl_render_label.setFont(font11)
        self.gl_render_label.setStyleSheet(u"color: #969696;")

        self.gameloop_frame = QFrame(self.gameloop_page)
        self.gameloop_frame.setGeometry(QRect(30, 85, 650, 550))
        self.gameloop_frame.setStyleSheet("color: white;")

        self.gameloop_render_grp = QGroupBox("Screen rendering mode:", self.gameloop_frame)
        self.gameloop_render_grp.setGeometry(QRect(10, 5, 630, 80))
        self.gameloop_render_grp.setFont(font1)
        self.gameloop_render_grp.setStyleSheet("QGroupBox { border: 2px solid #5c5c5c; border-radius: 10px; margin-top: 15px; color: #f7d620; } QGroupBox::title { subcontrol-origin: margin; left: 15px; padding: 0 5px; }")
        self.gl_render_opengl = QRadioButton("OpenGL+", self.gameloop_render_grp)
        self.gl_render_opengl.setGeometry(QRect(20, 35, 120, 30))
        self.gl_render_directx = QRadioButton("DirectX+", self.gameloop_render_grp)
        self.gl_render_directx.setGeometry(QRect(150, 35, 120, 30))
        self.gl_render_auto = QRadioButton("Auto", self.gameloop_render_grp)
        self.gl_render_auto.setGeometry(QRect(280, 35, 300, 30))
        for rb in [self.gl_render_opengl, self.gl_render_directx, self.gl_render_auto]:
            rb.setFont(font11)
            rb.setStyleSheet("QRadioButton { color: white; } QRadioButton::indicator { width: 18px; height: 18px; }")

        # CheckBoxes - Column 1
        self.gl_cb_render_cache = QCheckBox("Enable rendering cache", self.gameloop_frame)
        self.gl_cb_render_cache.setGeometry(QRect(20, 95, 300, 30))
        self.gl_cb_prioritize_gpu = QCheckBox("Prioritize GPU", self.gameloop_frame)
        self.gl_cb_prioritize_gpu.setGeometry(QRect(20, 130, 300, 30))
        self.gl_cb_vsync = QCheckBox("Enable VSync", self.gameloop_frame)
        self.gl_cb_vsync.setGeometry(QRect(20, 165, 300, 30))
        self.gl_cb_root = QCheckBox("Root Authority", self.gameloop_frame)
        self.gl_cb_root.setGeometry(QRect(20, 200, 300, 30))

        # CheckBoxes - Column 2
        self.gl_cb_force_global = QCheckBox("Force Global cache", self.gameloop_frame)
        self.gl_cb_force_global.setGeometry(QRect(330, 95, 300, 30))
        self.gl_cb_render_opt = QCheckBox("Rendering optimization", self.gameloop_frame)
        self.gl_cb_render_opt.setGeometry(QRect(330, 130, 300, 30))
        self.gl_cb_adb = QCheckBox("adb Debugging", self.gameloop_frame)
        self.gl_cb_adb.setGeometry(QRect(330, 165, 300, 30))

        cb_style = """
            QCheckBox { color: white; spacing: 10px; }
            QCheckBox::indicator { width: 20px; height: 20px; border: 1px solid #5c5c5c; border-radius: 4px; }
            QCheckBox::indicator:checked { background-color: #f7d620; image: url(:/Graphics/check_mark.png); }
            QCheckBox::indicator:unchecked:hover { border: 1px solid #f7d620; }
        """
        for cb in [self.gl_cb_render_cache, self.gl_cb_force_global, self.gl_cb_prioritize_gpu, 
                   self.gl_cb_render_opt, self.gl_cb_vsync, self.gl_cb_adb, self.gl_cb_root]:
            cb.setFont(font11)
            cb.setStyleSheet(cb_style)

        # Dropdowns - Row 1
        self.gl_label_aa = QLabel("Anti-aliasing:", self.gameloop_frame)
        self.gl_label_aa.setGeometry(QRect(20, 245, 250, 25))
        self.gl_label_aa.setFont(font10)
        self.gl_combo_aa = QComboBox(self.gameloop_frame)
        self.gl_combo_aa.setGeometry(QRect(20, 275, 250, 35))
        self.gl_label_res = QLabel("Resolution:", self.gameloop_frame)
        self.gl_label_res.setGeometry(QRect(330, 245, 250, 25))
        self.gl_label_res.setFont(font10)
        self.gl_combo_res = QComboBox(self.gameloop_frame)
        self.gl_combo_res.setGeometry(QRect(330, 275, 250, 35))

        # Dropdowns - Row 2
        self.gl_label_mem = QLabel("Memory:", self.gameloop_frame)
        self.gl_label_mem.setGeometry(QRect(20, 320, 250, 25))
        self.gl_label_mem.setFont(font10)
        self.gl_combo_mem = QComboBox(self.gameloop_frame)
        self.gl_combo_mem.setGeometry(QRect(20, 350, 250, 35))
        self.gl_label_dpi = QLabel("Screen DPI:", self.gameloop_frame)
        self.gl_label_dpi.setGeometry(QRect(330, 320, 250, 25))
        self.gl_label_dpi.setFont(font10)
        self.gl_combo_dpi = QComboBox(self.gameloop_frame)
        self.gl_combo_dpi.setGeometry(QRect(330, 350, 250, 35))

        # Dropdowns - Row 3
        self.gl_label_cpu = QLabel("Processor:", self.gameloop_frame)
        self.gl_label_cpu.setGeometry(QRect(20, 395, 250, 25))
        self.gl_label_cpu.setFont(font10)
        self.gl_combo_cpu = QComboBox(self.gameloop_frame)
        self.gl_combo_cpu.setGeometry(QRect(20, 425, 250, 35))

        self.gl_combo_aa.addItems(["Off", "Balanced", "Ultra"])
        self.gl_combo_mem.addItems(["Auto", "1024M", "1536M", "2048M", "4096M", "8192M"])
        self.gl_combo_cpu.addItems(["Auto", "1", "2", "4", "8"])
        self.gl_combo_res.addItems(["1024x576", "1280x720", "1366x768", "1600x900", "1920x1080", "2560x1440"])
        self.gl_combo_dpi.addItems(["120", "160", "240", "320", "480"])

        combo_style = """
            QComboBox { background-color: #272c36; color: white; border: 1px solid #5c5c5c; border-radius: 5px; padding-left: 10px; }
            QComboBox:hover { border: 1px solid #f7d620; }
            QComboBox::drop-down { border: none; width: 30px; }
            QComboBox QAbstractItemView { background-color: #272c36; color: white; selection-background-color: #f7d620; selection-color: black; border: 1px solid white; }
        """
        for combo in [self.gl_combo_aa, self.gl_combo_mem, self.gl_combo_cpu, self.gl_combo_res, self.gl_combo_dpi]:
            combo.setFont(font10)
            combo.setStyleSheet(combo_style)

        # Buttons Row
        self.gameloop_save_btn = QPushButton("Save Engine Settings", self.gameloop_frame)
        self.gameloop_save_btn.setGeometry(QRect(330, 425, 280, 45))
        self.gameloop_save_btn.setFont(font10)
        
        self.gameloop_smart_btn = QPushButton("Smart Optimize", self.gameloop_frame)
        self.gameloop_smart_btn.setGeometry(QRect(20, 480, 590, 50))
        self.gameloop_smart_btn.setFont(font10)

        
        smart_btn_style = """
            QPushButton { 
                background-color: rgba(247, 214, 32, 20); 
                color: #f7d620; 
                border-radius: 10px; 
                font-weight: bold;
                border: 2px solid #f7d620;
            } 
            QPushButton:hover { 
                background-color: rgba(247, 214, 32, 40); 
                color: white;
            }
            QPushButton:pressed {
                background-color: #f7d620;
                color: black;
            }
        """
        self.gameloop_smart_btn.setStyleSheet(smart_btn_style)

        self.gameloop_save_btn.setStyleSheet("""
            QPushButton { 
                background-color: #f7d620; 
                color: black; 
                border-radius: 10px; 
                font-weight: bold;
                border: 2px solid #bda31a;
            } 
            QPushButton:hover { 
                background-color: #ffeb3b; 
                border: 2px solid white;
            }
            QPushButton:pressed {
                background-color: #c4aa18;
                padding-top: 5px;
            }
            QPushButton:disabled {
                background-color: #4d4d4d;
                color: #8c8c8c;
            }
        """)

        self.stackedWidget.addWidget(self.gameloop_page)

        self.about_page = QWidget()
        self.about_page.setObjectName(u"about_page")
        self.about_page.setMaximumSize(QSize(1081, 651))
        self.label_8 = QLabel(self.about_page)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setEnabled(False)
        self.label_8.setGeometry(QRect(-30, -80, 1311, 741))
        self.label_8.setStyleSheet(u"border-image: url(:/Graphics/bg.png);")
        self.about_label_text = QLabel(self.about_page)
        self.about_label_text.setObjectName(u"about_label_text")
        self.about_label_text.setGeometry(QRect(20, 0, 1061, 571))
        self.about_label_text.setMaximumSize(QSize(1061, 571))
        font13 = QFont(font_family)
        font13.setPointSize(20)
        font13.setBold(False)
        font13.setWeight(50)
        self.about_label_text.setFont(font13)
        self.about_label_text.setStyleSheet(u"text-align: center;\n"
                                            "                                border: none;\n"
                                            "                                color: rgb(255, 255, 255);\n"
                                            "                            ")
        self.about_label_text.setOpenExternalLinks(True)
        self.stackedWidget.addWidget(self.about_page)
        self.appname_label = QLabel(self.centralwidget)
        self.appname_label.setObjectName(u"appname_label")
        self.appname_label.setGeometry(QRect(30, 0, 669, 57))
        font14 = QFont(font_family)
        font14.setPointSize(35)
        font14.setBold(True)
        font14.setWeight(75)
        self.appname_label.setFont(font14)
        self.appname_label.setStyleSheet(u"text-align: center;\n"
                                         "                        border: none;\n"
                                         "                        color: rgb(255, 255, 255);\n"
                                         "                    ")
        self.appstatus_label = QLabel(self.centralwidget)
        self.appstatus_label.setObjectName(u"appstatus_label")
        self.appstatus_label.setGeometry(QRect(30, 672, 120, 44))
        font15 = QFont(font_family)
        font15.setPointSize(19)
        font15.setBold(True)
        font15.setWeight(75)
        self.appstatus_label.setFont(font15)
        self.appstatus_label.setStyleSheet(u"color: #f7d620; background: transparent;")
        self.appstatus_text_lable = QLabel(self.centralwidget)
        self.appstatus_text_lable.setObjectName(u"appstatus_text_lable")
        self.appstatus_text_lable.setGeometry(QRect(130, 672, 800, 44))
        font16 = QFont(font_family)
        font16.setPointSize(16)
        font16.setBold(True)
        font16.setWeight(75)
        self.appstatus_text_lable.setFont(font16)
        self.appstatus_text_lable.setStyleSheet(u"color: #ffffff; background: transparent;")
        self.close_btn = QPushButton(self.centralwidget)
        self.close_btn.setObjectName(u"close_btn")
        self.close_btn.setGeometry(QRect(1240, 10, 51, 41))
        font17 = QFont()
        font17.setFamily(u"MS Shell Dlg 2")
        font17.setPointSize(30)
        font17.setBold(True)
        font17.setWeight(75)
        self.close_btn.setFont(font17)
        self.close_btn.setStyleSheet(u"QPushButton {\n"
                                     "                        border-image: none;\n"
                                     "                        background-color: none;\n"
                                     "                        background-repeat: no-repeat;\n"
                                     "                        text-align: center;\n"
                                     "                        border: none;\n"
                                     "                        color: #FFF;\n"
                                     "                        padding-top: -3px;\n"
                                     "                        }\n"
                                     "\n"
                                     "                        QPushButton:checked,\n"
                                     "                        QPushButton:pressed {\n"
                                     "                        border-image: none;\n"
                                     "                        background-color: rgba(0, 0, 0, 0);\n"
                                     "                        background-repeat: no-repeat;\n"
                                     "                        color: #c7fff6;\n"
                                     "                        text-align: center;\n"
                                     "                        }\n"
                                     "                    ")
        self.close_btn.setFlat(True)
        self.minimize_btn = QPushButton(self.centralwidget)
        self.minimize_btn.setObjectName(u"minimize_btn")
        self.minimize_btn.setGeometry(QRect(1180, 10, 51, 41))
        font18 = QFont()
        font18.setFamily(u"MS Shell Dlg 2")
        font18.setPointSize(36)
        font18.setBold(True)
        font18.setWeight(75)
        self.minimize_btn.setFont(font18)
        self.minimize_btn.setStyleSheet(u"QPushButton {\n"
                                        "                        border-image: none;\n"
                                        "                        background-color: none;\n"
                                        "                        background-repeat: no-repeat;\n"
                                        "                        text-align: center;\n"
                                        "                        border: none;\n"
                                        "                        color: #FFF;\n"
                                        "                        padding-top: -3px;\n"
                                        "                        }\n"
                                        "\n"
                                        "                        QPushButton:checked,\n"
                                        "                        QPushButton:pressed {\n"
                                        "                        border-image: none;\n"
                                        "                        background-color: rgba(0, 0, 0, 0);\n"
                                        "                        background-repeat: no-repeat;\n"
                                        "                        color: #c7fff6;\n"
                                        "                        text-align: center;\n"
                                        "                        }\n"
                                        "                    ")
        self.minimize_btn.setFlat(True)
        self.PagesFrame = QFrame(self.centralwidget)
        self.PagesFrame.setObjectName(u"PagesFrame")
        self.PagesFrame.setGeometry(QRect(1140, 50, 168, 661))
        self.PagesFrame.setStyleSheet(u"QPushButton {\n"
                                      "                        border-image: none;\n"
                                      "                        text-align: center;\n"
                                      "                        border: none;\n"
                                      "                        color: #969696; /* sets the text color to #969696 */\n"
                                      "                        text-align: center; /* aligns the text to the left */\n"
                                      "\n"
                                      "                        }\n"
                                      "\n"
                                      "                        QPushButton:checked {\n"
                                      "\n"
                                      "                        border-image: url(:/Graphics/menu_checked.png);\n"
                                      "\n"
                                      "                        color: #f7d620; /* sets the text color to #b7ece4 */\n"
                                      "                        background-repeat: no-repeat;\n"
                                      "                        text-align: center;\n"
                                      "                        }\n"
                                      "                    ")
        self.PagesFrame.setFrameShape(QFrame.NoFrame)
        self.gfx_button = QPushButton(self.PagesFrame)
        self.gfx_button.setObjectName(u"gfx_button")
        self.gfx_button.setGeometry(QRect(0, 10, 168, 80))
        self.gfx_button.setFont(font6)
        self.gfx_button.setStyleSheet(u"")
        self.gfx_button.setCheckable(True)
        self.gfx_button.setChecked(True)
        self.gfx_button.setFlat(True)
        self.other_button = QPushButton(self.PagesFrame)
        self.other_button.setObjectName(u"other_button")
        self.other_button.setGeometry(QRect(0, 90, 168, 80))
        self.other_button.setFont(font6)
        self.other_button.setStyleSheet(u"")
        self.other_button.setCheckable(True)
        self.other_button.setFlat(True)
        
        self.gameloop_button = QPushButton(self.PagesFrame)
        self.gameloop_button.setObjectName(u"gameloop_button")
        self.gameloop_button.setGeometry(QRect(0, 170, 168, 80))
        self.gameloop_button.setFont(font6)
        self.gameloop_button.setStyleSheet(u"")
        self.gameloop_button.setCheckable(True)
        self.gameloop_button.setFlat(True)

        self.about_button = QPushButton(self.PagesFrame)
        self.about_button.setObjectName(u"about_button")
        self.about_button.setGeometry(QRect(0, 565, 168, 80))
        self.about_button.setFont(font6)
        self.about_button.setStyleSheet(u"")
        self.about_button.setCheckable(True)
        self.about_button.setFlat(True)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        self.stackedWidget.setCurrentIndex(0)

        self.apply_cyberpunk_theme(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
        # setupUi

    def apply_cyberpunk_theme(self, MainWindow):
        MainWindow.setStyleSheet("""
            QWidget {
                background-color: #121212;
                color: #E6E6E6;
                font-family: "Segoe UI", "Roboto", "Inter";
                font-size: 12px;
            }

            QLabel {
                background: transparent;
                color: #F2F2F2;
            }

            #title_bar {
                background-color: #1A1B1F;
                border: 1px solid #2B2D33;
                border-radius: 12px;
            }

            #stackedWidget {
                background-color: #121212;
                border: 1px solid #25262C;
                border-radius: 14px;
            }

            QFrame#GraphicsFrame, QFrame#FramerateFrame, QFrame#StyleFrame, QFrame#ShadowFrame,
            QFrame#ResolutionkrFrame, QFrame#gameloop_frame {
                background-color: #1E1F24;
                border: 1px solid #2F3139;
                border-radius: 14px;
            }

            QFrame#other_left_card, QFrame#other_right_card {
                background-color: #171A21;
                border: 1px solid #292D36;
                border-radius: 14px;
            }

            QPushButton {
                background-color: #23252B;
                color: #EAEAEA;
                border: 1px solid #30333B;
                border-radius: 10px;
                padding: 8px 12px;
                font-weight: 600;
            }

            QPushButton:hover {
                border: 1px solid #00EAFF;
                background-color: #2A2D35;
            }

            QPushButton:pressed {
                background-color: #00EAFF;
                color: #101114;
                border: 1px solid #00EAFF;
            }

            QPushButton:checked {
                background-color: #00EAFF;
                color: #101114;
                border: 1px solid #8CF7FF;
            }

            #submit_gfx_btn, #gameloop_save_btn {
                background-color: #FFEA00;
                color: #0F1115;
                border: 1px solid #FFEA00;
                font-weight: 700;
            }

            #submit_gfx_btn:hover, #gameloop_save_btn:hover {
                background-color: #FFF066;
            }

            /* Right column action buttons: high-contrast neon outline style */
            #dns_other_btn, #shortcut_other_btn, #ipad_other_btn, #ipad_rest_btn {
                background-color: rgba(255, 234, 0, 0.08);
                color: #FFEA00;
                border: 1px solid #FFEA00;
                font-weight: 700;
            }

            #dns_other_btn:hover, #shortcut_other_btn:hover, #ipad_other_btn:hover, #ipad_rest_btn:hover {
                background-color: rgba(255, 234, 0, 0.2);
                color: #FFF5A3;
                border: 1px solid #FFF066;
            }

            #gfx_button, #other_button, #gameloop_button, #about_button {
                border-radius: 12px;
                background-color: #1B1D22;
                color: #A7A9AF;
                border: 1px solid #2C2F36;
                min-height: 58px;
                font-size: 14px;
                font-weight: 700;
            }

            #supersmooth_graphics_btn, #smooth_graphics_btn, #balanced_graphics_btn, #hd_graphics_btn,
            #hdr_graphics_btn, #ultrahd_graphics_btn, #uhd_graphics_btn, #low_fps_btn, #medium_fps_btn,
            #high_fps_btn, #ultra_fps_btn, #extreme_fps_btn, #fps90_fps_btn, #fps120_fps_btn {
                font-size: 12px;
                font-weight: 600;
                padding: 4px 8px;
                text-align: center;
            }

            #gfx_button:hover, #other_button:hover, #gameloop_button:hover, #about_button:hover {
                color: #EAFBFF;
                border: 1px solid #00EAFF;
                background-color: #252933;
            }

            #gfx_button:checked, #other_button:checked, #gameloop_button:checked, #about_button:checked {
                color: #00EAFF;
                border: 1px solid #00EAFF;
                background-color: #1D2B30;
            }

            QComboBox, QLineEdit {
                background-color: #1A1C22;
                color: #ECECEC;
                border: 1px solid #323540;
                border-radius: 10px;
                padding: 7px 10px;
            }

            QComboBox:hover, QLineEdit:hover {
                border: 1px solid #00EAFF;
            }

            QComboBox::drop-down {
                border: none;
                width: 30px;
            }
            QComboBox::down-arrow {
                image: url('""" + resource_path(r"assets\down_arrow.svg").replace("\\", "/") + """');
                width: 22px;
                height: 22px;
            }

            QComboBox QAbstractItemView {
                background-color: #1A1C22;
                color: #EAEAEA;
                border: 1px solid #00EAFF;
                selection-background-color: #00EAFF;
                selection-color: #0D0F12;
            }

            /* Modern toggle switch style for checkboxes */
            QCheckBox {
                spacing: 10px;
                color: #EAEAEA;
                font-weight: 500;
            }

            QCheckBox::indicator {
                width: 40px;
                height: 22px;
                border-radius: 11px;
                background-color: #3C4049;
                border: 1px solid #555A66;
            }

            QCheckBox::indicator:checked {
                background-color: #00EAFF;
                border: 1px solid #00EAFF;
            }

            /* Cleaner radio buttons with neon state */
            QRadioButton {
                color: #EAEAEA;
                spacing: 8px;
            }

            QRadioButton::indicator {
                width: 16px;
                height: 16px;
                border-radius: 8px;
                border: 1px solid #5D6370;
                background-color: #1C1F25;
            }

            QRadioButton::indicator:checked {
                background-color: #00EAFF;
                border: 1px solid #00EAFF;
            }

            #optimizer_label, #shortcut_label, #dns_label, #ipad_label, #gl_settings_label {
                font-size: 16px;
                font-weight: 700;
                color: #FFFFFF;
            }

            #gl_render_label, #gl_label_aa, #gl_label_mem, #gl_label_cpu, #gl_label_res, #gl_label_dpi {
                font-size: 14px;
                font-weight: 600;
                color: #E7EBF0;
            }

            #appstatus_label {
                color: #FFEA00;
                font-size: 16px;
                font-weight: 700;
            }

            #appstatus_text_lable {
                color: #DEE4EC;
                font-size: 14px;
                font-weight: 500;
            }
        """)

        self.centralwidget.setStyleSheet("background-color: #121212;")
        self.appbackground.hide()
        self.gfx_page_background.hide()
        self.other_page_background.hide()
        self.gameloop_page_background.hide()
        self.label_8.hide()

        self.title_bar = QFrame(self.centralwidget)
        self.title_bar.setObjectName("title_bar")
        self.title_bar.setGeometry(QRect(18, 10, 1274, 52))
        self.title_bar.lower()

        self.appname_label.setGeometry(QRect(36, 12, 820, 44))
        self.appname_label.setStyleSheet("color: #F7F9FB; font-size: 24px; font-weight: 700;")

        self.minimize_btn.setGeometry(QRect(1194, 15, 40, 36))
        self.close_btn.setGeometry(QRect(1238, 15, 40, 36))
        self.minimize_btn.setText("–")
        self.close_btn.setText("✕")
        self.minimize_btn.setStyleSheet("QPushButton { background-color: transparent; color: #C7CBD3; border: none; border-radius: 8px; } QPushButton:hover { background-color: #2D3038; color: #00EAFF; }")
        self.close_btn.setStyleSheet("QPushButton { background-color: transparent; color: #C7CBD3; border: none; border-radius: 8px; } QPushButton:hover { background-color: #3A1F24; color: #FF5A6A; }")

        self.PagesFrame.setStyleSheet("background: transparent;")
        self.PagesFrame.setGeometry(QRect(1132, 78, 168, 636))
        self.stackedWidget.setGeometry(QRect(24, 78, 1092, 590))
        self.appstatus_label.setGeometry(QRect(28, 678, 120, 32))
        self.appstatus_text_lable.setGeometry(QRect(132, 678, 972, 32))

        # Keep sidebar buttons balanced and leave clean spacing for About.
        self.gfx_button.setGeometry(QRect(0, 14, 168, 78))
        self.other_button.setGeometry(QRect(0, 96, 168, 78))
        self.gameloop_button.setGeometry(QRect(0, 178, 168, 78))
        self.about_button.setGeometry(QRect(0, 260, 168, 78))

        # Other page layout polish: left and right column card containers.
        self.other_left_card = QFrame(self.other_page)
        self.other_left_card.setObjectName("other_left_card")
        self.other_left_card.setGeometry(QRect(14, 24, 468, 538))
        self.other_left_card.lower()
        self.other_right_card = QFrame(self.other_page)
        self.other_right_card.setObjectName("other_right_card")
        self.other_right_card.setGeometry(QRect(500, 24, 566, 538))
        self.other_right_card.lower()

        self.optimizer_label.setGeometry(QRect(30, 34, 351, 42))
        self.tempcleaner_other_btn.setGeometry(QRect(36, 90, 430, 44))
        self.gloptimizer_other_btn.setGeometry(QRect(36, 146, 430, 44))
        self.all_other_btn.setGeometry(QRect(36, 202, 430, 44))
        self.drivers_other_btn.setGeometry(QRect(36, 270, 430, 44))
        self.forceclosegl_other_btn.setGeometry(QRect(36, 388, 210, 44))
        self.uninstallgl_other_btn.setGeometry(QRect(256, 388, 210, 44))
        self.gameloopsuper_other_btn.setGeometry(QRect(36, 444, 430, 44))
        self.gpuforce_other_btn.setGeometry(QRect(36, 500, 430, 44))

        self.shortcut_label.setGeometry(QRect(528, 46, 320, 30))
        self.shortcut_dropdown.setGeometry(QRect(528, 82, 300, 38))
        self.shortcut_other_btn.setGeometry(QRect(836, 82, 220, 38))
        self.dns_label.setGeometry(QRect(528, 138, 320, 30))
        self.dns_dropdown.setGeometry(QRect(528, 174, 300, 38))
        self.dns_other_btn.setGeometry(QRect(836, 174, 220, 38))
        self.dns_status_label.setGeometry(QRect(536, 216, 320, 22))
        self.ipad_label.setGeometry(QRect(528, 274, 320, 30))
        self.ipad_dropdown.setGeometry(QRect(528, 310, 300, 38))
        self.ipad_other_btn.setGeometry(QRect(836, 310, 220, 38))
        self.ipad_code.setGeometry(QRect(528, 358, 300, 32))
        self.ipad_rest_btn.setGeometry(QRect(836, 358, 220, 32))
        self.ipad_code_label.setGeometry(QRect(536, 392, 280, 20))

        # GFX page: keep all sections visible inside the reduced stacked area.
        self.frame.setGeometry(QRect(0, 0, 1081, 500))
        self.submit_gfx_btn.setGeometry(QRect(908, 528, 156, 46))
        self.connect_gameloop_btn.setGeometry(QRect(592, 528, 304, 46))
        self.PubgchooseFrame.setGeometry(QRect(20, 522, 268, 72))
        self.pubgchoose_btn.setGeometry(QRect(188, 10, 71, 42))
        self.pubgchoose_dropdown.setGeometry(QRect(0, 10, 180, 42))
        self.pubgchoose_label.setGeometry(QRect(0, 54, 260, 16))
        # Keep bottom action row above the main frame layer.
        self.submit_gfx_btn.raise_()
        self.connect_gameloop_btn.raise_()
        self.PubgchooseFrame.raise_()

        # Engine page spacing and button alignment.
        self.gl_settings_label.setGeometry(QRect(30, 16, 360, 40))
        self.gl_render_label.hide()
        self.gameloop_frame.setGeometry(QRect(24, 64, 1040, 512))
        self.gameloop_render_grp.setGeometry(QRect(16, 10, 650, 70))
        self.gl_render_opengl.setGeometry(QRect(20, 34, 130, 30))
        self.gl_render_directx.setGeometry(QRect(165, 34, 120, 30))
        self.gl_render_auto.setGeometry(QRect(300, 34, 280, 30))
        self.gl_cb_render_cache.setGeometry(QRect(20, 88, 300, 30))
        self.gl_cb_prioritize_gpu.setGeometry(QRect(20, 122, 300, 30))
        self.gl_cb_vsync.setGeometry(QRect(20, 156, 300, 30))
        self.gl_cb_root.setGeometry(QRect(20, 190, 300, 30))
        self.gl_cb_force_global.setGeometry(QRect(330, 88, 300, 30))
        self.gl_cb_render_opt.setGeometry(QRect(330, 122, 300, 30))
        self.gl_cb_adb.setGeometry(QRect(330, 156, 300, 30))
        self.gl_label_aa.setGeometry(QRect(20, 230, 250, 25))
        self.gl_combo_aa.setGeometry(QRect(20, 258, 250, 35))
        self.gl_label_res.setGeometry(QRect(330, 230, 250, 25))
        self.gl_combo_res.setGeometry(QRect(330, 258, 250, 35))
        self.gl_label_mem.setGeometry(QRect(20, 302, 250, 25))
        self.gl_combo_mem.setGeometry(QRect(20, 330, 250, 35))
        self.gl_label_dpi.setGeometry(QRect(330, 302, 250, 25))
        self.gl_combo_dpi.setGeometry(QRect(330, 330, 250, 35))
        self.gl_label_cpu.setGeometry(QRect(20, 374, 250, 25))
        self.gl_combo_cpu.setGeometry(QRect(20, 402, 250, 35))
        self.gameloop_save_btn.setGeometry(QRect(330, 402, 280, 40))
        self.gameloop_smart_btn.setGeometry(QRect(20, 454, 590, 42))

    def retranslateUi(self, MainWindow):
            MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Mo-Tech", None))
            self.appbackground.setText("")
            self.gfx_page_background.setText("")
            self.submit_gfx_btn.setText(QCoreApplication.translate("MainWindow", u"Submit", None))
            # if QT_CONFIG(tooltip)
            self.connect_gameloop_btn.setToolTip(
                    QCoreApplication.translate("MainWindow", u"Click here to connect to Gameloop", None))
            # endif // QT_CONFIG(tooltip)
            self.connect_gameloop_btn.setText(QCoreApplication.translate("MainWindow", u"Connect to Gameloop", None))
            self.pubgchoose_btn.setText(QCoreApplication.translate("MainWindow", u"Use", None))
            self.pubgchoose_label.setText(
                    QCoreApplication.translate("MainWindow", u"Select the game version you need to use.", None))
            self.graphics_label.setText(QCoreApplication.translate("MainWindow", u"Graphics", None))
            self.supersmooth_graphics_btn.setText(QCoreApplication.translate("MainWindow", u"Super Smooth (BETA)", None))
            self.smooth_graphics_btn.setText(QCoreApplication.translate("MainWindow", u"Smooth", None))
            self.balanced_graphics_btn.setText(QCoreApplication.translate("MainWindow", u"Balanced", None))
            self.hd_graphics_btn.setText(QCoreApplication.translate("MainWindow", u"HD", None))
            self.hdr_graphics_btn.setText(QCoreApplication.translate("MainWindow", u"HDR", None))
            self.ultrahd_graphics_btn.setText(QCoreApplication.translate("MainWindow", u"Ultra HDR", None))
            # if QT_CONFIG(tooltip)
            self.uhd_graphics_btn.setToolTip(
                    QCoreApplication.translate("MainWindow", u"<html><head/><body><p>Extreme HDR graphics profile.</p></body></html>\n"
                                                             "                                            ", None))
            # endif // QT_CONFIG(tooltip)
            self.uhd_graphics_btn.setText(QCoreApplication.translate("MainWindow", u"Extreme HDR", None))
            self.fps_label.setText(QCoreApplication.translate("MainWindow", u"Frame Rate", None))
            self.low_fps_btn.setText(QCoreApplication.translate("MainWindow", u"Power Saving", None))
            self.medium_fps_btn.setText(QCoreApplication.translate("MainWindow", u"Medium", None))
            self.high_fps_btn.setText(QCoreApplication.translate("MainWindow", u"High", None))
            self.ultra_fps_btn.setText(QCoreApplication.translate("MainWindow", u"Ultra", None))
            self.extreme_fps_btn.setText(QCoreApplication.translate("MainWindow", u"Extreme", None))
            self.fps90_fps_btn.setText(QCoreApplication.translate("MainWindow", u"Extreme+", None))
            self.fps120_fps_btn.setText(QCoreApplication.translate("MainWindow", u"Ultra Extreme", None))
            self.style_label.setText(QCoreApplication.translate("MainWindow", u"Style", None))
            self.shadow_label.setText(QCoreApplication.translate("MainWindow", u"Shadow", None))
            # if QT_CONFIG(tooltip)
            self.disable_shadow_btn.setToolTip(QCoreApplication.translate("MainWindow", u"Soon Can Edit", None))
            # endif // QT_CONFIG(tooltip)
            self.disable_shadow_btn.setText(QCoreApplication.translate("MainWindow", u"Disable", None))
            # if QT_CONFIG(tooltip)
            self.enable_shadow_btn.setToolTip(QCoreApplication.translate("MainWindow", u"Soon Can Edit", None))
            # endif // QT_CONFIG(tooltip)
            self.enable_shadow_btn.setText(QCoreApplication.translate("MainWindow", u"Enable", None))
            self.resolution_label.setText(QCoreApplication.translate("MainWindow", u"Resolution PUBG KR", None))
            self.resolution_btn.setText(QCoreApplication.translate("MainWindow", u"1080p", None))
            self.other_page_background.setText("")
            # if QT_CONFIG(tooltip)
            self.tempcleaner_other_btn.setToolTip(
                    QCoreApplication.translate("MainWindow", u"Clean temporary files and boost system performance.",
                                               None))
            # endif // QT_CONFIG(tooltip)
            self.tempcleaner_other_btn.setText(QCoreApplication.translate("MainWindow", u"Temp Cleaner", None))
            # if QT_CONFIG(tooltip)
            self.gloptimizer_other_btn.setToolTip(
                    QCoreApplication.translate("MainWindow", u"<html><head/><body><p>1- Optimize Gameloop Registry in\n"
                                                             "                                Windows. </p><p>2- Nvidia Optimizer (Nvidia GPU). </p><p>3- Add\n"
                                                             "                                to Exclusion List for faster game startup.</p></body></html>\n"
                                                             "                            ", None))
            # endif // QT_CONFIG(tooltip)
            self.gloptimizer_other_btn.setText(QCoreApplication.translate("MainWindow", u"Gameloop Optimizer", None))
            # if QT_CONFIG(tooltip)
            self.all_other_btn.setToolTip(QCoreApplication.translate("MainWindow",
                                                                     u"<html><head/><body><p align=\"center\">Temp Cleaner</p><p\n"
                                                                     "                                align=\"center\">Gameloop Optimizer</p><p align=\"center\">&gt;&gt; One-click Magic\n"
                                                                     "                                &lt;&lt;</p></body></html>\n"
                                                                     "                            ", None))
            # endif // QT_CONFIG(tooltip)
            self.all_other_btn.setText(QCoreApplication.translate("MainWindow", u"\u2b06\ufe0f All \u2b06\ufe0f", None))
            # if QT_CONFIG(tooltip)
            self.forceclosegl_other_btn.setToolTip(
                    QCoreApplication.translate("MainWindow", u"Force Kill Gameloop Processes.", None))
            # endif // QT_CONFIG(tooltip)
            self.forceclosegl_other_btn.setText(QCoreApplication.translate("MainWindow", u"Force Close Gameloop", None))
            # if QT_CONFIG(tooltip)
            self.uninstallgl_other_btn.setToolTip(
                    QCoreApplication.translate("MainWindow", u"Completely uninstall and remove GameLoop from the system.", None))
            # endif // QT_CONFIG(tooltip)
            self.uninstallgl_other_btn.setText(QCoreApplication.translate("MainWindow", u"Uninstall Gameloop", None))
            
            # if QT_CONFIG(tooltip)
            self.gameloopsuper_other_btn.setToolTip(QCoreApplication.translate("MainWindow", u"Run Gameloop with maximum CPU, RAM and GPU priority natively.", None))
            # endif // QT_CONFIG(tooltip)
            self.gameloopsuper_other_btn.setText(QCoreApplication.translate("MainWindow", u"Gameloop Super \u26a1", None))

            # if QT_CONFIG(tooltip)
            self.drivers_other_btn.setToolTip(QCoreApplication.translate("MainWindow", u"Download and install essential drivers for the emulator (VC++ Runtime, GPU drivers).", None))
            # endif // QT_CONFIG(tooltip)
            self.drivers_other_btn.setText(QCoreApplication.translate("MainWindow", u"Essential Drivers \U0001f527", None))

            self.dns_dropdown.setItemText(0, QCoreApplication.translate("MainWindow", u"Google DNS - 8.8.8.8", None))
            self.dns_dropdown.setItemText(1,
                                          QCoreApplication.translate("MainWindow", u"Cloudflare DNS - 1.1.1.1", None))
            self.dns_dropdown.setItemText(2, QCoreApplication.translate("MainWindow", u"Quad9 DNS - 9.9.9.9", None))
            self.dns_dropdown.setItemText(3,
                                          QCoreApplication.translate("MainWindow", u"Cisco Umbrella - 208.67.222.222",
                                                                     None))
            self.dns_dropdown.setItemText(4, QCoreApplication.translate("MainWindow", u"Yandex DNS - 77.88.8.1", None))

            self.shortcut_dropdown.setItemText(0, QCoreApplication.translate("MainWindow", u"PUBG Mobile Global", None))
            self.shortcut_dropdown.setItemText(1, QCoreApplication.translate("MainWindow", u"PUBG Mobile VN", None))
            self.shortcut_dropdown.setItemText(2, QCoreApplication.translate("MainWindow", u"PUBG Mobile TW", None))
            self.shortcut_dropdown.setItemText(3, QCoreApplication.translate("MainWindow", u"PUBG Mobile KR", None))
            self.shortcut_dropdown.setItemText(4,
                                               QCoreApplication.translate("MainWindow", u"Battlegrounds Mobile India",
                                                                          None))

            self.optimizer_label.setText(QCoreApplication.translate("MainWindow", u"Optimizer", None))
            # if QT_CONFIG(tooltip)
            self.shortcut_other_btn.setToolTip(QCoreApplication.translate("MainWindow",
                                                                          u"Click here to create a shortcut for your game on the desktop",
                                                                          None))
            # endif // QT_CONFIG(tooltip)
            self.shortcut_other_btn.setText(QCoreApplication.translate("MainWindow", u"Create Shortcut", None))
            self.shortcut_label.setText(QCoreApplication.translate("MainWindow", u"Shortcut Maker", None))
            self.dns_label.setText(QCoreApplication.translate("MainWindow", u"DNS Changer", None))
            # if QT_CONFIG(tooltip)
            self.dns_other_btn.setToolTip(
                    QCoreApplication.translate("MainWindow", u"Click here to change your DNS settings", None))
            # endif // QT_CONFIG(tooltip)
            self.dns_other_btn.setText(QCoreApplication.translate("MainWindow", u"Change DNS", None))
            self.dns_status_label.setText("")
            self.ipad_label.setText(QCoreApplication.translate("MainWindow", u"IPad View", None))
            # if QT_CONFIG(tooltip)
            self.ipad_other_btn.setToolTip(
                    QCoreApplication.translate("MainWindow", u"Click here to change your DNS settings", None))
            # endif // QT_CONFIG(tooltip)
            self.ipad_other_btn.setText(QCoreApplication.translate("MainWindow", u"Change Resolution", None))
            self.ipad_dropdown.setItemText(0, QCoreApplication.translate("MainWindow", u"1920 x 1440", None))
            self.ipad_dropdown.setItemText(1, QCoreApplication.translate("MainWindow", u"1600 x 1200", None))
            self.ipad_dropdown.setItemText(2, QCoreApplication.translate("MainWindow", u"1440 x 1080", None))
            self.ipad_dropdown.setItemText(3, QCoreApplication.translate("MainWindow", u"1280 x 960", None))

            # if QT_CONFIG(tooltip)
            self.ipad_code.setToolTip(
                    QCoreApplication.translate("MainWindow", u"The layout code is provided here", None))
            # endif // QT_CONFIG(tooltip)
            self.ipad_code.setText("")
            self.ipad_code_label.setText("")
            # if QT_CONFIG(tooltip)
            self.ipad_rest_btn.setToolTip(
                    QCoreApplication.translate("MainWindow", u"Click here to change your DNS settings", None))
            # endif // QT_CONFIG(tooltip)
            self.ipad_rest_btn.setText(QCoreApplication.translate("MainWindow", u"Reset Resolution", None))
            self.label_8.setText("")
            self.about_label_text.setText(QCoreApplication.translate("MainWindow",
                                                                     u"<h2 style='color: #00EAFF; font-size: 19px; font-weight: bold;'>About Mo-Tech</h2>\n"
                                                                     "<p style='font-size: 13.5px;'>Mo-Tech is your ultimate companion for optimizing GameLoop and PUBG Mobile. It unlocks hidden potentials, forces the maximum capabilities out of your PC, and cleans the clutter for a silky-smooth experience.</p>\n"
                                                                     "\n"
                                                                     "<h3 style='color: #cba6f7; margin-top: 10px; font-size: 16px;'>Optimizer Features Explained</h3>\n"
                                                                     "<ul style='line-height: 1.5; font-size: 12.5px;'>\n"
                                                                     "  <li><b>Temp Cleaner:</b> Safely deletes junk, cache, and temporary files from your system and GameLoop to reduce lag and free up space.</li>\n"
                                                                     "  <li><b>GameLoop Optimizer:</b> Applies secret registry tweaks, network optimizations, and adds the game to Windows exclusion lists for a stutter-free experience.</li>\n"
                                                                     "  <li><b>All (Magic Button):</b> Executes both the Temp Cleaner and the GameLoop Optimizer together in one click.</li>\n"
                                                                     "  <li><b>Essential Drivers:</b> Fixes game crashes by downloading and installing missing Visual C++ runtimes and critical Windows components.</li>\n"
                                                                     "  <li><b>Force Close Gameloop:</b> Instantly terminates all frozen emulator processes, background services, and instances stuck in memory.</li>\n"
                                                                     "  <li><b>Uninstall Gameloop:</b> Completely roots out the emulator, its hidden data, and leftover registry keys as if it was never installed.</li>\n"
                                                                     "  <li><b>Gameloop Super \u26A1:</b> Launches GameLoop with the absolute highest CPU and RAM Windows priorities for VIP performance.</li>\n"
                                                                     "  <li><b>Force GPU & Optimize CPU:</b> Forces your Nvidia/AMD dedicated card to take the heavy lifting, while smartly dedicating CPU cores strictly to the game.</li>\n"
                                                                     "</ul>\n"
                                                                     "\n"
                                                                     "<h3 style='color: #cba6f7; margin-top: 10px; font-size: 16px;'>Developer</h3>\n"
                                                                     "<ul style='font-size: 12.5px;'>\n"
                                                                     "  <li><b>Name:</b> Mohammed Emad</li>\n"
                                                                     "  <li><b>Discord:</b> <a href=\"https://discord.com/users/elitemohmmad\" style=\"color: #00EAFF; text-decoration: none;\">elitemohmmad</a></li>\n"
                                                                     "  <li><b>GitHub:</b> <a href=\"https://github.com/mohammad-emad9\" style=\"color: #00EAFF; text-decoration: none;\">mohammad-emad9</a></li>\n"
                                                                     "</ul>\n"
                                                                     "                            ", None))
            self.appname_label.setText(QCoreApplication.translate("MainWindow", u"Mo-Tech pubgm", None))
            self.appstatus_label.setText(QCoreApplication.translate("MainWindow", u"Status:", None))
            self.appstatus_text_lable.setText("")
            self.close_btn.setText(QCoreApplication.translate("MainWindow", u"X", None))
            self.minimize_btn.setText(QCoreApplication.translate("MainWindow", u"-", None))
            self.gfx_button.setText(QCoreApplication.translate("MainWindow", u"GFX", None))
            self.other_button.setText(QCoreApplication.translate("MainWindow", u"Other", None))
            self.gameloop_button.setText(QCoreApplication.translate("MainWindow", u"Engine", None))
            self.about_button.setText(QCoreApplication.translate("MainWindow", u"About", None))
            
            # Engine Page Strings
            self.gl_settings_label.setText(QCoreApplication.translate("MainWindow", u"Engine Settings", None))
            self.gl_render_label.setText(QCoreApplication.translate("MainWindow", u"Screen Rendering Mode", None))
            self.gl_render_auto.setText(QCoreApplication.translate("MainWindow", u"Auto (Recommended)", None))
            self.gl_render_opengl.setText(QCoreApplication.translate("MainWindow", u"OpenGL+", None))
            self.gl_render_directx.setText(QCoreApplication.translate("MainWindow", u"DirectX+", None))
            
            self.gl_cb_render_cache.setText(QCoreApplication.translate("MainWindow", u"Enables local shader cache", None))
            self.gl_cb_force_global.setText(QCoreApplication.translate("MainWindow", u"Force global render cache", None))
            self.gl_cb_prioritize_gpu.setText(QCoreApplication.translate("MainWindow", u"Prioritize Dedicated GPU", None))
            self.gl_cb_render_opt.setText(QCoreApplication.translate("MainWindow", u"Rendering optimization", None))
            self.gl_cb_vsync.setText(QCoreApplication.translate("MainWindow", u"Vertical sync (VSync)", None))
            self.gl_cb_adb.setText(QCoreApplication.translate("MainWindow", u"Enable ADB Debugging", None))
            self.gl_cb_root.setText(QCoreApplication.translate("MainWindow", u"Root Authority", None))
            
            self.gl_label_aa.setText(QCoreApplication.translate("MainWindow", u"Anti-aliasing:", None))
            self.gl_label_mem.setText(QCoreApplication.translate("MainWindow", u"Memory:", None))
            self.gl_label_cpu.setText(QCoreApplication.translate("MainWindow", u"Processor:", None))
            self.gl_label_res.setText(QCoreApplication.translate("MainWindow", u"Resolution:", None))
            self.gl_label_dpi.setText(QCoreApplication.translate("MainWindow", u"Screen DPI:", None))
            
            self.gameloop_save_btn.setText(QCoreApplication.translate("MainWindow", u"Save Engine Settings", None))
            self.gameloop_smart_btn.setText(QCoreApplication.translate("MainWindow", u"Smart Optimize \U0001f916 AI", None))
    # retranslateUi



