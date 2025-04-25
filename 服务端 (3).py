import socket
import threading
from sjk import DbM
db_m = DbM(host = "192.168.3.159",user= "chat_room",password="zhishou_chat")

# 配置信息
HOST = '0.0.0.0'  # 监听所有网络接口
PORT = 12345       # 监听的端口号

# 线程锁和共享数据
lock = threading.Lock()
clients = []        # 存储所有客户端连接
usernames = {}      # 存储用户名与套接字的映射

def broadcast(message, sender_socket=None):
    """广播消息给所有客户端（排除发送者）"""
    with lock:
        # 创建副本避免遍历时修改原始列表
        clients_copy = clients.copy()
    
    for client in clients_copy:
        if client != sender_socket:
            try:
                client.send(message.encode('utf-8'))
            except:
                # 发送失败则关闭连接并清理
                with lock:
                    if client in clients:
                        clients.remove(client)
                    if client in usernames:
                        del usernames[client]
                client.close()

def handle_client(client_socket):
    """处理单个客户端的连接"""
    try:
        # 接收用户名
        username = client_socket.recv(1024).decode('utf-8').strip()
        if not username:
            raise Exception("无效用户名")
        
        # 获取客户端IP
        ip_address = client_socket.getpeername()[0]
        
        # 记录用户信息
        with lock:
            usernames[client_socket] = username
            clients.append(client_socket)
        
        # 通知所有用户新成员加入
        broadcast(f"[系统] {username} 进入了聊天室", client_socket)
        print(f"[系统] {username} 已连接")
        
        # 持续接收消息
        while True:
            message = client_socket.recv(1024).decode('utf-8').strip()
            if not message:
                break
            full_msg = f"{username}: {message}"
            
            # 保存消息到数据库
            db_m.save_message(username, message, ip_address)
            
            broadcast(full_msg, client_socket)
            
    except Exception as e:
        print(f"[错误] 连接异常: {e}")
    finally:
        # 清理客户端资源
        with lock:
            if client_socket in clients:
                clients.remove(client_socket)
            username = usernames.get(client_socket, "未知用户")
            if client_socket in usernames:
                del usernames[client_socket]
        client_socket.close()
        broadcast(f"[系统] {username} 离开了聊天室", None)
        print(f"[系统] {username} 已断开")

def start_server():
    """启动服务器"""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print(f"[系统] 服务器已启动，监听 {HOST}:{PORT}")
    
    try:
        while True:
            client_socket, addr = server.accept()
            print(f"[系统] 新连接来自 {addr}")
            # 为每个客户端创建新线程
            threading.Thread(target=handle_client, args=(client_socket,)).start()
    except KeyboardInterrupt:
        print("\n[系统] 服务器正在关闭...")
    finally:
        server.close()

if __name__ == "__main__":
    start_server()
