# tool_check_status_fb_python
Dùng để kiểm tra tình trạng hoạt động của danh sách các link facebook. Đặc biệt ứng dụng vào việc theo dõi scam trên facebook.
<!-- Banner -->
<p align="center">
    <img src="https://upload.wikimedia.org/wikipedia/commons/d/d0/Icon_scam11.gif" alt="Scam symbol">
  </a>
</p>
<!-- Title -->
<h1 align="center"><b> Tool Check Status on FB </b></h1>

## GIỚI THIỆU
* **Ngày tạo:** 7/2023
* **Tác giả:** **ĐỖ PHI SƠN** - *dophison2002@gmail.com*
## CÁC THÀNH PHẦN
* checkscam.txt : File lưu trữ các thông tin hiển thị cơ bản khi truy cập localhost (danh sách tổng quát)
* debug_link.txt: File lưu trữ các thông tin cần kiểm tra tình trạng (Link facebook chứa id user - nếu link đã bị đổi thành bí danh thì dùng postman để tìm id) sử dụng trong route /status
* history.html: File lưu trữ lịch sử có thời gian chi tiết sau khi vào route /status kiểm tra tình trạng. Có 3 tình trạng theo màu sắc: <span style="color: red">màu đỏ - link không tồn tại/bị khoá/bị block</span>; <span style="color: green">màu xanh - link còn sử dụng và truy cập được</span>; <span style="color: yellow">màu vàng - một số trường hợp không đúng format (có thể nền tảng facebook thay đổi cấu trúc đăng nhập/thông tin trả về,...)</span>
* web_checkstatus.py: File là thành phần chính của công cụ, chứa 3 route là: / ; /status ; /history
* Cần cài đặt các thư viện tương ứng và lưu ý tool có dùng selenium vì thế cần cài đặt geckodriver (v0.33.0 đã chạy tốt).
## HƯỚNG DẪN SỬ DỤNG
* Sau khi git clone thành công -> đề nghị dùng PyCharm Edition để có thể hỗ trợ cài đặt các package phù hợp trong .venv 
* Chỉnh sửa biến môi trường trong **Edit environment variables for your account** (Windows) để đặt tài khoản, mật khẩu tài khoản facebook. Trong file web_checkstatus.py tại _dòng 106, 107, 108_ chỉnh sửa cho phù hợp để đáp ứng.
* Chỉnh sửa các file checkscam.txt và debug_link.txt để đáp ứng nhu cầu. Lưu ý: không nên để dòng trống (\n) trong hai file này -> sinh ra lỗi.
* Chạy file web_checkstatus.py
## FLOW
* / : hiển thị file checkscam.txt
* /status: đọc file debug_link.txt --> mở lần lượt từng link (lấy đường dẫn mới nhất và tên) --> nếu link không truy cập được --> đăng nhập facebook và kiểm tra lại (trường hợp xảy ra khi users bật tính năng không công khai tài khoản) --> hiển thị tình trạng --> ghi vào history.html
* /history: hiển thị file history.html 
## Nền tảng
* Python (Flask, Selenium)
* HTML (hiển thị cơ bản)
## Tính năng có thể phát triển
* Auto unfriend/addfriend on Facebook.
* Kiểm tra tình trạng mối quan hệ bạn bè ( bạn bè có thể block bạn hoặc đổi tên nhưng bạn không biết,...)
