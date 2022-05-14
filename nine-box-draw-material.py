import random
import time

from PySide2.QtWidgets import *
from functools import partial
from qt_material import apply_stylesheet, list_themes, QtStyleTools
from JasonUI.buttons import DarkerButton


class NineBoxDraw(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.order = [(0, 0), (0, 1), (0, 2), (1, 2), (2, 2), (2, 1), (2, 0), (1, 0)]
        self.current_position = 0
        self.buttons = [[QPushButton("奖品") for j in range(3)] for i in range(9)]
        self.buttons[1][1] = DarkerButton()
        self.buttons[1][1].setStyleSheet(self.buttons[1][1].styleSheet() + "\nQPushButton{color: gray;}")
        self.buttons[1][1].setText("抽奖！")
        self.buttons[1][1].setFixedSize(100, 100)
        self.buttons[1][1].clicked.connect(self.draw)
        self.grid = QGridLayout(self)
        for line in range(3):
            for col in range(3):
                self.grid.addWidget(self.buttons[line][col], line, col)
        for (row, col) in self.order:
            self.buttons[row][col].clicked.connect(partial(self.on_text_edit, row, col))
            self.buttons[row][col].setFixedSize(100, 100)

    def on_text_edit(self, row, col):
        d = EditDialog(row, col, self)
        d.show()

    def draw(self):
        index = self.current_position
        row, col = self.order[index]
        self.buttons[row][col].setStyleSheet(self.buttons[row][col].styleSheet().rstrip("\nQPushButton{"
                                                                                        "background-color: pink;}"))
        stop_point = random.randint(1, 8)
        for i in range(self.current_position, 50+stop_point):
            index = i % 8;
            row, col = self.order[index]
            button_to_shine = self.buttons[row][col]
            button_to_shine.setStyleSheet(button_to_shine.styleSheet() + "\nQPushButton{background-color: pink;}")
            QApplication.processEvents()
            if 0.2 - i*0.01 >= 0.03:
                time.sleep(0.2 - i*0.01)
            elif 50+stop_point - i <= 12:
                time.sleep(0.03+(12 - 50+stop_point + i)*0.01)
            else:
                time.sleep(0.03)
            if i != 50+stop_point - 1:
                button_to_shine.setStyleSheet(button_to_shine.styleSheet().rstrip("\nQPushButton{background-color: pink;}"))
        self.current_position = i % 8


class EditDialog(QDialog):
    def __init__(self, row, col, parent=None):
        super().__init__(parent)
        self.coordinates = (row, col)
        self.vbox = QVBoxLayout(self)
        self.label = QLabel("请输入奖品名称：")
        self.line_edit = QLineEdit(self)
        self.btn = QPushButton("确定")
        self.btn.clicked.connect(self.quit)
        self.vbox.addWidget(self.label)
        self.vbox.addWidget(self.line_edit)
        self.vbox.addWidget(self.btn)

    def quit(self):
        self.parentWidget().buttons[self.coordinates[0]][self.coordinates[1]].setText(self.line_edit.text())
        self.close()


class SelectBatchDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.vbox = QVBoxLayout(self)
        self.label = QLabel("在这里批量添加奖品名称，一行一个奖品，共八个，从左上角开始顺时针顺序")
        self.text_edit = QTextEdit(self)
        self.submit = QPushButton("确定")
        self.vbox.addWidget(self.label)
        self.vbox.addWidget(self.text_edit)
        self.vbox.addWidget(self.submit)
        self.submit.clicked.connect(self.submit_names)

    def submit_names(self):
        text = self.text_edit.toPlainText().strip().split('\n')
        for index in range(8):
            w = self.parentWidget().w
            row, col = w.order[index]
            w.buttons[row][col].setText(text[index].strip())
        self.close()


class AboutDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.vbox = QVBoxLayout(self)
        self.label = QLabel("这是关于作者、本程序，以及本程序的使用条款")
        self.text_edit = QTextEdit(self)
        self.text_edit.setText("本程序的作者是河北省保定市的一名中学生，"
                               "欢迎通过jasoncoder@qq.com与作者联系，或进行关于编程问题的交流探讨。\n"
                               "这个程序受版权保护，不得随意进行修改。未经作者同意，不得商用。\n"
                               "这个程序完全免费。")
        self.text_edit.setReadOnly(True)
        self.submit = QPushButton("我已阅读")
        self.vbox.addWidget(self.label)
        self.vbox.addWidget(self.text_edit)
        self.vbox.addWidget(self.submit)


class MainWindow(QMainWindow, QtStyleTools):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("九宫格抽奖程序")
        self.w = NineBoxDraw(self)
        self.setCentralWidget(self.w)
        self.menu = self.menuBar()
        self.more_menu = self.menu.addMenu("更多……")
        self.add_more = self.more_menu.addAction("批量添加奖品名称")
        self.add_more.triggered.connect(self.select_names)
        self.themes_menu = self.more_menu.addMenu("设置程序外观")
        self.about = self.more_menu.addAction("关于")
        self.about.triggered.connect(self.about_toggled)
        self.ac = []
        t = list_themes() + ['default']
        for theme_name in t:
            act = self.themes_menu.addAction(theme_name)
            act.triggered.connect(partial(self.set_theme, theme_name, t.index(theme_name)))
            act.setCheckable(True)
            self.ac.append(act)
        self.ac[-1].setChecked(True)
        self.checked_index = len(t) - 1

    def select_names(self):
        d = SelectBatchDialog(self)
        d.show()

    def set_theme(self, theme_name, index):
        self.apply_stylesheet(self, theme_name)
        self.ac[self.checked_index].setChecked(False)
        self.checked_index = index

    def about_toggled(self):
        d = AboutDialog(self)
        d.show()


app = QApplication([])
window = MainWindow()

# setup stylesheet
extra = {

    # Button colors
    'danger': '#dc3545',
    'warning': '#ffc107',
    'success': '#17a2b8',
}
apply_stylesheet(app, theme='default', extra=extra)

# run
window.show()
app.exec_()