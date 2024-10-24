from PyQt5 import QtWidgets, QtCore
import os
import pandas as pd
import subprocess  # 用于运行外部脚本


class DataProviderScreen(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("数据提供者界面")
        self.setGeometry(100, 100, 600, 400)  # 调整窗口大小

        # 主布局
        main_layout = QtWidgets.QVBoxLayout()
        main_layout.setSpacing(15)  # 设置控件之间的间距
        main_layout.setContentsMargins(20, 20, 20, 20)  # 设置边距

        # 创建水平布局来放置文本框和按钮
        file_selection_layout = QtWidgets.QHBoxLayout()

        # 文件选择框（只读）
        self.file_name_edit = QtWidgets.QLineEdit()
        self.file_name_edit.setPlaceholderText("选择的文件名...")
        self.file_name_edit.setReadOnly(True)  # 只读，用户不能输入
        file_selection_layout.addWidget(self.file_name_edit)

        # 文件选择按钮
        self.select_file_button = QtWidgets.QPushButton("选择文件")
        self.select_file_button.clicked.connect(self.select_file)
        file_selection_layout.addWidget(self.select_file_button)

        main_layout.addLayout(file_selection_layout)

        # 上传文件按钮（移动到分析目标框上方）
        self.upload_button = QtWidgets.QPushButton("上传文件")
        self.upload_button.clicked.connect(self.upload_file)
        main_layout.addWidget(self.upload_button)

        # 输入分析目标文本框
        self.analysis_target_entry = QtWidgets.QLineEdit()
        self.analysis_target_entry.setPlaceholderText("请输入分析目标...")  # 占位文本
        main_layout.addWidget(self.analysis_target_entry)

        # 确认输入分析目标按钮
        self.confirm_target_button = QtWidgets.QPushButton("确认输入分析目标")
        self.confirm_target_button.clicked.connect(self.save_analysis_target)
        main_layout.addWidget(self.confirm_target_button)

        # 输出策略文本框
        self.policy_entry = QtWidgets.QTextEdit()
        self.policy_entry.setPlaceholderText("请输入策略文本...")  # 可选：占位文本
        main_layout.addWidget(self.policy_entry)

        # 确认按钮
        self.confirm_button = QtWidgets.QPushButton("确认保存策略")
        self.confirm_button.clicked.connect(self.save_policy)
        main_layout.addWidget(self.confirm_button)

        # 查看分析结果按钮
        self.view_results_button = QtWidgets.QPushButton("查看分析结果")
        self.view_results_button.clicked.connect(self.check_results)
        main_layout.addWidget(self.view_results_button)

        # 设置主布局
        self.setLayout(main_layout)

    def select_file(self):
        options = QtWidgets.QFileDialog.Options()
        file_name, _ = QtWidgets.QFileDialog.getOpenFileName(self, "选择文件", "", "CSV 文件 (*.csv);;所有文件 (*)",
                                                             options=options)

        if file_name:
            self.file_name_edit.setText(file_name)  # 显示选择的文件名

    def upload_file(self):
        file_name = self.file_name_edit.text().strip()  # 从文本框中获取文件名
        if file_name and os.path.exists(file_name):
            # 将文件移动到当前工作目录
            destination_path = os.path.join(os.getcwd(), os.path.basename(file_name))
            os.rename(file_name, destination_path)

            # 读取 CSV 文件并提取列名和行数
            self.write_csv_info_to_txt(destination_path)

            # 在命令行中运行 python enc.py
            try:
                subprocess.run(["python", "enc.py"], check=True)
                QtWidgets.QMessageBox.information(self, "成功", f"文件已成功上传并加密")
            except subprocess.CalledProcessError as e:
                QtWidgets.QMessageBox.critical(self, "错误", f"执行 enc.py 失败: {e}")
        else:
            QtWidgets.QMessageBox.warning(self, "警告", "请先选择一个有效的文件。")

    def write_csv_info_to_txt(self, csv_file_path):
        try:
            # 读取 CSV 文件
            df = pd.read_csv(csv_file_path)

            # 获取所有列名
            column_names = df.columns.tolist()

            # 将列名和行数写入 TXT 文件
            txt_file_path = os.path.join(os.getcwd(),
                                         '/home/ys/Documents/PrivProtecter/PrivGuard/src/examples/data/cssjj/meta.txt')  # 输出 TXT 文件路径
            with open(txt_file_path, 'w') as f:
                # 写入列名，以逗号分隔
                f.write(','.join(column_names) + '\n')  # 列名在第一行
                # 写入行数
                row_count = len(df)  # 获取行数
                f.write(f"{row_count}\n")  # 行数在第二行

        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "错误", f"读取文件失败: {str(e)}")

    def save_policy(self):
        policy_text = self.policy_entry.toPlainText().strip()
        if policy_text:
            policy_file_path = "/home/ys/Documents/PrivProtecter/PrivGuard/src/examples/data/cssjj/policy.txt"  # 保存策略文件的路径
            with open(policy_file_path, 'w') as file:  # 以写入模式打开文件（覆盖）
                file.write(policy_text)  # 写入策略文本
            QtWidgets.QMessageBox.information(self, "成功", "策略已保存到文件。")
            self.policy_entry.clear()  # 清空策略文本框
        else:
            QtWidgets.QMessageBox.warning(self, "警告", "请输入策略文本。")

    def save_analysis_target(self):
        analysis_target = self.analysis_target_entry.text().strip()
        if analysis_target:
            target_file_path = "/home/ys/Documents/PrivProtecter/PrivGuard/src/examples/data/cssjj/analyse_purpose.txt"  # 保存分析目标的路径
            with open(target_file_path, 'w') as file:  # 以写入模式打开文件（覆盖）
                file.write(analysis_target)  # 写入分析目标文本
            QtWidgets.QMessageBox.information(self, "成功", "分析目标已保存到文件。")
            self.analysis_target_entry.clear()  # 清空分析目标文本框
        else:
            QtWidgets.QMessageBox.warning(self, "警告", "请输入分析目标。")

    def check_results(self):
        result_file_path = os.path.join(os.getcwd(),
                                        '/home/ys/Documents/PrivProtecter/PrivGuard/src/mult_result.bin')  # 结果文件路径
        if os.path.exists(result_file_path):
            reply = QtWidgets.QMessageBox.question(self, "分析结果", "发现结果文件，是否需要解密结果？",
                                                   QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                                   QtWidgets.QMessageBox.No)
            if reply == QtWidgets.QMessageBox.Yes:
                # 运行解密脚本
                command = ["python", "dec.py"]
                subprocess.run(command, check=True)
                csv_file_path = "result.csv"  # 可以根据实际路径修改

                # 检查CSV文件是否存在
                if os.path.exists(csv_file_path):
                    # 使用xdg-open打开result.csv
                    subprocess.run(["xdg-open", csv_file_path], check=False)
                else:
                    QtWidgets.QMessageBox.warning(self, "警告", f"结果文件未找到: {csv_file_path}")

        else:
            QtWidgets.QMessageBox.information(self, "信息", "未找到分析结果文件 result.bin。")


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    window = DataProviderScreen()
    window.show()
    sys.exit(app.exec_())

