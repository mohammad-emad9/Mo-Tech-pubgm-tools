from PyQt5 import QtCore, QtGui, QtWidgets
from .app_functions import Game
from .gfx import GFX
from .other import Other
from .ui import Ui_MainWindow


class AnimatedToggle(QtWidgets.QCheckBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setCursor(QtCore.Qt.PointingHandCursor)
        self.setMinimumHeight(28)
        self._offset = 3.0
        self._pulse = 0.0
        self._anim = QtCore.QPropertyAnimation(self, b"offset", self)
        self._anim.setDuration(180)
        self._anim.setEasingCurve(QtCore.QEasingCurve.InOutCubic)
        self._pulse_anim = QtCore.QPropertyAnimation(self, b"pulse", self)
        self._pulse_anim.setDuration(180)
        self._pulse_anim.setStartValue(0.0)
        self._pulse_anim.setEndValue(1.0)
        self._pulse_anim.setEasingCurve(QtCore.QEasingCurve.OutCubic)
        self.toggled.connect(self._animate_toggle)

    @QtCore.pyqtProperty(float)
    def offset(self):
        return self._offset

    @offset.setter
    def offset(self, value):
        self._offset = value
        self.update()

    @QtCore.pyqtProperty(float)
    def pulse(self):
        return self._pulse

    @pulse.setter
    def pulse(self, value):
        self._pulse = value
        self.update()

    def _animate_toggle(self, checked):
        end = 23.0 if checked else 3.0
        self._anim.stop()
        self._anim.setStartValue(self._offset)
        self._anim.setEndValue(end)
        self._anim.start()
        self._pulse_anim.stop()
        self._pulse_anim.start()

    def paintEvent(self, _event):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        text_rect = QtCore.QRect(52, 0, self.width() - 52, self.height())
        track_rect = QtCore.QRectF(0, (self.height() - 22) / 2, 44, 22)
        knob_rect = QtCore.QRectF(self._offset, (self.height() - 18) / 2, 18, 18)

        track_color = QtGui.QColor("#00EAFF") if self.isChecked() else QtGui.QColor("#3C4049")
        painter.setPen(QtGui.QPen(QtGui.QColor("#555A66"), 1))
        painter.setBrush(track_color)
        painter.drawRoundedRect(track_rect, 11, 11)

        if self._pulse > 0 and self.isChecked():
            glow = QtGui.QColor("#00EAFF")
            glow.setAlpha(int(70 * (1 - self._pulse)))
            painter.setPen(QtCore.Qt.NoPen)
            painter.setBrush(glow)
            painter.drawEllipse(QtCore.QRectF(knob_rect.x() - 4, knob_rect.y() - 4, 26, 26))

        painter.setPen(QtCore.Qt.NoPen)
        painter.setBrush(QtGui.QColor("#F5F7FA"))
        painter.drawEllipse(knob_rect)
        painter.setPen(QtGui.QColor("#EAEAEA"))
        painter.drawText(text_rect, QtCore.Qt.AlignVCenter | QtCore.Qt.AlignLeft, self.text())


class Window(QtWidgets.QMainWindow, Game):
    def __init__(self, app_name, app_version):
        # Remove the default title bar
        super(Window, self).__init__()
        self.app_name = app_name
        self.app_version = app_version

        self.setWindowFlag(QtCore.Qt.WindowType.FramelessWindowHint)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.appname_label.setText(f"{app_name} {app_version}")
        self.timer = None
        self._animations = []
        self._hover_anims = {}
        self._setup_micro_interactions()

        # Set up the GFX and Other objects
        self.GFX = GFX(self)
        self.Other = Other(self)
        
        from .gameloop_settings_ui import GameloopSettingsUI
        self.GameloopSettings = GameloopSettingsUI(self)

        # Initialize variables for dragging
        self.draggable = True
        self.drag_start_position = None

        # Connect the button signals
        self.ui.gfx_button.clicked.connect(lambda: self.buttonClicked(self.ui.gfx_button, self.ui.gfx_page))
        self.ui.other_button.clicked.connect(lambda: self.buttonClicked(self.ui.other_button, self.ui.other_page))
        self.ui.gameloop_button.clicked.connect(lambda: self.buttonClicked(self.ui.gameloop_button, self.ui.gameloop_page))
        self.ui.about_button.clicked.connect(lambda: self.buttonClicked(self.ui.about_button, self.ui.about_page, ))
        self.ui.close_btn.clicked.connect(lambda: self.close())
        self.ui.minimize_btn.clicked.connect(lambda: self.setWindowState(QtCore.Qt.WindowState.WindowMinimized))

    def buttonClicked(self, button, page):
        self.ui.gfx_button.setChecked(button == self.ui.gfx_button)
        self.ui.other_button.setChecked(button == self.ui.other_button)
        self.ui.gameloop_button.setChecked(button == self.ui.gameloop_button)
        self.ui.about_button.setChecked(button == self.ui.about_button)
        self.ui.stackedWidget.setCurrentWidget(page)
        self._animate_page_transition(page)

    def _animate_page_transition(self, page):
        effect = QtWidgets.QGraphicsOpacityEffect(page)
        page.setGraphicsEffect(effect)
        anim = QtCore.QPropertyAnimation(effect, b"opacity", self)
        anim.setDuration(180)
        anim.setStartValue(0.15)
        anim.setEndValue(1.0)
        anim.setEasingCurve(QtCore.QEasingCurve.InOutQuad)
        anim.finished.connect(lambda: page.setGraphicsEffect(None))
        anim.start()
        self._animations.append(anim)
        if len(self._animations) > 8:
            self._animations = self._animations[-8:]

    def _setup_micro_interactions(self):
        self._apply_sidebar_icons()
        self._install_hover_glow()
        self._upgrade_toggles()

    def _apply_sidebar_icons(self):
        icon_map = {
            self.ui.gfx_button: self.style().standardIcon(QtWidgets.QStyle.SP_ComputerIcon),
            self.ui.other_button: self.style().standardIcon(QtWidgets.QStyle.SP_DriveHDIcon),
            self.ui.gameloop_button: self.style().standardIcon(QtWidgets.QStyle.SP_CommandLink),
            self.ui.about_button: self.style().standardIcon(QtWidgets.QStyle.SP_MessageBoxInformation),
        }
        for button, icon in icon_map.items():
            button.setIcon(icon)
            button.setIconSize(QtCore.QSize(20, 20))
            button.setStyleSheet(button.styleSheet() + "QPushButton { text-align: left; padding-left: 14px; }")

    def _install_hover_glow(self):
        glow_buttons = [
            self.ui.gfx_button, self.ui.other_button, self.ui.gameloop_button, self.ui.about_button,
            self.ui.submit_gfx_btn, self.ui.connect_gameloop_btn, self.ui.gameloop_save_btn, self.ui.gameloop_smart_btn,
            self.ui.tempcleaner_other_btn, self.ui.gloptimizer_other_btn,
            self.ui.shortcut_other_btn, self.ui.dns_other_btn, self.ui.ipad_other_btn,
        ]
        for btn in glow_buttons:
            shadow = QtWidgets.QGraphicsDropShadowEffect(btn)
            shadow.setOffset(0, 0)
            shadow.setBlurRadius(0)
            shadow.setColor(QtGui.QColor(0, 234, 255, 0))
            btn.setGraphicsEffect(shadow)
            btn.installEventFilter(self)
            self._hover_anims[btn] = shadow

    def _upgrade_toggles(self):
        toggle_names = [
            "gl_cb_render_cache", "gl_cb_prioritize_gpu", "gl_cb_vsync", "gl_cb_root",
            "gl_cb_force_global", "gl_cb_render_opt", "gl_cb_adb"
        ]
        for name in toggle_names:
            old = getattr(self.ui, name, None)
            if not old:
                continue
            parent = old.parentWidget()
            new_toggle = AnimatedToggle(parent)
            new_toggle.setObjectName(old.objectName())
            new_toggle.setGeometry(old.geometry())
            new_toggle.setFont(old.font())
            new_toggle.setText(old.text())
            new_toggle.setToolTip(old.toolTip())
            new_toggle.setChecked(old.isChecked())
            old.deleteLater()
            setattr(self.ui, name, new_toggle)

    def eventFilter(self, obj, event):
        if obj in self._hover_anims:
            effect = self._hover_anims[obj]
            if event.type() == QtCore.QEvent.Enter:
                self._animate_glow(effect, 24, 130)
            elif event.type() == QtCore.QEvent.Leave:
                self._animate_glow(effect, 0, 0)
        return super().eventFilter(obj, event)

    def _animate_glow(self, effect, blur_radius, alpha):
        blur = QtCore.QPropertyAnimation(effect, b"blurRadius", self)
        blur.setDuration(180)
        blur.setEndValue(blur_radius)
        blur.setEasingCurve(QtCore.QEasingCurve.InOutCubic)
        blur.start()

        # Color fade is done with stepped timer to avoid a custom QProperty wrapper.
        start_alpha = effect.color().alpha()
        steps = 8
        delta = (alpha - start_alpha) / steps
        for i in range(steps):
            QtCore.QTimer.singleShot(
                i * 20,
                lambda i=i: effect.setColor(QtGui.QColor(0, 234, 255, int(start_alpha + delta * (i + 1))))
            )
        self._animations.append(blur)

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton and self.draggable:
            # Drag window only from the custom title bar region.
            local_pos = event.pos()
            if hasattr(self.ui, "title_bar") and self.ui.title_bar.geometry().contains(local_pos):
                self.drag_start_position = event.globalPos()
            else:
                self.drag_start_position = None

    def mouseMoveEvent(self, event):
        if self.draggable and self.drag_start_position is not None:
            if event.buttons() & QtCore.Qt.LeftButton:
                self.move(self.pos() + event.globalPos() - self.drag_start_position)
                self.drag_start_position = event.globalPos()

    def mouseReleaseEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.drag_start_position = None

    def show_status_message(self, message, duration=5):
        """Displays a message on the status label for a specified duration."""
        try:
            if hasattr(self, 'status_timer') and self.status_timer and self.status_timer.isActive():
                self.status_timer.stop()
            
            self.ui.appstatus_text_lable.setText(str(message))
            
            self.status_timer = QtCore.QTimer(self)
            self.status_timer.setSingleShot(True)
            self.status_timer.timeout.connect(lambda: self.ui.appstatus_text_lable.setText(""))
            self.status_timer.start(duration * 1000)
        except Exception:
            self.ui.appstatus_text_lable.setText(str(message))