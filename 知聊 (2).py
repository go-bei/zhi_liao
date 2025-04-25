# -*- coding: utf-8 -*-
from PyQt6.QtCore import Qt, QRect, pyqtSignal
from PyQt6.QtGui import QPixmap, QFont
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtGui import QTextBlockFormat, QTextCursor
import socket
import threading
from sjk import DbM

class Ui_zhi_liao(object):
    def setupUi(self, zhi_liao):
        zhi_liao.setObjectName("zhi_liao")
        zhi_liao.resize(1272, 744)
        
        # 装饰按钮（保持原状）
        self.zhuang_shi = QtWidgets.QPushButton(parent=zhi_liao)
        self.zhuang_shi.setGeometry(QtCore.QRect(1160, 150, 81, 261))
        self.zhuang_shi.setStyleSheet("""
        QPushButton {
            border: 2px solid #CCCCCC;    
            border-radius: 10px;         
            padding: 5px;                
            background-color: rgba(1, 1, 1, 50);  
            border: none;                         
            color: black;                         
            font-family: "宋体";               
            font-size: 14px;                      
            font-weight: bold;                    
        }""")

        # 功能按钮组（保持原有样式）
        button_style = """
        QPushButton {
            border: 2px solid #CCCCCC;    
            border-radius: 10px;         
            padding: 5px;                
            background-color: rgba(0, 0, 0, 80);  
            border: none;                         
            color: white;                         
            font-family: "宋体";               
            font-size: 14px;                      
            font-weight: bold;                    
        }
        QPushButton:hover {
            color: white;                           
            font-size: 16px;                      
        }
        QPushButton:pressed {
            color: #0066CC;                       
            font-size: 14px;                      
        }"""
        
        self.yong_hu_xin_xi = QtWidgets.QPushButton(parent=zhi_liao)
        self.yong_hu_xin_xi.setGeometry(QtCore.QRect(1170, 170, 61, 41))
        self.yong_hu_xin_xi.setStyleSheet(button_style)
        
        self.li_shi = QtWidgets.QPushButton(parent=zhi_liao)
        self.li_shi.setGeometry(QtCore.QRect(1170, 230, 61, 41))
        self.li_shi.setStyleSheet(button_style)
        
        self.she_zhi = QtWidgets.QPushButton(parent=zhi_liao)
        self.she_zhi.setGeometry(QtCore.QRect(1170, 290, 61, 41))
        self.she_zhi.setStyleSheet(button_style)
        
        self.bang_zhu = QtWidgets.QPushButton(parent=zhi_liao)
        self.bang_zhu.setGeometry(QtCore.QRect(1170, 350, 61, 41))
        self.bang_zhu.setStyleSheet(button_style)

        # 在线列表区域（增强显示效果）
        self.zai_xian_list = QtWidgets.QLabel(parent=zhi_liao)
        self.zai_xian_list.setGeometry(QtCore.QRect(0, 0, 251, 711))
        self.zai_xian_list.setStyleSheet("""
        QLabel {
            background-color: rgba(0, 0, 0, 50);
            color: #00FF00;
            padding: 35px 25px;
            border: none;
            font-family: "宋体";
            font-size: 14px;
            qproperty-alignment: AlignTop;
        }""")
        self.zai_xian_list.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.zai_xian_list.setWordWrap(True)
        # 消息显示区域（优化显示效果）
        self.shu_chu = QtWidgets.QTextBrowser(parent=zhi_liao)  # 改用QTextBrowser支持滚动条
        self.shu_chu.setGeometry(QtCore.QRect(360, 10, 791, 511))
        self.shu_chu.setStyleSheet("""
QTextBrowser {
    background-color: rgba(0, 0, 0, 0);
    color: white;
    border-radius: 10px;
    padding: 20px;
    font-family: "宋体";
    font-size: 18px;
}

/* 垂直滚动条整体 */
QScrollBar:vertical {
    background: rgba(200, 200, 200, 0);
    width: 12px;
    margin: 15px 0 15px 0;
}

/* 水平滚动条整体 */
QScrollBar:horizontal {
    background: rgba(200, 200, 200, 0);
    height: 12px;
    margin: 0 15px 0 15px;
}

/* 滚动条手柄 */
QScrollBar::handle:vertical {
    background: rgba(255, 255, 255, 50);
    min-height: 30px;
    border-radius: 6px;
}

QScrollBar::handle:horizontal {
    background: rgba(255, 255, 255, 150);
    min-width: 30px;
    border-radius: 6px;
}

/* 滚动条悬停效果 */
QScrollBar::handle:hover {
    background: rgba(255, 255, 255, 200);
}

/* 滚动条上下按钮 */
QScrollBar::add-line:vertical, 
QScrollBar::sub-line:vertical {
    background: none;
}

QScrollBar::add-line:horizontal,
QScrollBar::sub-line:horizontal {
    background: none;
}

/* 滚动条背景角 */
QScrollBar::add-page:vertical, 
QScrollBar::sub-page:vertical,
QScrollBar::add-page:horizontal, 
QScrollBar::sub-page:horizontal {
    background: none;
}
""")
        self.shu_chu.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)

        # 输入区域（增加输入提示）
        self.textEdit = QtWidgets.QTextEdit(parent=zhi_liao)
        self.textEdit.setGeometry(QtCore.QRect(340, 590, 801, 91))
        self.textEdit.setStyleSheet("""
        QTextEdit {
            border: 2px solid #CCCCCC;    
            border-radius: 10px;         
            padding: 20px;                
            background-color: rgba(0, 0, 0, 80);  
            border: none;                        
            color: white;   
            font-family: "宋体";    
            font-size: 18px;                      
            font-weight: bold;   
}


/* 垂直滚动条整体 */
QScrollBar:vertical {
    width: 12px;        /* 滚动条宽度 */
    margin: 0;          /* 关键：消除边缘间距 */
    background: transparent;
}



/* 彻底隐藏所有箭头按钮 */
QScrollBar::up-arrow:vertical, 
QScrollBar::down-arrow:vertical,
QScrollBar::left-arrow:horizontal,
QScrollBar::right-arrow:horizontal {
    border: none;
    background: none;
    width: 0;
    height: 0;
}

/* 消除按钮占位空间 */
QScrollBar::add-line:vertical, 
QScrollBar::sub-line:vertical {
    subcontrol-origin: margin;  /* 关键：基于外边距定位 */
    subcontrol-position: top;   /* 强制定位到边缘 */
    height: 0;                  /* 消除高度占位 */
}

QScrollBar::add-line:horizontal,
QScrollBar::sub-line:horizontal {
    subcontrol-origin: margin;
    subcontrol-position: left;
    width: 0;                  /* 消除宽度占位 */
}

/* 手柄样式定制 */
QScrollBar::handle:vertical {
    min-height: 30px;
    background: rgba(255,255,255,0);
    border-radius: 6px;
    margin: 0 2px;            /* 两侧留出呼吸空间 */
}

QScrollBar::handle:horizontal {
    min-width: 30px;
    background: rgba(0,0,0,0.3);
    border-radius: 6px;
    margin: 2px 0;
}
""")
        
        self.textEdit.setPlaceholderText("输入消息...")

        # 发送按钮（增加图标）
        self.fa_song = QtWidgets.QPushButton(parent=zhi_liao)
        self.fa_song.setGeometry(QtCore.QRect(1020, 540, 121, 41))
        self.fa_song.setStyleSheet(button_style)
        self.fa_song.setIcon(QtGui.QIcon("send_icon.png"))
        self.fa_song.setIconSize(QtCore.QSize(20, 20))

        self.bei_jing = QtWidgets.QLabel(parent=zhi_liao)
        self.bei_jing.setGeometry(QtCore.QRect(0, -40, 1271, 751))
        try:
            # 尝试加载背景图片
            self.bei_jing.setPixmap(QtGui.QPixmap("D:/图片/  (1).png"))
        except:
            # 图片加载失败时设置纯色背景
            self.bei_jing.setStyleSheet("background-color: #2D2D2D;")
        self.bei_jing.setScaledContents(True)

        self.retranslateUi(zhi_liao)
        QtCore.QMetaObject.connectSlotsByName(zhi_liao)
        self.bei_jing.lower()  # 背景置于底层

    def retranslateUi(self, zhi_liao):
        _translate = QtCore.QCoreApplication.translate
        zhi_liao.setWindowTitle(_translate("zhi_liao", "知聊 - 在线聊天室"))
        self.she_zhi.setText(_translate("zhi_liao", "设置"))
        self.bang_zhu.setText(_translate("zhi_liao", "帮助"))
        self.yong_hu_xin_xi.setText(_translate("zhi_liao", "用户"))
        self.li_shi.setText(_translate("zhi_liao", "历史"))
        self.fa_song.setText(_translate("zhi_liao", "发送"))
        self.zai_xian_list.setText(_translate("zhi_liao", "在线用户\n-----------"))
        self.shu_chu.setPlaceholderText(_translate("zhi_liao", "消息记录将在此显示..."))

