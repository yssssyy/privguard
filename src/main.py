import sys
from PyQt5 import QtWidgets, QtCore  # 添加 QtCore 的导入
from PyQt5.QtGui import QPixmap
from data_provider import DataProviderScreen
from data_analyst import DataAnalystScreen

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("算力提供中心")
        self.setGeometry(100, 100, 700, 500) 
        self.background = QtWidgets.QLabel(self)
        self.background.setGeometry(0, 0, 700, 500)  # 设置背景 QLabel 尺寸与主窗口一致
        pixmap = QPixmap("/home/ys/Documents/PrivProtecter/PrivGuard/src/a.png")  # 替换为你的背景图片路径

        # 检查图片是否加载成功
        if pixmap.isNull():
            print("图片加载失败，检查路径和文件格式。")
        else:
            self.background.setPixmap(pixmap)
            self.background.setScaledContents(True)  # 让背景图自适应 QLabel 的大小

        # 创建按钮
        self.data_provider_button = QtWidgets.QPushButton("数据提供者", self)
        self.data_provider_button.setGeometry(390, 150, 200, 70)
        self.data_provider_button.setStyleSheet(
            "QPushButton { background-color: rgba(255, 255, 255, 128); }") 
        self.data_provider_button.clicked.connect(self.show_data_provider)

        self.data_analyst_button = QtWidgets.QPushButton("数据分析师", self)
        self.data_analyst_button.setGeometry(390, 250, 200, 70)
        self.data_analyst_button.setStyleSheet(
            "QPushButton { background-color: rgba(255, 255, 255, 128); }")
        self.data_analyst_button.clicked.connect(self.show_data_analyst)

   
        self.welcome_label = QtWidgets.QLabel("请选择您的身份", self)
        self.welcome_label.setGeometry(350, 0, 300, 150)
        self.welcome_label.setAlignment(QtCore.Qt.AlignCenter)
        self.welcome_label.setStyleSheet("QLabel { font-size: 16pt; color: grey;}")

    def show_data_provider(self):
        self.provider_screen = DataProviderScreen()
        self.provider_screen.show()
        self.close()  # 关闭主界面

    def show_data_analyst(self):
        self.analyst_screen = DataAnalystScreen()
        self.analyst_screen.show()
        self.close()  # 关闭主界面

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

