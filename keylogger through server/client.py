import socket

def send_log_file(file_path, server_host, server_port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_host, server_port))

    with open(file_path, 'rb') as file:
        while chunk := file.read(1024):
            client_socket.send(chunk)

    client_socket.close()
    print("Log file sent and client closed.")

if __name__ == '__main__':
    send_log_file('C:\\path_to_log\\log.txt', '192.168.x.x', 65432)  # Thay đổi IP và port nếu cần
