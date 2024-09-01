# Keylogger

## Giới Thiệu

Chương trình này là một keylogger đơn giản cho Windows, được thiết kế để ghi lại các hành động nhập từ bàn phím của người dùng và gửi file log chứa dữ liệu này đến một máy chủ Linux qua SCP (Secure Copy Protocol). 

Chương trình cũng được cấu hình để tự động chạy khi người dùng đăng nhập vào hệ thống, giúp duy trì hoạt động liên tục.

**Lưu ý quan trọng:** Chương trình này được cung cấp chỉ với mục đích học tập và nghiên cứu an ninh mạng. Việc sử dụng hoặc phát triển các công cụ như vậy trong các tình huống không được phép có thể vi phạm pháp luật và các chính sách bảo mật. Hãy sử dụng nó một cách có trách nhiệm.

## Yêu Cầu

- Windows 10 hoặc Windows 11
- Python 3.x
- Các thư viện Python:
  - `pywin32`
  - `pyHook`
  - `paramiko`

## Cài Đặt

### Cài Đặt Python và Thư Viện

1. Cài đặt Python từ [python.org](https://www.python.org/downloads/).
2. Cài đặt các thư viện cần thiết bằng pip:

   ```bash
   pip install -r requirements.txt