class ChatWindow(QtWidgets.QDialog, Ui_zhi_liao):
    update_signal = pyqtSignal(str)  

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.client = None
        self.running = True
        self.username = None  

        # 网络初始化
        self.client = None
        self.running = True
        self.connect_server()

        # 连接信号
        self.fa_song.clicked.connect(self.send_message)
        self.textEdit.installEventFilter(self)  # 回车发送支持
        self.update_signal.connect(self.update_display)
        
    def connect_server(self):
        """连接服务器并初始化"""
        try:
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client.connect(('127.0.0.1',12345))
        
            # 获取用户名
            username, ok = QtWidgets.QInputDialog.getText(
                self, '用户登录', '请输入您的昵称:',
                QtWidgets.QLineEdit.EchoMode.Normal, 
                text="匿名用户"
            )
            god = username
            if not ok or not username.strip():
                username = "匿名用户"
            
            self.client.send(username.encode('utf-8'))
            self.load_recent_messages()  # 加载历史消息
            # 启动接收线程
            self.recv_thread = threading.Thread(target=self.recv_message)
            self.recv_thread.daemon = True
            self.recv_thread.start()
            self.username = username  # 保存用户名
            self.client.send(username.encode('utf-8'))
            
        except Exception as e:
            QtWidgets.QMessageBox.critical(
                self, "连接错误",
                f"无法连接到服务器:\n{str(e)}\n请检查服务器是否运行",
                buttons=QtWidgets.QMessageBox.StandardButton.Ok
            )
            self.close()
    def load_recent_messages(self):
        try:
            #临时连接数据库获取历史消息
            db = DbM(host="192.168.3.159", user = "chat_room",
                      password = "zhishou_chat")
            messages = db.get_recent_messages(limit=50)
            for msg in reversed(messages):
                display_text = f"{msg['username']}: {msg['message']}"
                self.append_message(display_text)
        except Exception as e:
            print(f"加载历史消息失败: {str(e)}")

            
    def eventFilter(self, source, event):
        """实现回车发送功能"""
        if (event.type() == QtCore.QEvent.Type.KeyPress and
            source is self.textEdit and
            event.key() == Qt.Key.Key_Return and
            not event.modifiers()):
            
            self.send_message()
            return True
        return super().eventFilter(source, event)

    def send_message(self):
        """发送消息处理"""
        text = self.textEdit.toPlainText().strip()
        if text:
            try:
                self.client.send(text.encode('utf-8'))
                self.textEdit.clear()
                self.textEdit.setFocus()
                # 在本地显示自己发送的消息
                self.append_message(f"我: {text}")
                i = 1
            except Exception as e:
                QtWidgets.QMessageBox.warning(
                    self, "发送失败",
                    f"消息发送失败:\n{str(e)}",
                    buttons=QtWidgets.QMessageBox.StandardButton.Ok
                )

    def recv_message(self):
        """接收消息线程"""
        while self.running:
            try:
                data = self.client.recv(1024).decode('utf-8')
                if not data:
                    break           
                if data.startswith('ONLINE:'):
                    self.update_signal.emit(f"ONLINE:{data[7:]}")
                else:
                    self.update_signal.emit(data)
            except ConnectionResetError:
                self.update_signal.emit("[系统] 连接已断开")
                break
            except:
                break

    def append_message(self, msg):
        """追加消息到显示区域"""
        cursor = self.shu_chu.textCursor()
        cursor.movePosition(QtGui.QTextCursor.MoveOperation.End)
        cursor.insertText(msg + '\n\n')
        self.shu_chu.setTextCursor(cursor)
        self.shu_chu.ensureCursorVisible()

    def update_display(self, msg):
        """处理界面更新（修复版）"""
        if msg.startswith("ONLINE:"):
            # 安全解析用户数据
            try:
                users_part = msg[7:].strip()  # 移除前后空白
                users = [u.strip() for u in users_part.split(',') if u.strip()]
            except Exception as e:
                print(f"解析在线列表错误: {str(e)}")
                users = []

            # 保证user_list始终有初始值
            user_list = ["在线用户\n-----------"]
            
            if users:  # 有有效用户时处理
                for user in users:
                    display_name = f"● {user}"
                    if user == self.username:
                        display_name += " (你)"
                    user_list.append(display_name)
            else:  # 无用户时显示提示
                user_list.append("暂无其他在线用户")
            
            # 设置显示文本（确保至少有空列表）
            final_text = '\n'.join(user_list)
            self.zai_xian_list.setText(final_text)
            
            self.zai_xian_list.setText('\n'.join(user_list) + '\n')
            
        else:  # 普通消息处理
            self.append_message(msg)
            if msg.startswith('ONLINE:'):
                # 解析在线用户数据
                users = msg[7:].split(',')  # 格式应为 "ONLINE:user1,user2"
                users = [u.strip() for u in users if u.strip()]  # 清理空白项
            
                # 构建带格式的用户列表文本
                user_list = ["在线用户\n-----------"]
                for user in users:
                    if user == self.username:
                        user_list.append(f"● {user} (你)")  # 标记当前用户
                    else:
                        user_list.append(f"● {user}")
            

    def closeEvent(self, event):
        """窗口关闭事件处理"""
        self.running = False
        if self.client:
            self.client.close()
        event.accept()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    font = QFont("宋体", 10)
    app.setFont(font)
    window = ChatWindow()
    window.show()
    sys.exit(app.exec())