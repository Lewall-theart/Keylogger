import socket

def start_server(host, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)
    print(f"Server is listening on {host}:{port}")

    conn, addr = server_socket.accept()
    print(f"Connected by {addr}")

    with open('received_log.txt', 'wb') as file:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            file.write(data)

    conn.close()
    print("File received and server closed.")

if __name__ == '__main__':
    start_server('0.0.0.0', 65432)  # Thay đổi host và port nếu cần
