from PyQt5 import QtWidgets, QtCore, QtGui
import os
import subprocess
import re  # 引入正则表达式库

# 定义保存文件的完整路径
SAVE_FILE = '/home/ys/Documents/PrivProtecter/PrivGuard/src/examples/program/24_MedicalDataAnalysis.py'

# 确保保存目录存在
SAVE_DIR = os.path.dirname(SAVE_FILE)  # 获取文件的目录
if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)

class DataAnalystScreen(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("数据分析师界面")
        self.setGeometry(100, 100, 500, 500)  # 增加窗口大小

        # 创建“分析目标”标签并读取文件内容
        self.analysis_target_label = QtWidgets.QLabel("分析目标为：", self)
        self.analysis_target_label.setGeometry(50, 20, 400, 30)
        self.analysis_target_label.setFont(QtGui.QFont("Arial", 12))  # 设置标签字体大小
        self.load_analysis_target()  # 加载分析目标

        # 创建“分析程序”标签
        analysis_label = QtWidgets.QLabel("分析程序：", self)
        analysis_label.setGeometry(50, 60, 120, 30)
        analysis_label.setFont(QtGui.QFont("Arial", 12))  # 设置标签字体大小

        # 创建文本框
        self.text_entry = QtWidgets.QTextEdit(self)
        self.text_entry.setGeometry(50, 100, 400, 150)  # 调整文本框大小
        self.text_entry.setPlaceholderText("请输入分析程序...")  # 提示信息
        self.text_entry.setFont(QtGui.QFont("Arial", 10))  # 设置输入框字体大小

        # 创建保存按钮
        save_button = QtWidgets.QPushButton("保存程序并检测", self)
        save_button.setGeometry(150, 270, 200, 40)  # 调整按钮大小
        save_button.setFont(QtGui.QFont("Arial", 12))  # 设置按钮字体大小
        save_button.clicked.connect(self.save_and_execute)

        # 创建“检测结果”标签
        result_label = QtWidgets.QLabel("检测结果：", self)
        result_label.setGeometry(50, 320, 120, 30)
        result_label.setFont(QtGui.QFont("Arial", 12))  # 设置标签字体大小

        # 创建输出框
        self.output_display = QtWidgets.QTextEdit(self)
        self.output_display.setGeometry(50, 350, 400, 100)  # 调整输出框大小
        self.output_display.setReadOnly(True)  # 设置为只读

    def load_analysis_target(self):
        # 从文件中读取分析目标
        target_file_path = '/home/ys/Documents/PrivProtecter/PrivGuard/src/examples/data/cssjj/analyse_purpose.txt'
        if os.path.exists(target_file_path):
            with open(target_file_path, 'r') as file:
                target_value = file.read().strip()  # 读取内容并去除多余空白
                if target_value:
                    self.analysis_target_label.setText(f"分析目标为：{target_value}")  # 更新标签文本
                else:
                    self.analysis_target_label.setText("分析目标为：未找到目标")  # 若文件为空

    def save_and_execute(self):
        text = self.text_entry.toPlainText().strip()  # 获取文本框的内容
        if text:  # 检查文本框是否为空
            with open(SAVE_FILE, 'w') as file:  # 以写入模式打开文件
                file.write(text + "\n")  # 写入文本
            
            # 执行命令并获取结果
            command = ["python", "analyze.py", "--example_id", "24"]
            try:
                result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                output = result.stdout + result.stderr  # 获取输出和错误信息
                
                # 使用正则表达式提取所需部分
                match = re.search(r'Residual policy of the output:\n(.*)', output, re.DOTALL)
                if match:
                    extracted_output = match.group(0)  # 包含"Residual policy of the output:"和提取的内容
                    self.output_display.setPlainText(extracted_output.strip())  # 显示提取的输出

                    # 检查输出中是否包含 "(SAT)" 字符串
                    if "(SAT)" in output:
                        # 执行另一个脚本
                        subprocess.run(["python", "cul.py"], check=True)
                        self.output_display.append("\n分析程序检测合规已执行")
                        
                else:
                    self.output_display.setPlainText("程序有误")  # 提示信息

                QtWidgets.QMessageBox.information(self, "成功", "文本已保存并执行。")
                # self.text_entry.clear()  # 可选: 清空文本框
            except Exception as e:
                QtWidgets.QMessageBox.critical(self, "错误", f"执行命令失败：{str(e)}")
        else:
            QtWidgets.QMessageBox.warning(self, "警告", "请输入一些文本。")

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = DataAnalystScreen()
    window.show()
    sys.exit(app.exec_())

