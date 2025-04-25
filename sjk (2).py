import mysql.connector
from mysql.connector import Error
from datetime import datetime

class DbM:
    def __init__(self,host:str, user:str, password:str, database:str = "chat_room"):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            if self.connection.is_connected():
                print("成功连接到数据库")
        except Error as e:
            print(f"连接数据库失败: {e}")
    def close(self):
        if self.connection.is_connected():
            self.connection.close()
            print("数据库连接已关闭")
    def save_message(self, username: str, message: str,ip_address = None) -> bool:
        try:
            if not self.connection or not self.connection.is_connected():
                self.connect()
            curcor = self.connection.cursor()
            sql = "INSERT INTO chat_messages (username, message, ip_address) VALUES (%s, %s, %s)"
            curcor.execute(sql, (username, message, ip_address))
            self.connection.commit()
            print("消息已保存")
            return True
        except Error as e:
            print(f"保存消息失败: {e}")
            return False
    def get_recent_messages(self, limit: int = 50) -> list:
        try:
            if not self.connection or not self.connection.is_connected():
                self.connect()
            curcor = self.connection.cursor(dictionary=True)
            sql = "SELECT username,message,send_time FROM chat_messages ORDER BY send_time DESC LIMIT %s"
            curcor.execute(sql, (limit,))
            results = curcor.fetchall()
            return results
        except Error as e:
            print(f"获取消息失败: {e}")
            return []
    def clear_all_messages(self) -> bool:
        try:
            if not self.connection or not self.connection.is_connected():
                self.connect()
            curcor = self.connection.cursor()
            sql = "TRUNCATE TABLE chat_messages"
            curcor.execute(sql)
            self.connection.commit()
            print("所有消息已清除")
            return True
        except Error as e:
            print(f"清除消息失败: {e}")
            return False
        finally:
            if curcor:
                curcor.close()
if __name__ == "__main__":
    pass
